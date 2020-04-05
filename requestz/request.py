import logging
import json as pyjson
import io
from typing import Mapping
from urllib.parse import quote, urlencode, urlparse, urlunparse, urlsplit

from requestz.utils import pack_cookies

class Request(object):
    """处理请求参数"""
    def __init__(self):
        self.method = None
        self.url = None
        self.headers = {}
        self.body = None

    def prepare(self, method=None, url=None, headers=None,cookies=None, params=None, data=None,json=None,files=None,
                auth=None, hooks=None):

        self.prepare_url(url, params)
        self.prepare_body(data, files, json)
        self.prepare_headers(headers, cookies)  # 需要在prepare_body后面
        self.prepare_method(method)  # 需要在prepare_body后面
        return self

    def prepare_method(self, method):
        self.method = method.upper() if method else 'POST' if self.body else 'GET'

    def prepare_url(self, url, params):
        # 处理url
        if not isinstance(url, str):
            raise TypeError(f'url: {url} 应为字符串')

        result = urlparse(url=url, allow_fragments=True)
        query = result.query

        # 处理params
        if params:
            if not isinstance(params, (dict, list, tuple)):
                raise TypeError(f'params: {params} 只支持dict,list,tuple格式')
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

    def prepare_headers(self, headers, cookies):
        if not headers and not cookies:
            return

        if not isinstance(headers, (dict, list, tuple)):
            raise TypeError(f'headers: {headers} 只支持dict,list,tuple格式')

        # 处理cookies
        if cookies:
            if not isinstance(cookies, (dict, list, tuple)):
                raise TypeError(f'cookies: {cookies} 只支持dict,list,tuple格式')
            if isinstance(cookies, Mapping):
                cookies = cookies.items()
            cookies = pack_cookies(cookies)
            print('cookies', cookies)
            headers['Cookie'] = cookies  # FIXME 只支持headers为字典格式

        if isinstance(headers, Mapping):

            headers = headers.items()

        self.headers = [': '.join(item) for item in headers]  # todo


    def prepare_body(self, data, files, json=None):
        body = None
        if files is not None:
            raise NotImplementedError
        elif data is not None:
            if not isinstance(data, (Mapping, str, io.TextIOWrapper)):
                raise TypeError(f'data: {data} 只支持dict, str, io.TextIOWrapper格式')

            if isinstance(data, (Mapping, list, tuple)):
                self.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
                body = urlencode(data)
                print(body)
            else:
                body = data
        elif json is not None:
            self.headers.update({'Content-Type': 'application/json'})
            body = pyjson.dumps(json, ensure_ascii=True).encode('ascii')

        self.body = body