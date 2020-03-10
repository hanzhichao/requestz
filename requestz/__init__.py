import io
import json as js
import logging
from string import Template
from urllib.parse import quote, urlencode, urlparse, urlunparse

import pycurl
import yaml


class Response(object):
    def __init__(self):
        pass

    def json(self):
        try:
            return js.loads(self.text)
        except js.decoder.JSONDecodeError:
            print(f'响应非JSON格式: {self.text}')
            return {}


class Session(object):
    def __init__(self):
        self.c = pycurl.Curl()  # todo session默认配置

    def _handle_method(self, method: str):
        if not isinstance(method, str):
            raise TypeError(f'method: {method} 应为字符串')
        try:
            print('设置method:', method.upper())
            self.c.setopt(pycurl.CUSTOMREQUEST, method.upper())
        except Exception as ex:
            logging.exception(ex)
            raise ValueError(f'不支持的请求方法 {method}')

    def _handle_params(self, params: (dict, list, tuple)) -> str:
        if not isinstance(params, (dict, list, tuple)):
            raise TypeError(f'params: {params} 只支持dict,list,tuple格式')
        if isinstance(params, dict):
            params = params.items()

        params_list = ['='.join(item) for item in params]  # todo
        query = '&'.join(params_list)
        return query

    def _handle_query(self, url, params):
        """处理query中的中文"""  # todo
        result = urlparse(url=url, allow_fragments=True)
        query = result.query
        extra_query = self._handle_params(params) if params else ''
        if extra_query:
            query = '&'.join([query, extra_query]).strip('&')

        if not query:
            return url
        result = list(result)
        params = []
        for item in query.split('&'):
            item = item.split('=')
            params.append(f'{item[0]}={quote(item[1])}')
        result[4] = '&'.join(params)
        url = urlunparse(result)
        return url

    def _handle_url(self, url: str, params):   # todo url encode
        if not isinstance(url, str):
            raise TypeError(f'url: {url} 应为字符串')
        url = self._handle_query(url, params)
        try:
            print(f'设置url: {url}')
            if not url.startswith('http'):
                if not self.base_url:
                    raise ValueError('url未已http开头,并且base_url未配置')
                else:
                    url = f'{self.base_url}/{url.lstrip("/")}'

            self.c.setopt(pycurl.URL, url)
        except Exception as ex:
            logging.exception(ex)
            raise ValueError(f'url: {url} 不合法')

    def _handle_headers(self, headers: (dict, list, tuple)):
        if not isinstance(headers, (dict, list, tuple)):
            raise TypeError(f'headers: {headers} 只支持dict,list,tuple格式')

        if isinstance(headers, dict):
            headers = headers.items()

        headers = [': '.join(item) for item in headers]  # todo
        try:
            self.c.setopt(pycurl.HTTPHEADER, headers)
        except Exception as ex:
            logging.exception(ex)
            raise ValueError(f'headers: {headers} 不合法')

    def _handle_json(self, json: dict):
        if not isinstance(json, (dict)):
            raise TypeError(f'json: {json} 只支持dict格式')
        self.c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
        self.c.setopt(pycurl.POSTFIELDS, js.dumps(json))

    def _handle_data(self, data: (dict, str, io.TextIOWrapper)):
        if not isinstance(data, (dict, str, io.TextIOWrapper)):
            raise TypeError(f'data: {data} 只支持dict, str, io.TextIOWrapper格式')

        if isinstance(data, dict):
            self.c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/x-www-form-urlencoded"])
            self.c.setopt(pycurl.POSTFIELDS, urlencode(data))

    def _handle_timeout(self, timeout):
        if not isinstance(timeout, (int, float)):
            raise TypeError(f'timeout: {timeout} 只支持int,float格式')
        self.c.setopt(pycurl.TIMEOUT, timeout)

    def send(self):
        res = Response()
        content = self.c.perform_rb()
        res.status_code = self.c.getinfo(pycurl.HTTP_CODE)

        res.content = content
        res.text = content.decode('utf-8')  # todo

        res.elispse = self.c.getinfo(pycurl.TOTAL_TIME)
        res.namelookup_time = self.c.getinfo(pycurl.NAMELOOKUP_TIME)
        res.connect_time = self.c.getinfo(pycurl.CONNECT_TIME)
        res.pretransfer_time = self.c.getinfo(pycurl.PRETRANSFER_TIME)
        res.starttransfer_time = self.c.getinfo(pycurl.STARTTRANSFER_TIME)
        res.redirect_time = self.c.getinfo(pycurl.REDIRECT_TIME)

        # self.c.close()
        return res

    def request(self, method, url, params=None, headers=None, cookies=None,
                data=None, json=None, files=None, timeout=None, verify_ssl=False):

        self._handle_method(method)
        self._handle_url(url, params)
        if headers:
            self._handle_headers(headers)
        if data:
            self._handle_data(data)
        if json:
            self._handle_json(json)

        res = self.send()
        return res


class Runner(object):
    def __init__(self):
        self.session = Session()
        self.variables = None
        self.name = None
        self.base_url = None
        self.request = None

    def _handle_config(self, config: dict):
        if not isinstance(config, dict):
            raise TypeError(f'config: {config} 参数只支持dict类型')
        self.name = config.get('name')
        self.session.base_url = self.base_url = config.get('base_url')  # todo
        self.variables = config.get('variables', {})
        self.request = config.get('request')  # todo


    def _handle_steps(self, steps: list):
        if not isinstance(steps, list):
            raise TypeError(f'steps: {steps} 参数只支持dict类型')
        for step in steps:
            print("处理请求:", step.get('name'))
            request = step.get('request', {})  # 请求报文，默认值为{}
            # 处理参数化请求中的${变量}
            request_str = yaml.dump(request, default_flow_style=False)  # 先转为字符串
            if '$' in request_str:
                request_str = Template(request_str).safe_substitute(self.variables)  # 替换${变量}为局部变量中的同名变量
                request = yaml.safe_load(request_str)  # 重新转为字典
            # 发送请求
            response = self.session.request(**request)  # 字典解包，发送接口
            print('响应内容:', response.text)
            # 提取变量
            extract = step.get('extract')
            if extract is not None:  # 如果存在extract
                for key, value in extract.items():
                    # 计算value表达式，可使用的全局变量为空，可使用的局部变量为RESPONSE(响应对象)
                    # 保存变量结果到局部变量中
                    print("提取变量:", key, value)
                    self.variables[key] = eval(value, {}, {'response': response})
            # 处理断言
            verify = step.get('verify')
            if verify is not None:
                for line in verify:
                    result = eval(line, {}, {'response': response})  # 计算断言表达式，True代表成功，False代表失败
                    print("断言:", line, "结果:", "PASS" if result else "FAIL")


    def run_yaml(self, yaml_str):
        if not isinstance(yaml_str, str):
            raise TypeError(f'yaml_str: {yaml_str} 参数只支持str类型')
        try:
            data_dict = yaml.safe_load(yaml_str)
        except Exception as ex:
            print(f'yaml_str: {yaml_str}格式不合法')
            raise ex
        config = data_dict.get('config')
        steps = data_dict.get('steps')
        if config:
            self._handle_config(config)
        if steps:
            self._handle_steps(steps)
