from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# from tortoise.contrib.fastapi import register_tortoise

from app.config import project
from app.db import database
from app.utils import load_app

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'], allow_credentials=True,
                   allow_methods=['*'], allow_headers=['*']
                   )


@app.get('/')
async def index():
    return 'welcome to FastAPI!'


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# auto load sub apps
sub_app_names = [i.stem for i in project.SUB_APP_DIR.iterdir()]
for sub_app_name in sub_app_names:
    app.mount(f"/{sub_app_name}", app=load_app(sub_app_name), name=sub_app_name)


# register_tortoise(
#     app,
#     db_url=f'mysql://{project.DB_USER}:{project.DB_PSWD}@{project.DB_HOST}:3306/{project.DB_NAME}',
#     modules={"models": ["app.models"]},
#     generate_schemas=False,
#     add_exception_handlers=True,
# )