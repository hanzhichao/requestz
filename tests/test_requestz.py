import sys; sys.path.append('/Users/apple/Documents/Projects/Self/requestz')
import pytest
from requestz.runner import Session, Runner
import json


s = Session()


def test_baidu():
    res = s.request('get', 'https://www.baidu.com')
    assert res.status_code == 200

def test_get():
    res = s.request('get', 'https://httpbin.org/get')
    assert res.status_code == 200
    assert 'https://httpbin.org/get' in res.text


def test_get_with_query():
    res = s.request('get', 'https://httpbin.org/get?a=1&b=2')
    assert res.status_code == 200
    try:
        res_dict = json.loads(res.text)
    except Exception as ex:
        raise AssertionError(f'{res.text} not json')
    else:
        form = res_dict.get('args')
        assert form == {'a': '1', 'b': '2'}


def test_get_with_query2():
    res = s.request('get', 'https://httpbin.org/get?a=1&name=张三')
    assert res.status_code == 200
    print(res.text)
    try:
        res_dict = json.loads(res.text)
    except Exception as ex:
        raise AssertionError(f'{res.text} not json')
    else:
        form = res_dict.get('args')
        assert form == {'a': '1', 'name': '张三'}


def test_post_form():
    data = {'a': '1', 'b': '2'}
    res = s.request('post', 'https://httpbin.org/post', data=data)
    assert res.status_code == 200
    try:
        res_dict = json.loads(res.text)
    except Exception as ex:
        raise AssertionError(f'{res.text} not json')
    else:
        form = res_dict.get('form')
        assert form == data


def test_post_json():
    data = {'a': '1', 'b': '2'}
    res = s.request('post', 'https://httpbin.org/post', json=data)
    assert res.status_code == 200
    try:
        res_dict = json.loads(res.text)
    except Exception as ex:
        raise AssertionError(f'{res.text} not json')
    else:
        form = res_dict.get('json')
        assert form == data


def test_runner():
    with open('/Users/apple/Documents/Projects/Self/requestz/tests/demo_apis.yaml', encoding='utf-8') as f:
        data = f.read().strip()
    runner = Runner()
    runner.run_yaml(data)


if __name__ == "__main__":
    pytest.main([__file__, '-qs'])
