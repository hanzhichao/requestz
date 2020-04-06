import re
import logging
from typing import Mapping
from functools import wraps

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
    return re.findall(expr, text, re.MULTILINE)


def find_by_xpath(text, expr):  # html
    root = etree.HTML(text)
    return root.xpath(expr)  # todo text


def verify_by_expr(self, operator, expr, expect_value):  # expr: content.url
    pass


def verify_by_schema(field, schema):
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


# 装饰器
def params_check(*self, args=None, kwargs=None):
    def _check_type(func):
        @wraps(func)
        def inner(*func_args, **func_kwargs):
            if args:
                for index, _type in enumerate(args):
                    try:
                        func_arg = func_args[index]
                    except Exception as ex:
                        logging.exception(ex)
                        continue

                    if not isinstance(func_arg, _type):
                        raise TypeError(f"函数: {func.__name__} 参数:{func_arg} 必须为 {_type} 类型")
            if kwargs:
                for kwarg, _type in kwargs.items():
                    func_kwarg = func_kwargs.get(kwarg, 'NOTHISKEY')
                    if func_kwargs == 'NOTHISKEY':
                        continue
                    if not isinstance(locals().get(func_kwarg), _type):
                        raise TypeError(f"函数: {func.__name__} 参数:{func_kwarg} 必须为 {_type} 类型")
            return func(*func_args, **func_kwargs)
        return inner
    return _check_type


def type_check(value, types):
    if not isinstance(value, types):
        raise TypeError(f'value: {value} must be in type {types}')
