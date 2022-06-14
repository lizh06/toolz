from todo import compute
from todo import Coll, Item

def test_compute(mocker):
    mocker.patch('todo.expensive_call', return_value=123)
    expected = 124
    actual = compute(1)
    assert expected == actual

def test_init_empty():
    coll = Coll()

    assert coll() == []

def test_add_first_item():
    coll = Coll()
    z = {'name': 'zheng'}

    coll += z
    assert coll() == [z]
