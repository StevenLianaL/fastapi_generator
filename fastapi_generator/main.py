from pathlib import Path

import plac

from fastapi_generator.app import App
from fastapi_generator.config import fs
from fastapi_generator.utils.helper import OrmCreation, InterfaceCreation


class MainApp(App):
    def create_app(self):
        super(MainApp, self).create_app()
        self.generate_orm()

    @staticmethod
    def create_app_files():
        # create folders
        for folder in fs.top_dirs:
            folder = Path(folder)
            if not folder.exists():
                folder.mkdir()

        # create app files
        for file in fs.app_files:
            Path(fs.root_dir, file).with_suffix('.py').touch()
        fs.sub_app_dir.mkdir(exist_ok=True)

        # create top files
        for file in fs.top_files:
            Path(file).touch()

    def write_files(self):
        for file in fs.app_files:
            self.write_file(name=file, parent='app')

        for file in fs.top_files:
            self.write_file(name=file)
        else:
            self.write_requirements()

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
