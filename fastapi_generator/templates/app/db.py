import sqlalchemy
from databases import Database

from app.config import project

DATABASE_URL = f"{project.DB_MODE}://{project.DB_USER}:{project.DB_PSWD}@{project.DB_HOST}/" \
               f"{project.DB_NAME}?charset=utf8"

database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL, encoding='utf-8')
