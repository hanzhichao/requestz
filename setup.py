import os
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
setup_requirements = []


def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setup(
    author="Han Zhichao",
    author_email='superhin@126.com',
    description='Requests based on PyCurl, more duration info in response',
    # long_description='easy log use for extra infos',
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",  # 新参数
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
    license="MIT license",
    include_package_data=True,
    keywords=[
        'restful', 'requests', 'http',
    ],
    name='requestz',
    packages=find_packages(include=['requestz']),
    setup_requires=setup_requirements,
    url='https://github.com/hanzhichao/requestz',
    version='0.12',
    zip_safe=True,
    install_requires=['pycurl', 'jsonschema', 'jsonpath', 'lxml']
)
