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

    # db
    MYSQL_HOST = '' if not DEBUG else 'localhost'
    MYSQL_DB = '' if not DEBUG else 'test'
    MYSQL_USER = '' if not DEBUG else 'test'
    MYSQL_PSWD = '' if not DEBUG else 'test'

    # dir
    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
    APP_DIR = ROOT_DIR / 'app'
    LOG_DIR = ROOT_DIR / 'log'


project = Settings()
