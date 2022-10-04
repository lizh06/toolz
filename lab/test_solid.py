import inspect
from f2 import let

from solid import effect, memo, signal

flag, flag_set = signal(False)
base, base_set = signal(100)
count, count_set = signal(0)
total = memo(lambda: base() + count())

def test_a():
    pass

conf = '''
process: echo-service
count: 5
'''

def process():
    pass

def x():
    _(lambda: print(1))
    _(lambda: print(2))

def echo():
    # print('---')
    if flag():
        print(f'{count()}')
    else:
        print('hi')

print('---')
# effect(echo)
effect(lambda: let(f'{count()}' if flag() else 'hi', print))
effect(lambda: print(f'total: {total()}'))
print('---')
count_set(1)
print('---')
flag_set(True)
print('---')
count_set(2)
print('---')
flag_set(False)
