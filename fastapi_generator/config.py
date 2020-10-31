from pathlib import Path


class Settings:
    top_dirs = ('app', 'log', 'test')
    top_files = ('README.md', 'requirements.txt', '.gitignore')
    app_dirs = ('sub_apps',)
    app_files = ('__init__', 'config', 'data', 'db', 'models', 'interface', 'main')

    root_dir = Path('app')
