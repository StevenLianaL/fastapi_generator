from pathlib import Path

import plac

from fastapi_generator.config import fs, ps
from fastapi_generator.sub import SubApp


@plac.pos('app_name', "sub app name", type=str)
@plac.pos('api_name', "api name", type=str)
def create_api(sub_app_name, api_name):
    sub_app_dir = Path(fs.sub_app_dir, sub_app_name)
    if not sub_app_dir.exists():
        sub_app = SubApp()
        sub_app.create_app(name=sub_app_name)
    file = Path(sub_app_dir, 'router', f"{api_name}_api").with_suffix('.py')
    text = Path(ps.template_dir, 'api', 'api').read_text(encoding='utf8')
    with file.open(mode='w', encoding='utf8') as w:
        w.write(text)


if __name__ == '__main__':
    plac.call(create_api)
