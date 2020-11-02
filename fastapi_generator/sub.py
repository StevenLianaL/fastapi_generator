from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import plac

from fastapi_generator.app import App
from fastapi_generator.config import ss, ps


@dataclass
class SubApp(App):
    """Generate sub app for main"""
    name: str = ''
    root_dir: Optional[Path] = None

    @plac.pos('name', "sub app name", type=str)
    def create_app(self, name):
        """
        :type name: str
        """
        self.name = name
        super(SubApp, self).create_app()

    def write_files(self):
        self.root_dir = ss.fs.sub_app_dir / f"{self.name}"
        self.root_dir.mkdir(exist_ok=True)

        for file_name in ss.app_files:
            self.write_file(file_name)
        else:
            Path(self.root_dir / '__init__.py').touch()

        router_dir = self.root_dir / 'router'
        router_dir.mkdir()

    def write_file(self, file_name: str):
        sub_template = ps.template_dir / 'sub'
        file = sub_template / file_name
        with file.open(mode='r', encoding='utf8') as f:
            text = f.read()
        target = self.root_dir / f"{self.name}_{file_name}"
        with target.open(mode='w', encoding='utf8') as w:
            w.write(text)


if __name__ == '__main__':
    app = SubApp()
    plac.call(app.create_app)
