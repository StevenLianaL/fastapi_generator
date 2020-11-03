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
