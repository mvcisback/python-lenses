import collections

import pytest

import lenses.setter as s


def test_setitem_imm_custom_class():
    class C:
        def __init__(self, item):
            self.item = item

        def __eq__(self, other):
            return self.item == other.item

        def _lens_setitem(self, key, value):
            return C(value)

    assert s.setitem_immutable(C(1), 0, 2) == C(2)


def test_setitem_imm_list():
    assert s.setitem_immutable([1, 2, 3], 0, 4) == [4, 2, 3]


def test_setitem_imm_tuple():
    assert s.setitem_immutable((1, 2, 3), 0, 4) == (4, 2, 3)


def test_setattr_imm_custom_class():
    class C:
        def __init__(self, attr):
            self.attr = attr

        def __eq__(self, other):
            return self.attr == other.attr

        def _lens_setattr(self, name, value):
            if name == 'fake_attr':
                return C(value)
            else:
                raise AttributeError(name)

    assert s.setattr_immutable(C(1), 'fake_attr', 2) == C(2)


def test_setattr_imm_custom_class_raw():
    class C:
        def __init__(self, attr):
            self.attr = attr

        def __eq__(self, other):
            return self.attr == other.attr

    assert s.setattr_immutable(C(1), 'attr', 2) == C(2)


def test_setattr_imm_namedtuple():
    Tup = collections.namedtuple('Tup', 'attr')
    assert s.setattr_immutable(Tup(1), 'attr', 2) == Tup(2)


def test_fromiter_custom_class():
    class C:
        def __init__(self, attr):
            self.attr = attr

        def __eq__(self, other):
            return self.attr == other.attr

        def _lens_fromiter(self, iterable):
            return C(next(iter(iterable)))

    assert s.fromiter(C(1), [2]) == C(2)


def test_fromiter_list():
    assert s.fromiter([], (1, 2, 3)) == [1, 2, 3]


def test_fromiter_set():
    assert s.fromiter(set(), [1, 2, 3]) == {1, 2, 3}


def test_fromiter_str():
    assert s.fromiter('hello', ['1', '2', '3']) == '123'


def test_fromiter_tuple():
    assert s.fromiter((), [1, 2, 3]) == (1, 2, 3)


def test_fromiter_unknown():
    with pytest.raises(NotImplementedError):
        s.fromiter({}, [1, 2, 3])
