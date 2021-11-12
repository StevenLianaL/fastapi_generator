import platform
from pathlib import Path

from pydantic import BaseSettings


def is_debug():
    system = platform.system()
    dev_system = ('Windows', 'Darwin')
    return True if system in dev_system else False


class Settings(BaseSettings):
    # mode
    DEBUG = is_debug()

    PROJECT = ''

    # db
    DB_MODE = 'mysql'
    DB_HOST = '' if not DEBUG else 'localhost'
    DB_NAME = '' if not DEBUG else 'test'
    DB_USER = '' if not DEBUG else 'test'
    DB_PSWD = '' if not DEBUG else 'test'

    # redis
    REDIS_HOST = '' if not DEBUG else 'localhost'
    REDIS_DB = 1

    # dir
    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
    APP_DIR = ROOT_DIR / 'app'
    SUB_APP_DIR = APP_DIR / 'sub_apps'
    LOG_DIR = ROOT_DIR / 'log'

    # time
    utc = 'UTC'
    timezone = 'Asia/Shanghai'
    format = 'YYYY-MM-DD HH:mm:ss'


project = Settings()
