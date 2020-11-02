from abc import abstractmethod
from pathlib import Path
from typing import Optional

from fastapi_generator.config import ps


class App:
    def create_app(self):
        self.create_app_files()
        self.write_files()

    @abstractmethod
    def write_files(self):
        """"""

    @staticmethod
    @abstractmethod
    def create_app_files():
        """"""

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
