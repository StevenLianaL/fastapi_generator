from pathlib import Path

from fastapi_generator.data import fastapi_run_requires


class FastapiSettings:
    top_dirs = ('app', 'log', 'test')
    top_files = ('README.md', 'requirements.txt', '.gitignore')
    app_files = [f"{i}.py" for i in (
        '__init__', 'config', 'utils', 'db', 'data',
        'models', 'interface', 'main'
    )]

    root_dir = Path('app')
    sub_app_dir = root_dir / 'sub_apps'
    orm_file = root_dir / 'models.py'
    interface_file = root_dir / 'interface.py'

    requires = fastapi_run_requires
    require_file = root_dir.parent / 'requirements.txt'


class SubAppSettings:
    fs = FastapiSettings()

    app_files = [f"{i}" for i in ('app', 'help', 'interface', 'config')]


class ProjectSettings:
    root_dir = Path(__file__).resolve(strict=True).parent
    template_dir = root_dir / 'templates'

    orm_file = template_dir / 'app' / 'models'
    interface_file = template_dir / 'app' / 'interface'


fs = FastapiSettings()
ps = ProjectSettings()
ss = SubAppSettings()
