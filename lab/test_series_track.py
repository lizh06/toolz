class NameVer(tuple):
    def rename(self, new, old=None):
        if old is not None and self[0] != old:
            raise ValueError(f"Cannot rename '{self}' from '{old}' -> '{new}'")
        return NameVer((new, self[-1]))
    def update(self, new=None, old=None):
        if new is not None:
            ver = self.rename(new, old)
        else: ver = self
        return NameVer((ver[0], ver[-1]+1))
    def __repr__(self):
        return '{}-{}'.format(*self)
    __str__ = __repr__

# changes = [
#     lambda ver: ver.rename('t', 'a'),
#     lambda ver: ver.update(),
#     lambda ver: ver.rename('x', 't'),
#     lambda ver: ver.update('y'),
#     lambda ver: ver.rename('t'),
# ]
# ver = NameVer(('a', 0)); print(ver)
# for c in changes:
#     ver = c(ver)
#     print(ver)
# quit()

class Column:
    def __init__(self, name):
        self.hist = [NameVer([name, 0])]
    @property
    def latest(self):
        return self.hist[-1]
    def name(self, index):
        pass
    def rename(self, new, old=None):
        ver = self.latest.rename(new, old)
        self.hist.append(ver)
        return ver
    def update(self, new=None, old=None):
        ver = self.latest.update(new, old)
        self.hist.append(ver)
        return ver
    def __str__(self):
        return str(self.hist)

class Frame(tuple):
    @property
    def data(self):
        return self[0]
    @property
    def meta(self):
        return self[-1]

# meta:
#     name -> (namever, index, colinfo)

def rename_col(from_, to):
    def t(frame):
        data, meta = frame
        col = meta[from_]
        col.rename(to)
        new_meta = {c: col for c, col in meta.items() if c != from_}
        new_meta[to] = col
        return Frame([object(), new_meta])
    return t

def delete_outliers(irrelevant_col_name=None):
    def t(frame):
        data, meta = frame
        for col in meta.values():
            col.update()

        new_meta = meta

        # col = meta[name]
        # col.change_data()
        # new_meta = {c: col for c, col in meta.items() if c != name}
        # new_meta[name] = col

        return Frame([object(), new_meta])
    return t

def append_new_column(new, irrelevant_args=None):
    def t(frame):
        data, meta = frame
        Column(new)
        return Frame([object(), meta])
    return t

data = object()
cols = 'a b c'.split()
meta = {c: Column(c) for c in cols}
frame = Frame([data, meta])
frame_hist = [frame]

changes = [
    delete_outliers(),
    rename_col('a', 'a1'),
    append_new_column('x'),
]

for t in changes:
    frame_hist.append(t(frame_hist[-1]))

print(frame_hist); quit()

print(frame)

model = [{'ver':0,'name':c} for c in frame]
print(model)
