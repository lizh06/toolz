import inspect
from f2 import let

from solid import effect, memo, signal

flag = signal(False)
base = signal(100)
count = signal(0)
total = memo(lambda: base() + count())

port = signal(6060)
data_dir = signal('/a/b/c')
# proc.data_dir()
# proc.data_dir.put()

# def start(): return pid
# pid = memo(start)

# hotswap
#   props change -> process restart
#   
# runner for
#   flask
#   tornado

'''
port: 6000
data_dir: /a/b/c
move?
k: str

pid
status: started, up, stopped, closing, down

warnings
failed = signal()
ok = signal()
total = memo(lambda: ok() + failed())

json schema
    name
        fields
    tag
    field

    type
        str|int
        object
        array

    object
        name?

    type str
    type string
    type int
    type array (min, max, elm)
    type alias str = string
    type alias float = number
    type alias double = number
    type alias int = number
    type number

    object:
        name: SomeDef
        props:
            a: string
            b: int
        all_required
'''

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
effect(lambda: let(f'{count()}' if flag() else 'hi', print))()
effect(lambda: print(f'total: {total()}'))()

print('---')
count.set(1)
print('---')
flag.set(True)
print('---')
count.set(2)
print('---')
flag.set(False)
