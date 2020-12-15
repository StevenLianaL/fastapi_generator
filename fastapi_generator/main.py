from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import sqlalchemy

from fastapi_generator.config import fs, ps
from fastapi_generator.utils.helper import OrmCreation, InterfaceCreation, TortoiseOrmCreation


@dataclass
class MainApp:
    def create_app(self):
        self.write_files()

    def create_app_with_orm(
            self, db_name: str = '', db_host: str = '', db_user: str = '', db_pswd: str = '',
            is_only_orm: bool = False, mode: str = 'o'
    ):
        if not is_only_orm:
            self.write_files()
        self.generate_orm(db_name=db_name, db_host=db_host, db_user=db_user, db_pswd=db_pswd, mode=mode)

    def write_files(self):

        for folder in fs.top_dirs:
            folder = Path(folder)
            if not folder.exists():
                folder.mkdir()

        fs.sub_app_dir.mkdir(exist_ok=True)

        for file in fs.app_files:
            self.write_file(name=file, parent='app')

        for file in fs.top_files:
            self.write_file(name=file)
        else:
            self.write_requirements()

    @staticmethod
    def write_file(name: str, parent: Optional[str] = None):
        """
        :param name: file name
        :param parent: if file is under folder, use parent
        """
        if parent:
            file = Path(parent, name)
            template = ps.template_dir / parent / name
        else:
            file = Path(name)
            template = ps.template_dir / name
        try:
            with template.open(mode='r', encoding='utf8') as f:
                text = f.read()
            with file.open(mode='w', encoding='utf8') as w:
                w.write(text)
        except FileNotFoundError:
            print(f"{ps.template_dir / parent / name} not found")

    @staticmethod
    def write_requirements():
        with fs.require_file.open(mode='a', encoding='utf8') as w:
            for package in fs.requires:
                w.write(f"{package}\n")

    @staticmethod
    def generate_orm(db_name: str, db_host: str, db_user: str, db_pswd: str, mode: str):
        if not fs.root_dir.exists():
            fs.root_dir.mkdir()
        database_url = f"mysql://{db_user}:{db_pswd}@{db_host}/" \
                       f"{db_name}?charset=utf8"
        engine = sqlalchemy.create_engine(database_url, encoding='utf-8')
        if mode == 'o':
            orm_class = OrmCreation
        elif mode == 't':
            orm_class = TortoiseOrmCreation
        else:
            raise ValueError('no orm')
        orm_creation = orm_class(db_name=db_name, engine=engine, file=fs.orm_file)
        orm_creation.generate()
        interface_creation = InterfaceCreation(
            db_name=db_name, engine=engine, file=fs.interface_file)
        interface_creation.generate()
