import importlib

from fastapi import FastAPI, APIRouter


def load_app(sub_app_name: str) -> FastAPI:
    """Load sub app from module"""
    module = f'app.sub_apps.{sub_app_name}.{sub_app_name}_app'
    sub_app_module = importlib.import_module(module)
    for var in sub_app_module.__dict__.values():
        if isinstance(var, FastAPI):
            return var
    else:
        raise Exception('Not found FastAPI app.')


def load_api(sub_app_name: str, api_name: str) -> APIRouter:
    module = f"app.sub_apps.{sub_app_name}.router.{api_name}_api"
    api = importlib.import_module(module)
    for var in api.__dict__.values():
        if isinstance(var, APIRouter):
            return var
    else:
        raise Exception('Not found APIRouter.')
