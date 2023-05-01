from typing import Optional
try:
    from enum import StrEnum
except:
    from strenum import StrEnum
import caseconverter as cc
import msgspec as ms
import itertools as _i

opt = Optional

class TypeCode:
    def __init__(self, **kw):
        self._map = {}
        for k, v in kw.items():
            self.rename(k, v)
    def rename(self, cls, name):
        if type(cls) == type:
            k = cls.__name__
        else: k = cls
        self._map[k] = name
    def __call__(self, name):
        k = self._map.get(name, name)
        return k.lower()
type_code = TypeCode(DbSchema='Schema')

class Struct(ms.Struct, kw_only=True, omit_defaults=True):
    pass

class FieldRef(Struct):
    model: str
    field: opt[str] = None
    def set_field(self, name):
        self.field = name
    def __repr__(self):
        return '.'.join([
            self.model,
            self.field if self.field else 'pk'
        ])
    def __str__(self):
        return f'[{repr(self)}]'

class ForeignKey(Struct):
    on: FieldRef
    to: FieldRef
    def __str__(self):
        return f'[{self.on!r} -> {self.to!r}]'

class Link(Struct):
    name: str
    backprop: opt[str] = None
    back: opt[str] = None # back from fk
    to: opt[str] = None   # to pk
    # fkey: opt[str] = None # to (Model) or via (local fk)
    on__: opt[ForeignKey] = None
    to__: opt[ForeignKey] = None

class Field(Struct):
    name: str
    type: opt[str] = None
    to: opt[str] = None
    primary_key: opt[bool] = None
    nullable: opt[bool] = None

class Model(Struct):
    name: str
    fields: opt[list[Field]] = []
    links: opt[list[Link]] = []
    base: opt[str] = None
    # pk: opt[str] = None

    implied__: list[Field] = []
    on__: list[ForeignKey] = []
    to__: list[ForeignKey] = []
    pk__: list[Field] = []

    def fkeys(self):
        res = []
        for x in self.fields:
            if x.fkey:
                res.append(x)
        return res

    @property
    def implied_fields(self):
        return attr(self, 'implied')

    @property
    def all_fields(self):
        return list(_i.chain(self.fields, self.implied_fields))

class Domain(Struct):
    models: opt[list[Model]] = None
    fk__: list[ForeignKey] = []

def prepare(dom):
    models = {}
    models.update((m.name, m) for m in dom.models)

    for m in dom.models:
        pk = [f for f in m.fields if f.primary_key]
        if pk:
            m.pk__ = pk
        else:
            f = Field('pk')
            m.implied__.append(f)
            m.pk__ = [f]

    for m in dom.models:
        on = []
        for f in m.fields:
            if f.to:
                ref = field_ref(f.to)
                fk = ForeignKey(FieldRef(m.name, f.name), ref)
                on.append(fk)
                print(f'add local fk {fk}')
        if on: m.on__ = on

    for m in dom.models:
        for l in m.links:
            if l.back:
                on = field_ref(l.back)
                if m.name != on.model:
                    fk = ForeignKey(on, FieldRef(m.name))
                else:
                    raise Exception()
                print(f'ensure fk {fk} is on {fk.on.model}')
            elif l.to:
                to = field_ref(l.to)
                if m.name != to.model:
                    fk = ForeignKey(FieldRef(m.name), to)
                else:
                    raise Exception()
                print(fk)
            # print(f'fk: {fk.on} -> {fk.to}')

            # ref = field_ref(l.fkey)
            # if m.name == ref.model:
            #     l.on__ = fk = ForeignKey(FieldRef(m.name), ref)
            # else:
            #     l.to__ = fk = ForeignKey(ref, FieldRef(m.name))
            # print(f'fk: {fk.on} -> {fk.to}')
            # # get to.pk

meta = {}

def metakey(x):
    # return x if isinstance(x, type) else x.__class__
    return x.name

def metainfo(x):
    k = metakey(x)
    mod = meta.get(k)
    if mod is None:
        meta[k] = mod = {}
    return mod

def attr(x, name):
    mod = metainfo(x)
    res = mod.get(name)
    if res is None:
        mod[name] = res = []
    return res

def field_ref(fkey):
    try: tab, col = fkey.split('.')
    except: tab, col = fkey, None
    return FieldRef(tab, col)

def imply_0(x):
    if not x.links: return
    print('--- 0 ---')
    mod = metainfo(x)
    for l in x.links:
        ref = field_ref(l.fkey)
        if x.name == ref.model:
            l.on__ = fk = ForeignKey(FieldRef(x.name), ref)
        else:
            l.to__ = fk = ForeignKey(ref, FieldRef(x.name))
        print(f'fk: {fk.on} -> {fk.to}')
        # get to.pk

def imply_1(x):
    print('--- 1 ---')
    pk = [f for f in x.fields if f.primary_key]
    if pk:
        x.pk__ = pk
    else:
        f = Field('pk')
        x.implied__.append(f)
        x.pk__ = [f]
    on = []
    for f in x.fields:
        if f.to:
            ref = field_ref(f.to)
            fk = ForeignKey(FieldRef(x.name, f.name), ref)
            on.append(fk)
    if on: x.on__ = on

    mod = metainfo(x)
    # print(pk)
    if pk: mod['pk'] = pk
    else:
        attr(x,'implied').append(Field('pk'))

def load_current(test):
    with open(f'{test}.yaml.in', 'rb') as f:
        return ms.yaml.decode(f.read(), type=Domain)

test = 'model1'

if 1:
    dom = load_current(test)
    # print(dom)

else:
    conn = Model('Connecion', fields=[
        Field('name'),
        Field('conn_type'),
        Field('token'),
        Field('url'),
    ])
    ds = Model('Dataset', fields=[
        Field('name'),
        Field('ds_type'),
    ])
    s = Model('Schema', base='Dataset', fields=[
        Field('source_id', fkey='Connection.pk')
    ], links=[
        Link('conn', fkey='Connection', back='datasets'),
    ])
    db = [conn, ds, s]
    dom = Domain(models=db)

    with open('model.yaml', 'wb') as out:
        out.write(ms.yaml.encode(dom))
        print(dom)

prepare(dom)

with open('full_model.yaml', 'wb') as out:
    out.write(ms.yaml.encode(dom))
# print(meta)
quit()

for m in dom.models:
    imply_0(m)

# 1
for m in dom.models:
    imply_1(m)

for m in dom.models:
    print('**', m)
    # print(m.fkeys())
    for f in m.all_fields:
        print(f)
