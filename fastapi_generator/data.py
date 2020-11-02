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
