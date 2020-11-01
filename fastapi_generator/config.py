from pathlib import Path


class FastapiSettings:
    top_dirs = ('app', 'log', 'test')
    top_files = ('README.md', 'requirements.txt', '.gitignore')
    app_dirs = ('sub_apps',)
    app_files = ('__init__', 'config', 'db', 'data', 'models', 'interface', 'main')

    root_dir = Path('app')
    orm_file = root_dir / 'models.py'

    orm_require_package = ('pandas', 'orm')


class ProjectSettings:
    root_dir = Path(__file__).resolve(strict=True).parent
    template_dir = root_dir / 'templates'

    orm_file = template_dir / 'app' / 'models'
    interface_file = template_dir / 'app' / 'interface'


fs = FastapiSettings()
ps = ProjectSettings()
