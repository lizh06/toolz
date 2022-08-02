from blades import *

# dispatch

def _start(blade, **config):
    if issubclass(blade, Blade):
        blade = blade()
    elif not isinstance(blade, Blade):
        raise Exception()
    blade.start(**config)
    return blade

_kernels = dict(
    cmd = ShellCmd(),
    shell = _start(Shell),
    python = _start(Python),
    py = Formula(),
)

def execute(lang, src, call):
    b = _kernels[lang]
    r = b(src, call)
    print('<-', r)
    print('<- ctx', b.ctx)
    print('<- call', call)

# topo-order

def need_to_run(book, index=-1):
    if index >= 0:
        raise NotImplemented()
    return book['cells']

if __name__ == '__main__':

    import tomli

    with open('cells.toml', 'rb') as f:
        book = tomli.load(f)

    print(book)

    call = {}

    for cell in need_to_run(book):
        print('>', cell)
        lang = cell.get('lang', 'python')
        execute(lang, cell['code'], call)
        # break

    print(call)

# NB
#   notebook is a collection of cells
#   runner is a notebook's running context, so r = Runner(notebook)
#   engine starts / contains many blades
#   runner.engine = default_engine
#   blade identity
#       owned or shared
#       venv-name:
#       skillset: pandas
#       color: cds BASKET
#       affinity: credit with cds curves
#       capacity: min, max
