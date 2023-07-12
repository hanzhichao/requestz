import gzip
import json
import logging
from typing import Union, Optional

from requestz.structure import CaseInsensitiveDict
from requestz.utils import parse_cookies, params_check, find_by_re, find_by_jsonpath, find_by_xpath, verify_by_schema


# import chardet
# from logz import log as logging


class Response(object):
    """Http Response"""

    def __init__(self):
        self.request = None
        self.url = None

        self.status_code = None
        self.reason: Optional[str] = None
        self.encoding: str = 'utf-8'
        self.headers = CaseInsensitiveDict()
        self.cookies = {}
        self.elapsed = None
        self.raw = None

        self.stats = {}

    def __repr__(self):
        return f'<Response {self.status_code}: {self.url}>'

    def handle_header_line(self, line: bytes):
        """
        Handle each response header line.
        :param line: response header line
        :return:
        """
        try:
            line = line.decode('utf-8').strip()
        except:
            line = line.decode('iso-8859-1').strip()
        if not line:
            return

        if line.startswith('HTTP/'):  # HTTP2
            try:
                _, _, reason = line.split()
                self.reason = reason
            except ValueError as ex:
                logging.debug(f'line: {line} 中没有reason')
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
    def apparent_encoding(self) -> str:
        """
        Guess the apparent encoding from the response content
        :return:
        """
        import chardet
        return chardet.detect(self.content)['encoding']

    @property
    def content(self) -> bytes:
        """
        Get the response body raw content.
        :return:
        """
        if 'gzip' in self.headers.get('Content-Encoding', ''):  # todo case in sensitive
            return gzip.decompress(self.raw)
        else:
            return self.raw

    @property
    def text(self) -> str:
        """
        Get the response body as string.
        :return:
        """
        self.encoding = self.apparent_encoding or 'utf-8'
        try:
            return self.content.decode(self.encoding)
        except UnicodeDecodeError:
            return self.content.decode('iso-8859-1')

    def json(self, **kwargs) -> Union[dict, list]:
        """
        JSON response body as dict or list.
        :param kwargs:
        :return:
        """
        try:
            return json.loads(self.text, **kwargs)
        except json.decoder.JSONDecodeError:
            logging.error(f'响应非JSON格式: {self.text}')
            raise
            # return {}

    @params_check(args=(object, str,))
    def find(self, expr: str, by: str = None, one: bool = True):
        """
        Find a value by xpath or jsonpath or regex.
        :param expr: xpath or jsonpath or regex expression
        :param by: xpath or jsonpath or regex
        :param one: return the first value if True
        :return:
        """
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




