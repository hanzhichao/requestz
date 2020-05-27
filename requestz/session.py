import logging
import io
import os
import datetime
import socket
import subprocess
import platform
import re
from urllib.parse import quote, urlencode, urlparse, urlunparse, urlsplit
from typing import Mapping

import pycurl
import certifi
from logz import log as logging

from requestz.response import Response
from requestz.request import Request
from requestz.utils import merge_dict, type_check

DEFAULT_REDIRECT_LIMIT = 30
DEFAULT_TIMEOUT = 60
DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/73.0.3683.103 Safari/537.36"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    'Accept-Encoding': ', '.join(('gzip', 'deflate')),
    'Accept': '*/*',
    'Connection': 'keep-alive',
}

REQUEST_KWARGS = dict(params=None, headers=None, cookies=None, data=None, json=None, files=None,timeout=None,
                      verify=None, allow_redirects=None, proxies=None, hooks=None, stream=None, cert=None)


class Session(object):
    def __init__(self):
        self.curl = pycurl.Curl()  # todo session默认配置

        self.base_url = None
        self.headers = DEFAULT_HEADERS
        self.cookies = {}
        self.params = {}

        self.timeout = DEFAULT_TIMEOUT
        self.allow_redirects = True
        self.auth = None
        self.cert = None
        self.trust_env = True
        self.verify = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.curl.close()
        self.curl = None

    def _set_method(self, method):
        if not method:
            return
        logging.debug('设置method:', method)
        try:
            self.curl.setopt(pycurl.CUSTOMREQUEST, method)
        except Exception as ex:
            logging.exception(ex)
            raise ValueError(f'不支持的请求方法 {method}')

    def _set_url(self, url):
        if not url:
            return
        logging.debug(f'设置url: {url}')
        try:
            if not url.startswith('http'):
                if not self.base_url:
                    raise ValueError('url未已http开头,并且base_url未配置')
                else:
                    url = f'{self.base_url}/{url.lstrip("/")}'
            self.curl.setopt(pycurl.URL, url)
        except Exception as ex:
            logging.exception(ex)
            raise ValueError(f'url: {url} 不合法')

    def _set_user_agent(self, user_agent):
        try:
            self.curl.setopt(pycurl.USERAGENT, user_agent)
        except:
            raise ValueError('设置useragent: {value}失败')

    def _set_headers(self, headers):
        if not headers:
            return
        logging.debug(f'设置headers: {headers}')
        if isinstance(headers, Mapping):
            for key, value in headers:
                if key.lower() == 'user-agent':
                    self._set_user_agent(value)
                    break
            headers = headers.items()
        try:
            self.curl.setopt(pycurl.HTTPHEADER, headers)
        except Exception as ex:
            logging.exception(ex)
            raise ValueError(f'headers: {headers} 不合法')

    def _set_upload(self, body):
        type_check(body, (io.TextIOWrapper, io.BufferedReader))
        # if not isinstance(body, (io.TextIOWrapper, io.BufferedReader)):
        #     raise TypeError(f'上传body: {type(body)} 只支持io.TextIOWrapper, io.BufferedReader')
        try:
            self.curl.setopt(pycurl.UPLOAD, 1)
            self.curl.setopt(pycurl.READDATA, body)
        except Exception as ex:
            logging.exception(ex)
            raise ValueError(f'上传body: {body} 不合法')

    def _set_body(self, body):
        if not body:
            return
        logging.debug(f'设置body: {body}')
        if isinstance(body, (io.TextIOWrapper, io.BufferedReader)):
            return self._set_upload(body)

        try:
            self.curl.setopt(pycurl.POSTFIELDS, body)
        except Exception as ex:
            logging.exception(ex)
            raise ValueError(f'body: {body} 不合法')

    def _set_files(self, files):
        if not files:
            return
        type_check(files, dict)
        # if not isinstance(files, dict):
        #     raise TypeError(f'files: {files} 必须为字典格式')
        logging.debug(f'设置files: {files}')
        files_data = []
        for key, value in files.items():
            type_check(value, (str, tuple, list))
            # if not isinstance(value, (str, tuple, list)):
            #     raise TypeError(f'value: {value} 只支持str, tuple, list格式')
            if isinstance(value, str):
                values = [value]
            else:
                values = value
            if len(values) > 1:
                file_path = values[0]
                if not os.path.exists(file_path):
                    raise ValueError(f'文件路径: {value}不存在')
            title = (pycurl.FORM_FILE, pycurl.FORM_FILENAME, pycurl.FORM_CONTENTTYPE)

            files_data.append((key, tuple(zip(title, values))[0]))
        print(files_data)
        try:
            self.curl.setopt(pycurl.HTTPPOST, files_data)
        except Exception as ex:
            logging.exception(ex)
            raise ex
            # raise ValueError(f'value: {value} 不合法')

    def _set_timeout(self, timeout):
        type_check(timeout, (int, float, tuple, list))
        # if not isinstance(timeout, (int, float, tuple, list)):
        #     raise TypeError(f'timeout: {timeout} 只支持int,float, tuple, list格式')
        if isinstance(timeout, (int, float)):
            self.curl.setopt(pycurl.TIMEOUT, timeout)
        if isinstance(timeout, (tuple, list)):
            if len(timeout) < 2:
                raise ValueError(f'timeout: {timeout} 应至少包含两个元素')
            connection_timeout, download_timeout,*_ = timeout
            type_check(connection_timeout, (int, float))
            type_check(download_timeout, (int, float))
            # if not all((isinstance(connection_timeout, (int, float)), isinstance(download_timeout, (int, float)))):
            #     raise TypeError(f'timeout: {timeout} 中前两个元素应为数字类型')
            self.curl.setopt(pycurl.CONNECTTIMEOUT, connection_timeout)
            self.curl.setopt(pycurl.TIMEOUT, download_timeout)  # todo

    def _set_allow_redirects(self, allow_redirects):
        if allow_redirects:
            if not isinstance(allow_redirects, int):
                allow_redirects = DEFAULT_REDIRECT_LIMIT
        try:
            self.curl.setopt(pycurl.FOLLOWLOCATION, True)
            self.curl.setopt(pycurl.MAXREDIRS, allow_redirects)
        except Exception as ex:
            print(f'设置allow_redirects {allow_redirects}失败')

    def _set_verify(self, verify):
        if verify:
            try:
                self.curl.setopt(pycurl.CAINFO, certifi.where())
            except Exception as ex:
                print(f'设置verify {verify}失败')

    def _get_clint_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def _ping(self, domain):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = f'ping {param} 1 {domain}'
        print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.read().decode('utf-8')
        result, *_ = re.findall(r'time=(\d.*)\sms', out, re.M) or ['']
        if result and result.isdigit():
            return float(result)

    def _set_response(self, response):
        response.status_code = self.curl.getinfo(pycurl.HTTP_CODE)
        response.ok = 200 <= response.status_code < 400  # todo
        # response.elapsed = self.curl.getinfo(pycurl.TOTAL_TIME)
        response.client_ip = self._get_clint_ip()  # todo
        response.elapsed = datetime.timedelta(seconds=self.curl.getinfo(pycurl.TOTAL_TIME))

        response.stats['total_time'] = self.curl.getinfo(pycurl.TOTAL_TIME)
        response.stats['namelookup_time'] = self.curl.getinfo(pycurl.NAMELOOKUP_TIME)
        response.stats['connect_time'] = self.curl.getinfo(pycurl.CONNECT_TIME)
        response.stats['pretransfer_time'] = self.curl.getinfo(pycurl.PRETRANSFER_TIME)
        response.stats['starttransfer_time'] = self.curl.getinfo(pycurl.STARTTRANSFER_TIME)
        response.stats['redirect_time'] = self.curl.getinfo(pycurl.REDIRECT_TIME)

        response.stats['ssl_time'] = self.curl.getinfo(pycurl.APPCONNECT_TIME)  # 握手时间
        response.stats['num_connects'] = self.curl.getinfo(pycurl.NUM_CONNECTS)
        response.stats['redirect_count'] = self.curl.getinfo(pycurl.REDIRECT_COUNT)
        response.stats['size_upload'] = self.curl.getinfo(pycurl.SIZE_UPLOAD)
        response.stats['size_download'] = self.curl.getinfo(pycurl.SIZE_DOWNLOAD)
        response.stats['content_length_upload'] = self.curl.getinfo(pycurl.CONTENT_LENGTH_UPLOAD)
        response.stats['content_length_download'] = self.curl.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
        response.stats['speed_upload'] = self.curl.getinfo(pycurl.SPEED_UPLOAD)
        response.stats['speed_download'] = self.curl.getinfo(pycurl.SPEED_DOWNLOAD)

    def send(self, request, timeout=None, verify=None, allow_redirects=None):
        """负责设置pycurl并发送请求,及组装响应"""
        response = Response()
        response.request = request
        response.url = request.url

        self._set_method(request.method)
        self._set_url(request.url)

        self._set_user_agent(DEFAULT_USER_AGENT) # 设置默认User-Agent
        self._set_headers(request.headers)

        self._set_body(request.body)
        self._set_files(request.files)

        self._set_timeout(timeout)
        self._set_verify(verify)
        self._set_allow_redirects(allow_redirects)

        self.curl.setopt(pycurl.HEADERFUNCTION, response.handle_header_line)

        # 发送请求
        response.raw = self.curl.perform_rb()
        self._set_response(response)
        # 更新会话cookies
        self.cookies.update(response.cookies)
        return response

    def super_send(self, requests, config=None, times=None, concurreny=None, is_async=False, loop_until=None):
        pass


    def request(self, method=None, url=None, params=None, headers=None, cookies=None, data=None, json=None, files=None,
                timeout=None, verify=None, allow_redirects=None, proxies=None, hooks=None, stream=None, cert=None):
        """负责整合session和参数中的设置"""
        if self.base_url and not url.startswith('http'):
            url = '/'.join((self.base_url.rstrip('/'), url.lstrip('/')))
        params = merge_dict(self.params, params)
        headers = merge_dict(self.headers, headers)
        cookies = merge_dict(self.cookies, cookies)

        # 负责解析和格式化请求
        request = Request().prepare(method, url, headers, cookies, params, data, json, files)

        timeout = timeout or self.timeout
        verify = verify if verify is not None else self.verify
        allow_redirects = verify if allow_redirects is not None else self.allow_redirects

        res = self.send(request, timeout, verify, allow_redirects)
        return res

    # todo 简化
    def get(self, url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None, verify=False):
        return self.request('GET', url, params, headers, cookies, data, json, files, timeout, verify)

    def post(self, url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None, verify=False):
        return self.request('POST', url, params, headers, cookies, data, json, files, timeout, verify)

    def head(self, url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None, verify=False):
        return self.request('HEAD', url, params, headers, cookies, data, json, files, timeout, verify)

    def options(self, url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None, verify=False):
        return self.request('OPTIONS', url, params, headers, cookies, data, json, files, timeout, verify)

    def put(self, url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None, verify=False):
        return self.request('PUT', url, params, headers, cookies, data, json, files, timeout, verify)

    def patch(self, url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None, verify=False):
        return self.request('PATCH', url, params, headers, cookies, data, json, files, timeout, verify)

    def delete(self, url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None, verify=False):
        return self.request('DELETE', url, params, headers, cookies, data, json, files, timeout, verify)
