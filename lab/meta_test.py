import sys
# import importlib.metadata as meta
import importlib_metadata as meta

eps = meta.entry_points()
print(type(eps))
print('----')
for k in eps.keys():
    print(k)
print('----')
# for x in eps.get('console_scripts', []):
for x in eps.get('markdown.extensions', []):
    try:
        # print(x, x.load())
        print(x)
    except Exception as e:
        print(f'failed to load {x}', e)
print('----')

import sys

for p in sys.meta_path:
    print(p)
