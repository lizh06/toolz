stack = []

def caller():
    if stack: return stack[-1]
    # how to get caller in python

# [p1, p2]
# [w1, w2, w3]
#
# machine
# process
# service
# proxy
# item
# tag: proxy

def effect(f, name=None):
    # wraps f
    def run(queue=None):
        # cleanup
        stack.append(run)
        try: f()
        finally: stack.pop()
    # who run?
    return run

def task(f):
    def make(*va, **kw):
        def eff():
            stack.append(eff)
            try: f(*va, **kw)
            finally: stack.pop()
        eff()
        # return handle to cancel
    return make

def mem(f):
    def make(*va, **kw):
        state, listeners = [None], set()
        def get():
            l = caller()
            if l: listeners.add(l)
            return state[0]
        def run():
            stack.append(run)
            try: state[0] = f(*va, **kw)
            finally: stack.pop()
            for l in listeners: l()
        run()
        return get
    return make

def memo(f):
    state, listeners = [None], set()
    def get():
        l = caller()
        if l: listeners.add(l)
        return state[0]
    def run(queue=None):
        stack.append(run)
        try: state[0] = f()
        finally: stack.pop()
        for l in listeners: l()
    run()
    return get

# only change
# history length
def slot(value, diff=None):
    state, listeners = [value], set()
    def get():
        l = caller()
        if l: listeners.add(l)
        return state[0]
    def put(value):
        state[0] = value
        for l in listeners: l()
    get.set = put
    return get

# state -> changes
# with debounce

