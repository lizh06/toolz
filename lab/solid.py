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

class Memo:
    def __init__(self, f):
        self.state = None
        self.listeners = set()
        def run():
            stack.append(run)
            try: self.state = f()
            finally: stack.pop()
            for l in self.listeners:
                l()
        run()
    def __call__(self):
        l = caller()
        if l: self.listeners.add(l)
        return self.state

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

class Signal:
    def __init__(self, value):
        self.state = value
        self.listeners = set()
    def __call__(self):
        l = caller()
        if l: self.listeners.add(l)
        return self.state
    def set(self, value):
        self.state = value
        for l in self.listeners: l()

# only change
# history length
def signal(value, diff=None):
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

