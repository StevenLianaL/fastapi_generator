from pathlib import Path
from typing import Optional

import plac

from fastapi_generator.app import App
from fastapi_generator.config import fs, ps
from fastapi_generator.utils.helper import OrmCreation, InterfaceCreation


class MainApp(App):
    def create_app(self):
        super(MainApp, self).create_app()
        self.generate_orm()

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
    def generate_orm():
        try:
            from app.db import engine
            from app.config import project
        except ImportError as e:
            raise Exception(f'cannot import engine:{e}')
        orm_creation = OrmCreation(db_name=project.DB_NAME, engine=engine, file=fs.orm_file)
        orm_creation.generate()
        interface_creation = InterfaceCreation(
            db_name=project.DB_NAME, engine=engine, file=fs.interface_file)
        interface_creation.generate()


if __name__ == '__main__':
    app = MainApp()
    plac.call(app.create_app)
