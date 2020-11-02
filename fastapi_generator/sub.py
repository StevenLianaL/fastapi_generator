from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import plac

from fastapi_generator.app import App
from fastapi_generator.config import ss


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

        for file in ss.app_files:
            self.write_file(name=f"{self.name}_{file}", parent='sub')

        router_dir = self.root_dir / 'router'
        router_dir.mkdir()


if __name__ == '__main__':
    app = SubApp()
    plac.call(app.create_app)
