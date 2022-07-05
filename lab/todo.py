import time

def compute(x):
    response = expensive_call()
    return response + x

def expensive_call():
    time.sleep(3)
    return 123

class Coll:
    def __init__(self):
        self._coll = []
    def __call__(self):
        return self._coll
    def __iadd__(self, x):
        pass
    def insert(self, x):
        self._coll.append(x)
        res = self.reducer(self.ctx, dict(action='insert', data=x))
        if res is not None:
            self.ctx = res
    def update(self, x):
        pass
    def delete(self, x):
        pass

class Item:
    def delete(self):
        pass

class ItemHandler:

    @property
    def monitors(self):
        self.ctx

    @property
    def name(self):
        return self.ctx.name

    def key(self):
        pass


import collections as _c

Action = _c.namedtuple('Action', ['type', 'data'])
# a = Action('add', 1)
# print(a); quit()

def combine_reducers(**kw):
    slices = dict(**kw)
    def _(state, action):
        if state is None: state = {}
        for k, r in slices.items():
            s1 = r(state.get(k), action)
            if s1 is not None:
                state[k] = s1
        return state
    return _

def compose_reducers(*va):
    def _(state, action):
        s = state
        for r in va:
            s1 = r(s, action)
            if s1 is not None:
                s = s1
        return s
    return _

def str_concat(s, action):
    if s is None: s = ''
    if action['type'] == 'add':
        s = f'{s} {action["data"]}'
    return s

def int_concat(s, action):
    if s is None: s = 0
    if action['type'] == 'add':
        s += action['data']
    return s

c = combine_reducers(s=str_concat, i=int_concat)
c1 = compose_reducers(str_concat, int_concat)
c = c1

s = c(None, dict(type='add', data=3))
s = c(s, dict(type='add', data=10))
print(s); quit()

def dict_reducer(key=None, cls=None):
    key = key if callable(key) else lambda x: x
    cls = cls if callable(cls) else dict
    def _(state, action):
        if state is None: state = cls()

        k = key(action.data)
        if action.type == 'insert':
            if k in state:
                raise Exception(f'{k} already exist')
            state[k] = action.data
        elif action.type == 'update':
            if k in state:
                state[k].update(action.data)
            raise Exception(f'{k} does not exist')
        elif action.type == 'upsert':
            if k in state:
                state[k].update(action.data)
            else:
                state[k] = action.data
        else:
            raise Exception(f'unknown action type {action.type}')
        return state

def list_reducer(key=None, cls=None):
    key = key if callable(key) else lambda x: x
    cls = cls if callable(cls) else list
    def _(state, action):
        if state is None: state = cls()

        k = key(action.data)
        if action.type == 'insert':
            for x in state:
                if key(x) == k:
                    raise Exception('already exist')
            state.append(action.data)
        elif action.type == 'update':
            for x in state:
                if key(x) == k:
                    x.update(action.data)
                    return state
            raise Exception(f'{k} does not exist')
        elif action.type == 'upsert':
            for x in state:
                if key(x) == k:
                    x.update(action.data)
                    return state
            state.append(action.data)
        else:
            raise Exception(f'unknown action type {action.type}')
        return state


def reducer(key=None, init=None):
    key = key if callable(key) else lambda x: x
    init = init if callable(init) else list
    keys, data = init(), init()
    def _(state, action):
        if state is None: state = init()

def coll_reducer(state, action):
    if state is None:
        state = []
    k = mykey(action.data)
    if action.type == 'insert':
        for x in state:
            if mykey(x) == k:
                raise Exception('already exist')
        state.append(action.data)
    elif action.type == 'update':
        for x in state:
            if mykey(x) == k:
                x.update(action.data)
                return state
        raise Exception(f'{k} does not exist')
    elif action.type == 'upsert':
        for x in state:
            if mykey(x) == k:
                x.update(action.data)
                return state
        state.append(action.data)
    else:
        raise Exception(f'unknown action {action}')
    return state

# coll['a'].monitors.insert(dict(in=3, rr=1))

# apps = coll(keyfun, ItemHandler)
# apps.insert({})
# apps.update({})
# apps.upsert({})
