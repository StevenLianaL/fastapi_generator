from pathlib import Path
from typing import Optional

import plac

from fastapi_generator.config import fs, ps


class MainApp:

    def create_app(self):
        self.create_app_files()
        self.write_files()

    def write_files(self):
        for file in fs.app_files:
            self.write_file(name=file, parent='app')

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
        for app_dir in fs.app_dirs:
            Path(fs.root_dir, app_dir).mkdir()

        # create top files
        for file in fs.top_files:
            Path(file).touch()

    @staticmethod
    def write_file(name: str, parent: Optional[str] = None):
        """
        :param name: file name
        :param parent: if file is under folder, use parent
        """
        if parent:
            file = Path(parent, name).with_suffix('.py')
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


if __name__ == '__main__':
    app = MainApp()
    plac.call(app.create_app)
