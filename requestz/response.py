import json
import re

import chardet
from jsonpath import jsonpath
from jsonschema import validate
from lxml import etree

class Response(object):
    def __init__(self):
        self.request = None
        self.content = None
        self.elapsed = None
        self.status_code = None
        self.reason = None
        self.headers = None
        self.encoding = None
        self.url = None

        self.stats = {}

    @property
    def apparent_encoding(self):
        return chardet.detect(self.content)['encoding']

    @property
    def text(self):
        return self.content.decode(self.encoding or 'utf-8')

    def json(self, *kwargs):
        try:
            return json.loads(self.text, **kwargs)
        except json.decoder.JSONDecodeError:
            print(f'响应非JSON格式: {self.text}')
            return {}

    def find_by_jsonpath(self, expr):
        return jsonpath(self.json(), expr)

    def find_by_re(self, expr):
        return re.findall(expr, self.text)

    def find_by_xpath(self, expr):  # html
        root = etree.HTML(self.text)
        return root.xpath(expr)  # todo text

    def verify_by_expr(self, operator, expr, expect_value):  # expr: content.url
        pass

    def verify_by_schema(self, schema, field=None):
        if field is None:
            return validate(self.json, schema=schema)