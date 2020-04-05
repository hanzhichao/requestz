from typing import Mapping


def ensure_dict(field):
    if isinstance(field, Mapping):
        return field
    try:
        return dict(field)
    except Exception as ex:
        raise TypeError('{current}无法转为字典格式')


def merge_dict(current, new):
    if not new:
        return current
    if not current:
        return new

    current,new = ensure_dict(current), ensure_dict(new)

    current = current.copy()
    current.update(new)

    return current