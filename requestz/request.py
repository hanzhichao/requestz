import io
import json as pyjson
from typing import Mapping, Union
from urllib.parse import quote, urlencode, urlparse, urlunparse

from requestz.utils import pack_cookies, type_check


class Request(object):
    """处理请求参数"""

    def __init__(self):
        self.method = None
        self.url = None
        self.headers = {}
        self.files = None
        self.body = None

    def prepare(self, method: str = None, url: str = None, headers: dict = None, cookies: dict = None,
                params: dict = None, data: Union[dict, str, bytes] = None, json: dict = None, files: dict = None,
                auth=None, hooks=None):

        self.prepare_url(url, params)
        self.prepare_body(data, files, json)
        self.prepare_headers(headers, cookies)  # 需要在prepare_body后面
        self.prepare_method(method)  # 需要在prepare_body后面
        return self

    def prepare_method(self, method: str) -> None:
        """
        Uppercase method name.
        :param method: HTTP method
        :return:
        """
        self.method = method.upper() if method else 'POST' if self.body else 'GET'

    def prepare_url(self, url: str, params: Union[dict, list, tuple]):
        """
        Handle url
        :param url:
        :param params:
        :return:
        """
        # 处理url
        type_check(url, str)
        # if not isinstance(url, str):
        #     raise TypeError(f'url: {url} 应为字符串')

        result = urlparse(url=url, allow_fragments=True)
        query = result.query

        # 处理params
        if params:
            type_check(params, (dict, list, tuple))
            # if not isinstance(params, (dict, list, tuple)):
            #     raise TypeError(f'params: {params} 只支持dict,list,tuple格式')
            if isinstance(params, dict):
                params = params.items()
            params_list = ['='.join(item) for item in params]  # todo
            extra_query = '&'.join(params_list)
            query = '&'.join([query, extra_query]).strip('&')

        if not query:
            self.url = url
        else:
            result = list(result)
            params = []
            for item in query.split('&'):
                item = item.split('=')
                params.append(f'{item[0]}={quote(item[1])}')
            result[4] = '&'.join(params)
            self.url = urlunparse(result)

    def prepare_headers(self, headers: Union[dict, list, tuple], cookies: Union[dict, list, tuple]):
        """
        Handle the request headers.
        :param headers:
        :param cookies:
        :return:
        """
        if not headers and not cookies:
            return
        type_check(headers, (dict, list, tuple))
        # if not isinstance(headers, (dict, list, tuple)):
        #     raise TypeError(f'headers: {headers} 只支持dict,list,tuple格式')

        # 处理cookies
        if cookies:
            type_check(cookies, (dict, list, tuple))
            # if not isinstance(cookies, (dict, list, tuple)):
            #     raise TypeError(f'cookies: {cookies} 只支持dict,list,tuple格式')
            if isinstance(cookies, Mapping):
                cookies = cookies.items()
            cookies = pack_cookies(cookies)
            print('cookies', cookies)
            headers['Cookie'] = cookies  # FIXME 只支持headers为字典格式

        if isinstance(headers, Mapping):
            headers = headers.items()

        self.headers = [': '.join(item) for item in headers]  # todo

    def prepare_body(self, data: Union[Mapping, str, io.TextIOWrapper, io.BufferedReader],
                     files: dict,
                     json: Union[dict, list] = None) -> None:
        """
        Handler the request body.
        :param data:
        :param files:
        :param json:
        :return:
        """
        body = None

        if data is not None:
            type_check(data, (Mapping, str, io.TextIOWrapper, io.BufferedReader))
            # if not isinstance(data, (Mapping, str, io.TextIOWrapper, io.BufferedReader)):
            #     raise TypeError(f'data: {data} 只支持dict, str, io.TextIOWrapper, io.BufferedReader格式')

            if isinstance(data, (Mapping, list, tuple)):
                self.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
                body = urlencode(data)
            else:
                body = data
        elif files is not None:
            self.headers.update({'Content-Type': 'multipart/form-data'})
            self.files = files

        elif json is not None:
            self.headers.update({'Content-Type': 'application/json'})
            body = pyjson.dumps(json, ensure_ascii=True).encode('ascii')

        self.body = body
