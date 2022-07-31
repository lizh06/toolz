import re
from subprocess import PIPE, Popen, run
from select import select

class Blade:
    def __init__(self): self._ctx = {}
    ctx = property(lambda a: a._ctx)
    def start(self, **config): pass
    def shutdown(self): pass

def _start(blade, **config):
    if issubclass(blade, Blade):
        blade = blade()
    elif not isinstance(blade, Blade):
        raise Exception()
    blade.start(**config)
    return blade

def _lines(s):
    for l in s.splitlines():
        yield l.strip()

class ShellCmd(Blade):
    def __call__(self, src, call=None):
        proc = run(src, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        res = dict(
            rc = proc.returncode,
            out = list(_lines(proc.stdout.decode())),
            err = list(_lines(proc.stderr.decode())),
        )
        if call is not None: call['res'] = res
        return res

def _read(fd, num):
    s = fd.read1().decode()
    # print('read', num, s)
    return s

def _write(fd, s):
    print('>', s)
    fd.write(s.encode())
    fd.flush()

_EOC_RE = re.compile('-= (\d+) =-$')

class Shell(Blade):
    def start(self):
        self.proc = Popen(['/bin/bash', '-l'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    def __call__(self, src, call=None):
        proc = self.proc
        print('shell', proc.pid, src)
        cmd = f'{src}; echo -= $? =-\n'
        _write(proc.stdin, cmd)
        fds = [proc.stdin, proc.stdout, proc.stderr]
        res, more = [proc.poll(), [], []], True
        while more:
            rds = select(fds[1:], [], [])[0]
            print('ready', [fds.index(_) for _ in rds])
            for fd in rds:
                i = fds.index(fd)
                s = _read(fd, i)
                m = _EOC_RE.search(s)
                if m:
                    res[0] = int(m.group(1))
                    s = s[:m.start()]
                    if s: res[i].append(s)
                    more = False
                else:
                    res[i].append(s)
        return res

# streaming between process from (even) different machines
class Pipe: pass

# why??
class API(Blade): pass

class Formula(Blade):
    def __call__(self, src, call=None):
        if isinstance(src, str):
            src = src.splitlines()
        code = 'def _fn():\n{}\n_x=_fn()'.format('\n'.join(f'\t{_}' for _ in src))
        res = {}
        exec(code, self.ctx, res)
        del self.ctx['__builtins__']
        if call is not None: call['res'] = res
        return res

from jinja2 import Template
from jinja2schema import infer

# def blade(code, ctx):
#     print(infer(code))
#     meta = infer(code)
#     print(meta)
#     print(type(meta['dir']), meta['dir'])
#     cmds = Template(code).render(**ctx)
#     # TODO multiple lines
#     return exchange(cmds)

if __name__ == '__main__':

    blades = dict(
        shell = _start(Shell),
        cmd = ShellCmd(),
        python = Formula(),
        py = Formula(),
    )

    import tomli

    with open('cells.toml', 'rb') as f:
        conf = tomli.load(f)

    call = {}
    for cell in conf['cells']:
        print('>', cell)
        b = blades[cell['lang']]
        r = b(cell['code'], call)
        print('<-', r)
        print('<- ctx', b.ctx)
        print('<- call', call)

    print(conf); quit()
