import contextlib
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

def activate_first(base, venvs):
    for v in venvs:
        d = base / v
        if d.exists():
            activate(d)
            return v

@contextlib.contextmanager
def sys_path_scope():
    saved, changed = list(sys.path), []
    yield changed
    if changed:
        sys.path[:] = saved

@contextlib.contextmanager
def sys_path_prepend(changes):
    if isinstance(changes, Path):
        changes = [str(changes)]
    elif isinstance(changes, str):
        changes = [changes]
    saved = list(sys.path)
    # print(changes + saved)
    sys.path[:] = changes + saved
    yield
    sys.path[:] = saved

def uniqa(i, key=None, return_none=False, return_empty=False):
    key = key or repr
    seen = set()
    for x in i:
        if x is None and not return_none: continue
        if not x and not return_empty: continue
        k = key(x)
        if k not in seen:
            seen.add(k)
            yield x

let = lambda *va: va[-1](*va[:-1])
