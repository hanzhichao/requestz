import sys; sys.path.append('/Users/apple/Documents/Projects/Self/PyPi/requestz/')
import logging
import os
import unittest
from string import Template
from collections import ChainMap

import yaml
from logz import log as logging

from requestz.session import Session
from requestz.utils import type_check

print = logging.info


class TestCaseTemplate(unittest.TestCase):
    pass


class Runner(object):
    def __init__(self):
        self.session = Session()
        self.variables = ChainMap({}, os.environ)
        self.name = None
        self.base_url = None
        self.status = None

    def _do_parse(self, request):
        if not self.variables:
            return request
        # 处理参数化请求中的${变量}
        request_str = yaml.dump(request, default_flow_style=False)  # 先转为字符串
        if '$' in request_str:
            request_str = Template(request_str).safe_substitute(self.variables)  # 替换${变量}为局部变量中的同名变量
            request = yaml.safe_load(request_str)  # 重新转为字典
        return request

    def _do_check(self, step, response):
        # 处理断言
        verify = step.get('check')
        if verify is not None:
            for line in verify:
                try:
                    result = eval(line, {}, {'response': response})  # 计算断言表达式，True代表成功，False代表失败
                    status = 'PASS' if result is True else 'FAIL'
                except Exception as ex:
                    logging.exception(ex)
                    status = 'ERROR'
                if status != 'PASS':
                    self.status = status
                print("断言:", line, "结果:", status)

    def _do_extract(self, step, response):
        # 提取变量
        extract = step.get('extract')
        if extract is not None:  # 如果存在extract
            for key, value in extract.items():
                # 计算value表达式，可使用的全局变量为空，可使用的局部变量为RESPONSE(响应对象)
                # 保存变量结果到局部变量中
                try:
                    result = eval(value, {}, {'response': response})  # todo try
                    self.variables[key] = result
                except Exception as ex:
                    logging.exception(ex)
                    result = False
                print("提取变量:", key, value, '结果', result)
                self.variables[key] = result

    def _config_session(self, base_url, request):
        if base_url:
            type_check(base_url, str)
            self.session.base_url = base_url
        if request:
            type_check(request, dict)
            for key, value in request.items():
                setattr(self.session, key, value)

    def _handle_config(self, config: dict):
        if not isinstance(config, dict):
            raise TypeError(f'config: {config} 参数只支持dict类型')
        self.name = config.get('name')

        self.variables.update(config.get('variables', {}))
        self._config_session(config.get('base_url'), config.get('request'))

    def _handle_tests(self, tests: dict):
        results = []
        for test in tests:
            logging.info(f'执行测试用例: {test.get("name")}')
            steps = test.get('steps')
            if steps:
                results.append(self._handle_steps(steps))
        return results

    def _handle_steps(self, steps: list):
        if not isinstance(steps, list):
            raise TypeError(f'steps: {steps} 参数只支持dict类型')
        results = []
        for step in steps:
            print("处理请求:", step.get('name'))
            request = self._do_parse(step.get('request', {}))
            # 发送请求
            response = self.session.request(**request)  # 字典解包，发送接口
            print('状态码:', response.status_code, '响应内容:', response.text[:100]+' ... ')
            self._do_extract(step, response)
            self._do_check(step, response)  # todo raise Assertion Error
            results.append(response)

        return results

    def run(self, data: dict):
        config = data.get('config')
        steps = data.get('steps')
        tests = data.get('tests')
        results = []
        if config:
            self._handle_config(config)
        if steps:
            results.append(self._handle_steps(steps))
        if tests:
            results.extend(self._handle_tests(tests))

    def run_yaml(self, yaml_str):
        if not isinstance(yaml_str, str):
            raise TypeError(f'yaml_str: {yaml_str} 参数只支持str类型')
        try:
            data = yaml.safe_load(yaml_str)
        except Exception as ex:
            print(f'yaml_str: {yaml_str}格式不合法')
            raise ex
        return self.run(data)

    def build_testcases(self, tests: list):
        for index, test in enumerate(tests):
            name = test.get('name')
            steps = test.get('steps')
            test_method = lambda sub_self: self._handle_steps(steps)
            test_method.__doc__ = name
            setattr(TestCaseTemplate, f'test_{index+1}', test_method)
        print(TestCaseTemplate)

    def run_by_unittest(self, data):
        config = data.get('config')

        tests = data.get('tests')

        if config:
            self._handle_config(config)

        if tests:
            self.build_testcases(tests)
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCaseTemplate)
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            return result


if __name__ == '__main__':
    from filez import file
    data = file.load('/Users/apple/Documents/Projects/Self/PyPi/requestz/tests/data/testsuite.yaml')
    result = Runner().run_by_unittest(data)
    print(result)




