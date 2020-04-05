import re
from typing import Mapping

import chardet
from jsonpath import jsonpath
from jsonschema import validate
from lxml import etree


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


def find_by_jsonpath(field, expr):
    return jsonpath(field, expr)


def find_by_re(text, expr):
    return re.findall(expr, text)


def find_by_xpath(text, expr):  # html
    root = etree.HTML(text)
    return root.xpath(expr)  # todo text


def verify_by_expr(self, operator, expr, expect_value):  # expr: content.url
    pass


def verify_by_schema(field, schema):
    if field is None:
        return validate(field, schema=schema)


def double_split(line, sep1, sep2):
    result = []
    for item in line.split(sep1):
        if sep2 in item:
            key, value = [i.strip() for i in item.split(sep2, 1)]
        else:
            key, value = item.strip(), ''
        result.append((key, value))

    return result


def double_pack(fields: list, sep1, sep2):
    items = []
    for key, value in fields:
        items.append('%s%s%s' % (key, sep2, value))
    return sep1.join(items)


def parse_cookies(line):
    result = double_split(line, ';', '=')
    key, value = result.pop(0)
    # item = dict(key=key, value=value)
    # item.update(result)
    # return key, item
    return key, value


def pack_cookies(cookies):
    return double_pack(cookies, '; ', '=')
