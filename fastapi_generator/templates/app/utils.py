import importlib
from dataclasses import dataclass
from typing import Iterator

from fastapi import FastAPI, APIRouter, Depends, Header
# from redis import StrictRedis
from starlette.middleware.cors import CORSMiddleware
# from tortoise.exceptions import DoesNotExist

from app.config import project
# from app.middle import RecordMiddleware
from app.sub_apps.auth.depends import AuthHeaders


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


@dataclass
class AuthHeaders:
    jwt: str = Header('', description="pass jwt in header")


@dataclass
class Appbuilder:
    app_name: str

    def __post_init__(self):
        self.app = FastAPI(dependencies=[Depends(AuthHeaders)], title=self.app_name)
        self.build_app()

    def build_app(self) -> FastAPI:
        self._add_middlewares()
        # self._add_redis()
        self._add_routers()
        return self.app

    def _add_middlewares(self):
        self.app.add_middleware(CORSMiddleware,
                                allow_origins='*',
                                allow_methods=['*'],
                                allow_headers=['*'],
                                allow_credentials=True)

    # def _add_redis(self):
    #     self.app.state.redis = StrictRedis(
    #         host=project.REDIS_HOST,
    #         db=project.REDIS_DB,
    #         decode_responses=True
    #     )

    def _add_routers(self):
        for router_file in self._count_router_files():
            api_name = router_file.stem.replace('_api', '')
            if api_name != "__pycache__":
                api = load_api(sub_app_name=self.app_name, api_name=api_name)
                self.app.include_router(router=api, prefix=f"/{api_name}", tags=[api_name])

    def _count_router_files(self) -> Iterator:
        router_dir = project.SUB_APP_DIR / self.app_name / 'router'
        return router_dir.iterdir()