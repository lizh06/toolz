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

def effect(f, name=None, queue=None):
    # wraps f
    def run():
        # cleanup
        stack.append(run)
        try: f()
        finally: stack.pop()
    # who run?
    run()

def memo(f):
    state, listeners = [None], set()
    def get():
        l = caller()
        if l: listeners.add(l)
        return state[0]
    def run():
        stack.append(run)
        try: state[0] = f()
        finally: stack.pop()
        for l in listeners: l()
    run()
    return get

def signal(value):
    state, listeners = [value], set()
    def get():
        l = caller()
        if l: listeners.add(l)
        return state[0]
    def put(value):
        state[0] = value
        for l in listeners: l()
    return get, put

