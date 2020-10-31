from pathlib import Path

import plac

from fastapi_generator.config import Settings


def gen_main_app():
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


if __name__ == '__main__':
    plac.call(gen_main_app)
