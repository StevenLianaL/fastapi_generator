space = ' '

orm_type_mapping = {
    "tinyint": "Integer",
    "smallint": "Integer",
    "bigint": "Integer",
    "int": "Integer",
    "float": "Float",
    "varchar": f"String",
    "longtext": "Text",
    "text": "Text",
    "datetime": "DateTime",
    "date": "DateTime",
    "timestamp": "DateTime",
}

tortoise_field_options = {
    "IS_NULLABLE": "null",
    "COLUMN_DEFAULT": "default",
    "CHARACTER_MAXIMUM_LENGTH": "max_length",
    "UNI": "unique",
    "PRI": "pk",
}

orm_field_options = {
    "IS_NULLABLE": "allow_null",
    "COLUMN_DEFAULT": "default",
    "CHARACTER_MAXIMUM_LENGTH": "max_length",
    "UNI": "unique",
    "PRI": "primary_key",
}

tortoise_type_mapping = {
    "tinyint": "SmallIntField",
    "smallint": "SmallIntField",
    "bigint": "BigIntField",
    "int": "IntField",
    "float": "FloatField",
    "varchar": "CharField",
    "longtext": "TextField",
    "text": "TextField",
    "datetime": "DatetimeField",
    "date": "DatetimeField",
    "timestamp": "DatetimeField",
}

python_type_mapping = {
    "tinyint": int,
    "smallint": int,
    "bigint": int,
    "int": int,
    "float": float,
    "varchar": str,
    "text": str,
}

pydantic_type_mapping = {
    "tinyint": 'int',
    "smallint": 'int',
    "bigint": 'int',
    "int": 'int',
    "float": 'float',
    "varchar": 'str',
    "text": 'str',
    "datetime": 'datetime',
    "date": 'datetime',
    "timestamp": 'datetime',
}

fastapi_run_requires = (
    'fastapi', 'uvicorn', 'sqlalchemy', 'databases', 'aiomysql',
    'mysqlclient', 'orm')
