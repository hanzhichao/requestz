
from string import Template

import yaml

from requestz.session import Session


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
