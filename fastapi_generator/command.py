import click

from fastapi_generator.api import create_api
from fastapi_generator.main import MainApp
from fastapi_generator.sub import SubApp


@click.group()
def fastapi():
    pass


@fastapi.command()
def main():
    app = MainApp()
    app.create_app()


@fastapi.command()
@click.option('--only', is_flag=True, help="only generate orm")
@click.option('--mode', default='o', help="choose mode in tortoise or orm")
@click.option('--db_host', default="localhost")
@click.option('--db_name', default='test')
@click.option('--db_user', default="test")
@click.option('--db_pswd', default="test")
def orm(db_name, db_host, db_user, db_pswd, only, mode):
    app = MainApp()
    app.create_app_with_orm(
        db_name=db_name, db_pswd=db_pswd, db_host=db_host, db_user=db_user, is_only_orm=only, mode=mode
    )


@fastapi.command()
@click.argument("sub_name", type=str)
def sub(sub_name):
    app = SubApp()
    app.create_app(name=sub_name)


@fastapi.command()
@click.argument("sub_name", type=str)
@click.argument("api_name", type=str)
def api(sub_name, api_name):
    create_api(sub_app_name=sub_name, api_name=api_name)


if __name__ == '__main__':
    fastapi()
