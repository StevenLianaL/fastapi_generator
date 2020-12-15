from abc import abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd

from fastapi_generator.data import (
    space, orm_type_mapping, python_type_mapping,
    pydantic_type_mapping, tortoise_type_mapping, orm_field_options, tortoise_field_options
)


class FileMixin:

    @classmethod
    def write_rows(cls, file: Path, rows: Optional[List[str]] = None, row: Optional[str] = None, mode: str = 'w'):
        assert bool(rows) ^ bool(row), "row and rows can work only one."
        if not rows:
            rows = [row]
        with file.open(mode=mode, encoding='utf8') as fa:
            for row in rows:
                fa.write(f"{row}\n")


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


@dataclass
class Creation(FileMixin, TableMixin):
    db_name: str
    engine: any
    file: Path
    rows: Tuple[str] = field(default_factory=tuple)
    col_prefix: str = ''
    type_mapping: dict = field(default_factory=dict)
    field_options: dict = field(default_factory=dict)

    def generate(self):
        self.write_rows(file=self.file, mode='w', rows=self.rows)
        tables = self.read_tables(db_name=self.db_name, engine=self.engine)
        tables.groupby('TABLE_NAME').apply(self._make_from_table)

    def _make_from_table(self, table: pd.DataFrame):
        tb_name: str = table['TABLE_NAME'].values[0]

        # write table orm meta
        self.write_rows(file=self.file, mode='a', rows=self._class_rows(tb_name=tb_name))
        # write table col field
        table.apply(self._make_field, axis=1)

        self.write_rows(file=self.file, mode='a', row='\n')

    def _make_field(self, col: pd.Series):
        the_field = self.generate_field(col)
        self.write_rows(file=self.file, mode='a', row=the_field)

    @abstractmethod
    def _class_rows(self, tb_name: str) -> Tuple[str]:
        """"""

    @staticmethod
    def _is_param_first(params: list):
        """Only used to determine whether the parameter is the first parameter of the field."""
        return len(params) <= 1

    def generate_field(self, col: pd.Series) -> str:
        params = []
        col_name: str = col['COLUMN_NAME']
        col_type = col['DATA_TYPE']
        res = f"{space * 4}{col_name} = {self.col_prefix}.{self.type_mapping[col_type]}()"

        is_null = col['IS_NULLABLE'] == 'YES'  # Set the default to None
        if is_null:
            params.append(is_null)
            null_str = f"{self.field_options['IS_NULLABLE']}={is_null},"
            res = self.combine_param(res=res, param_str=null_str, is_first=self._is_param_first(params))

        # default has (null, CURRENT_TIMESTAMP, int, float, empty str, str)
        col_default = col['COLUMN_DEFAULT']  # Set default
        if col_default is not None and col_default != 'CURRENT_TIMESTAMP':  # only set int/float/str
            params.append(col_default)
            default_val = python_type_mapping[col_type](col_default)
            if isinstance(default_val, str):
                default_str = f"{self.field_options['COLUMN_DEFAULT']}='{default_val}',"
            else:
                default_str = f"{self.field_options['COLUMN_DEFAULT']}={default_val},"
            res = self.combine_param(res=res, param_str=default_str, is_first=self._is_param_first(params))

        # keys has (MUL PRI UNI)
        col_key = col['COLUMN_KEY']
        if col_key:  # cannot handle foreignkey
            if col_key == 'UNI':
                params.append(col_key)
                unique_str = f"{self.field_options['UNI']}=True,"
                res = self.combine_param(res=res, param_str=unique_str, is_first=self._is_param_first(params))

            elif col_key == 'PRI':
                params.append(col_key)
                pk_str = f"{self.field_options['PRI']}=True,"
                res = self.combine_param(res=res, param_str=pk_str, is_first=self._is_param_first(params))

            elif col_key == 'MUL':
                foreign_name = f"{col_name[:-3]}s".capitalize()
                foreign_key_str = f"{space * 4}# {col_name[:-3]}={self.col_prefix}.ForeignKey({foreign_name})"
                self.write_rows(file=self.file, mode='a', row=foreign_key_str)

        # str len
        try:
            col_str_len = int(float(str(col['CHARACTER_MAXIMUM_LENGTH'])))
            if col_str_len > 0:
                params.append(col_str_len)
                len_str = f"{self.field_options['CHARACTER_MAXIMUM_LENGTH']}={col_str_len},"
                res = self.combine_param(res=res, param_str=len_str, is_first=self._is_param_first(params))
        except ValueError:
            pass

        # handle suffix comma
        if len(params):
            res = res[:-2] + res[-1]
        return res


@dataclass
class OrmCreation(Creation):
    """Used to generate orm for tables."""
    rows: Tuple[str] = (
        "import orm",
        "import sqlalchemy\n",
        "from app.db import database\n",
        "metadata = sqlalchemy.MetaData()\n\n"
    )

    def __post_init__(self):
        self.type_mapping = orm_type_mapping
        self.field_options = orm_field_options
        self.col_prefix = 'orm'

    def _class_rows(self, tb_name: str) -> Tuple[str]:
        return (
            f"class {self.count_model_name(tb_name=tb_name)}(orm.Model):",
            f'{space * 4}__tablename__ = "{tb_name}"',
            f'{space * 4}__database__ = database',
            f'{space * 4}__metadata__ = metadata\n'
        )


@dataclass
class TortoiseOrmCreation(Creation):
    rows: Tuple[str] = (
        "from tortoise import fields, models\n\n",
    )

    def __post_init__(self):
        self.type_mapping = tortoise_type_mapping
        self.field_options = tortoise_field_options
        self.col_prefix = 'fields'

    def _class_rows(self, tb_name: str) -> Tuple[str]:
        return (
            f"class {self.count_model_name(tb_name=tb_name)}(models.Model):",
        )


@dataclass
class InterfaceCreation(Creation):
    rows: Tuple[str] = (
        "from pydantic import BaseModel\n",
        "from datetime import datetime\n\n"
    )

    def _class_rows(self, tb_name: str) -> Tuple[str]:
        return f"class {self.count_model_name(tb_name=tb_name)}(BaseModel):",

    def generate_field(self, col: pd.Series) -> str:
        # name / type / default
        col_name: str = col['COLUMN_NAME']
        col_type = col['DATA_TYPE']
        res = f"{space * 4}{col_name}: {pydantic_type_mapping[col_type]}"
        col_default = col['COLUMN_DEFAULT']  # Set default
        if col_default is not None and col_default != 'CURRENT_TIMESTAMP':
            default_val = python_type_mapping[col_type](col_default)
            default_str = f"'{default_val}'" if isinstance(default_val, str) else f"{default_val}"
            res += f' = {default_str}'
        return res
