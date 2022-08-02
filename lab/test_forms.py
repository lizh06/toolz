from jinja2 import Template
from jinja2schema import infer

if __name__ == '__main__':

    import tomli

    with open('forms.toml', 'rb') as f:
        forms = tomli.load(f)

    print(forms)

    for form in forms.items():
        print(form)

    quit()
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

