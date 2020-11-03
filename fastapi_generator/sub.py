from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from fastapi_generator.config import ss, ps


@dataclass
class SubApp:
    """Generate sub app for main"""
    name: str = ''
    root_dir: Optional[Path] = None

    def create_app(self, name: str):
        self.name = name
        self.write_files()

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

        # read
        with file.open(mode='r', encoding='utf8') as f:
            text = f.read()

        # write to target
        target = Path(self.root_dir, f"{self.name}_{file_name}").with_suffix('.py')
        with target.open(mode='w', encoding='utf8') as w:
            if target.stem == f"{self.name}_config":
                text = text.replace('sign_app_name', self.name)
            elif target.stem == f"{self.name}_app":
                old_text = 'import_setting_flag'
                new_text = f"from app.sub_apps.{self.name}.{self.name}_config import settings"
                text = text.replace(old_text, new_text)
            w.write(text)
