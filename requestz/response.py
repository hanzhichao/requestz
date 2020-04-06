import json
import gzip
import logging

import chardet
from logz import log as logging

from requestz.utils import parse_cookies, params_check, find_by_re, find_by_jsonpath, find_by_xpath, verify_by_schema, type_check
from requestz.structure import CaseInsensitiveDict

class Response(object):
    def __init__(self):
        self.request = None
        self.url = None

        self.status_code = None
        self.reason = None
        self.encoding = 'utf-8'
        self.headers = CaseInsensitiveDict()
        self.cookies = {}
        self.elapsed = None
        self.raw = None

        self.stats = {}

    def __repr__(self):
        return f'<Response {self.status_code}: {self.url}>'

    def handle_header_line(self, line: bytes):
        """处理pycurl每一行的响应头"""
        try:
            line = line.decode('utf-8').strip()
        except:
            line = line.decode('iso-8859-1').strip()
        if not line:
            return

        if line.startswith('HTTP/'):   # HTTP2
            try:
                _, _, reason = line.split()
                self.reason = reason
            except Exception as ex:
                logging.warning(f'line: {line} 中没有reason')
            return

        name, value = [item.strip() for item in line.split(':', 1)]
        if name.lower() == 'set-cookie':
            key, item = parse_cookies(value)
            self.cookies[key] = item

        if name in self.headers:
            if not isinstance(self.headers[name], list):
                self.headers[name] = [self.headers[name]]
            self.headers[name].append(value)
        else:
            self.headers[name] = value

    @property
    def apparent_encoding(self):
        return chardet.detect(self.content)['encoding']

    @property
    def content(self):
        if 'gzip' in self.headers.get('Content-Encoding', ''):  # todo case in sensitive
            return gzip.decompress(self.raw)
        else:
            return self.raw

    @property
    def text(self):
        self.encoding = self.apparent_encoding or 'utf-8'
        try:
            return self.content.decode(self.encoding)
        except:
            return self.content.decode('iso-8859-1')

    def json(self, **kwargs):
        try:
            return json.loads(self.text, **kwargs)
        except json.decoder.JSONDecodeError:
            logging.error(f'响应非JSON格式: {self.text}')
            return {}

    @params_check(args=(object, str,))
    def find(self, expr, by=None, one=True):
        if by == 'xpath' or expr.startswith('/'):
            results = find_by_xpath(self.text, expr)
        elif by == 'jsonpath' or expr.startswith('$.'):
            results = find_by_jsonpath(self.json(), expr)
        else:
            results = find_by_re(self.text, expr)

        if one and isinstance(results, list) and len(results) > 0:
            return results[0]
        return results

    @params_check(args=(object, dict,))
    def check(self, schema, expr=None):
        field = self.find(expr) or {} if expr else self.json()
        try:
            verify_by_schema(field, schema)
            return True
        except Exception as ex:
            logging.exception(ex)
            return False




