from requestz.structure import DotDict, CaseInsensitiveDict, SameKeysDict


def test_dot_dict():
    d = DotDict({'a': 1, 'b': 2})
    print(d.a)


def test_case_insensitive_dict():
    d = CaseInsensitiveDict({'a': 1, 'b': 2})
    assert d['A'] == 1
    assert d.get('A') == 1
    assert d.get('C') is None
    d.update({'c': 3})
    assert d.get('C') == 3
    assert d == {'a': 1, 'b': 2, 'c': 3}


def test_same_key_dict():
    d = SameKeysDict({'a': 1, 'b': 2})
    d['a'] = 2
    print()
    print(d['a'])


def test_same_key_dict_init_with_tuple():
    d = SameKeysDict([('a', 1), ('a', 2), ('b', 2)])
    print(d['a'])


def test_same_key_dict_update():
    d = SameKeysDict({'a': 1, 'b': 2})
    d.update({'a': 3, 'b': 4})
    assert d.get('a') == [1, 3]