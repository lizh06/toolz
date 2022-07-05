from jinja2 import Template
import tomli
import yaml

from shell import bash_blade

setup = yaml.safe_load('''
lang: python
code: dir = '$temp'
''')

todo = yaml.safe_load('''
lang: bash
code: ls {{dir}}
''')

run_path = tomli.loads('''
lang = "bash"
code = "which run"
[[inputs]]
a = 'int'
''')
# print(run_path); quit()

cells = [setup, todo, run_path]
cells = [todo, run_path]

def blade_python():
    def blade(code, ctx):
        # TODO change ctx to compile-time context
        cmds = Template(code).render(**ctx)
        # TODO last expression
        exec(cmds, {}, ctx)
    return blade

blades = dict(
    bash=bash_blade,
    python=blade_python,
)

def run(cells, ctx):
    for c in cells:
        blade = blades[c['lang']]()
        r = blade(c['code'], ctx)
        print(r)

ctx = dict(
    dir='/var'
)
# ctx = dict()

res = run(cells, ctx)
print(res)
quit()

# TODO
#
# 1. local, global vars
# 2. wait across blades
# 3. py express format
# 4. pye importer

@cell(needs=[])
def setup():
    dir: str = '$temp'
    df: Frame

### @name: setup
dir: str = '$temp'

'''!bash
@type dir: str
@needs dbau_module
@name ls
ls {{dir}}
'''

###! cell
dir = '$temp'

'''!bash
ls {{dir}}
'''
