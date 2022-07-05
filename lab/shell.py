import re
from subprocess import Popen, PIPE
from select import select

from jinja2 import Template
from jinja2schema import infer

class Skill: pass
class Context: pass
class Formula: pass
class Cell: pass
class Book: pass

class Blade: pass
class Bash(Blade):
    pass

env = {}
blades = {}

def ctx_runall():
    for cell in cells:
        blades[cell.blade].run(cell.formula)

def ctx_cell():
    pass

def ctx_run_next():
    pass

def create_blade(kind):
    if kind == 'bash':
        blades['bash'] = Bash(env)

EOC = re.compile('-= (\d+) =-$')

def _read(fd, num):
    s = fd.read1().decode()
    # print('read', num, s)
    return s

def bash_blade():
    proc = Popen(['/bin/bash', '-l'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    fds = [proc.stdin, proc.stdout, proc.stderr]

    print([type(_) for _ in fds])
    print(proc.pid)

    def exchange(line):
        cmd = line or 'exit'
        cmd = f'{cmd}; echo -= $? =-\n'
        print('sending', cmd)
        proc.stdin.write(cmd.encode())
        proc.stdin.flush()
        outs, more = [proc.poll(), [], []], True
        while more:
            rds = select(fds[1:], [], [])[0]
            print('ready', [fds.index(_) for _ in rds])
            for fd in rds:
                i = fds.index(fd)
                s = _read(fd, i)
                m = EOC.search(s)
                if m:
                    s = s[:m.start()]
                    outs[0] = int(m.group(1))
                    more = False
                outs[i].append(s)
        return outs

    def blade(code, ctx):
        print(infer(code))
        meta = infer(code)
        print(meta)
        print(type(meta['dir']), meta['dir'])

        cmds = Template(code).render(**ctx)
        # TODO multiple lines
        return exchange(cmds)

    return blade

def output(rc, out, err):
    print('rc', rc)
    for x in out: print(str(x))
    for x in err:
        for l in x.splitlines():
            print('E', l)

# TODO
#  mixing out, err for logging
#  only whole line is printed

if __name__ == '__main__':
    communicate = bash_blade()

    while True:
        try:
            line = input('>> ').strip()
            if not line: continue
        except EOFError:
            output(*communicate(''))
            break
        output(*communicate(line))
