from pathlib import Path

import envoy
import pandas as pd

from fastapi_generator.data import space, orm_type_mapping, python_type_mapping


class TableMixin:
    @staticmethod
    def read_tables(db_name: str, engine) -> pd.DataFrame:
        """
        :param db_name: db name str
        :param engine: sqlalchemy engine
        """
        sql = f"SELECT * FROM information_schema.columns WHERE table_schema = '{db_name}';"
        tables = pd.read_sql(sql, engine).sort_values(['TABLE_NAME', 'ORDINAL_POSITION'])
        return tables

    @staticmethod
    def count_model_name(tb_name: str) -> str:
        model = ''.join([i.capitalize() for i in tb_name.split('_')])
        return model

    @staticmethod
    def combine_param(res: str, param_str: str, is_first: bool = True) -> str:
        param_str = param_str if is_first else f" {param_str}"
        return res[:-1] + param_str + res[-1]


class Creation:
    pass


class OrmCreation(Creation, TableMixin):
    def generate_orm(self, db_name: str, engine, orm_file: Path):
        """generate orm to orm_file by db_name"""
        rows = (
            "import orm",
            "import sqlalchemy\n",
            "from app.db import database\n",
            "metadata = sqlalchemy.MetaData()\n\n"
        )
        with orm_file.open(mode='w', encoding='utf8') as fa:
            for row in rows:
                fa.write(row + '\n')
        tables = self.read_tables(db_name=db_name, engine=engine)
        tables.groupby('TABLE_NAME').apply(self.make_orm_table, file=orm_file)

    def make_orm_table(self, table, file: Path):
        tb_name: str = table['TABLE_NAME'].values[0]
        rows = (
            f"class {self.count_model_name(tb_name=tb_name)}(orm.Model):",
            f'{space * 4}__tablename__ = "{tb_name}"',
            f'{space * 4}__database__ = database',
            f'{space * 4}__metadata__ = metadata\n'
        )
        # write table orm meta
        with file.open(mode='a', encoding='utf8') as fa:
            for row in rows:
                fa.write(row + '\n')
        # write table col field
        table.apply(self.make_orm_field, axis=1, file=file)

        with file.open(mode='a', encoding='utf8') as fa:
            fa.write('\n\n')

    def make_orm_field(self, col: pd.Series, file: Path):
        """"""
        field = self.generate_field(col, file=file)
        with file.open(mode='a', encoding='utf8') as fa:
            fa.write(field + '\n')

    def generate_field(self, field: pd.Series, file: Path) -> str:
        params = []
        col_name: str = field['COLUMN_NAME']
        col_type = field['DATA_TYPE']
        res = f"{space * 4}{col_name} = orm.{orm_type_mapping[col_type]}()"

        is_null = field['IS_NULLABLE'] == 'YES'  # Set the default to None
        if is_null:
            params.append(is_null)
            null_str = f"allow_null={is_null},"
            res = self.combine_param(res=res, param_str=null_str, is_first=self._is_param_first(params))

        # default has (null, CURRENT_TIMESTAMP, int, float, empty str, str)
        col_default = field['COLUMN_DEFAULT']  # Set default
        if col_default is not None and col_default != 'CURRENT_TIMESTAMP':  # only set int/float/str
            params.append(col_default)
            default_val = python_type_mapping[col_type](col_default)
            default_str = f"default='{default_val}'," if isinstance(default_val, str) else f"default={default_val},"
            res = self.combine_param(res=res, param_str=default_str, is_first=self._is_param_first(params))

        # keys has (MUL PRI UNI)
        col_key = field['COLUMN_KEY']
        if col_key:  # cannot handle foreignkey
            if col_key == 'UNI':
                params.append(col_key)
                unique_str = f"unique=True,"
                res = self.combine_param(res=res, param_str=unique_str, is_first=self._is_param_first(params))

            elif col_key == 'PRI':
                params.append(col_key)
                pk_str = f"primary_key=True,"
                res = self.combine_param(res=res, param_str=pk_str, is_first=self._is_param_first(params))

            elif col_key == 'MUL':
                foreign_name = f"{col_name[:-3]}s".capitalize()
                foreign_key_str = f"{space * 4}# {col_name[:-3]}=orm.ForeignKey({foreign_name})"
                with file.open(mode='a', encoding='utf8') as fa:
                    fa.write(foreign_key_str + '\n')

        # str len
        try:
            col_str_len = int(float(str(field['CHARACTER_MAXIMUM_LENGTH'])))
            if col_str_len > 0:
                params.append(col_str_len)
                len_str = f"max_length={col_str_len},"
                res = self.combine_param(res=res, param_str=len_str, is_first=self._is_param_first(params))
        except ValueError:
            pass

        # handle suffix comma
        if len(params):
            res = res[:-2] + res[-1]
        return res

    @staticmethod
    def _is_param_first(params: list):
        """Only used to determine whether the parameter is the first parameter of the field."""
        return len(params) <= 1


def is_package_installed(package: str) -> bool:
    package_res = envoy.run('pip list')
    packages = [p.split(' ')[0] for p in package_res.std_out.split('\n') if p]
    return package in packages
