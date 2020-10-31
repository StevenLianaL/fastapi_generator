from pathlib import Path

import plac


def gen_main_app():
    # create folders
    folders = ['app', 'log', 'test']
    for folder in folders:
        folder = Path(folder)
        if not folder.exists():
            folder.mkdir()
    root_dir = Path('app')

    # create app files
    app_files = ('__init__', 'config', 'data', 'db', 'models', 'interface', 'main')
    app_dirs = ('sub_apps',)
    for file in app_files:
        Path(root_dir, file).with_suffix('.py').touch()
    for app_dir in app_dirs:
        Path(root_dir, app_dir).mkdir()

    # create top files
    top_files = ('README.md', 'requirements.txt', ' .gitignore')
    for file in top_files:
        Path(file).touch()


if __name__ == '__main__':
    plac.call(gen_main_app)
