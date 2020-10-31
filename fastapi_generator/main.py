from pathlib import Path

import plac

from fastapi_generator.config import Settings


class MainApp:
    @staticmethod
    def create_app_files():
        # create folders
        for folder in Settings.top_dirs:
            folder = Path(folder)
            if not folder.exists():
                folder.mkdir()

        # create app files
        for file in Settings.app_files:
            Path(Settings.root_dir, file).with_suffix('.py').touch()
        for app_dir in Settings.app_dirs:
            Path(Settings.root_dir, app_dir).mkdir()

        # create top files
        for file in Settings.top_files:
            Path(file).touch()

    def create_app(self):
        self.create_app_files()


if __name__ == '__main__':
    app = MainApp()
    plac.call(app.create_app)
