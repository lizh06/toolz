from pathlib import Path
import os
import site
import sys

def activate(base):
    if not isinstance(base, Path):
        base = Path(base)
    if sys.platform != 'win32':
        bin, lib = 'bin', f'lib/python{sys.version[:3]}'
    else:
        bin, lib = 'Scripts', 'Lib'
    os.environ['PATH'] = os.pathsep.join(
        [str(base / bin)] + os.environ.get('PATH','').split(os.pathsep))
    os.environ['VIRTUAL_ENV'] = str(base)
    prev_sys_path = list(sys.path)
    # print('site', base / lib / 'site-packages')
    site.addsitedir(base / lib / 'site-packages')
    sys.real_prefix = sys.prefix
    sys.prefix = base
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path

def activate_all(base):
    for v in ['venv-local', 'venv']:
        d = base / v
        if d.exists():
            activate(d)
            return True
    return False

let = lambda *va: va[-1](*va[:-1])
