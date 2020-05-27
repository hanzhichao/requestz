# import sys; sys.path.append('/Users/apple/Documents/Projects/Self/requestz')
import os

import pytest
from filez import file

from requestz.runner import Session, Runner

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASEDIR, 'tests', 'data')


def test_runner_2f():  # file as testcase
    file_path = os.path.join(DATA_DIR, 'testcase.yaml')
    data = file.load(file_path)
    runner = Runner()
    results = runner.run(data)
    print(results)


def test_runner_3f():  # file as testsuite
    file_path = os.path.join(DATA_DIR, 'testsuite.yaml')
    data = file.load(file_path)
    runner = Runner()
    results = runner.run(data)
    print(results)


def test_run_by_unittest():
    pass