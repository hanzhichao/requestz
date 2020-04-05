import sys; sys.path.append('/Users/apple/Documents/Projects/Self/requestz')
import pytest
from requestz.runner import Session, Runner
import json


s = Session()
from pprint import pprint

HTTPBIN_BASE_URL = 'http://localhost'

def test_baidu():
    res = s.request('get', 'https://www.baidu.com')
    assert res.status_code == 200
    assert res.reason == 'OK'
    assert res.url == 'https://www.baidu.com'
    assert 'Connection' in res.headers
    assert 'BAIDUID' in res.cookies
    assert res.elapsed is not None
    assert res.apparent_encoding == 'utf-8'
    assert res.encoding == 'utf-8'
    # print(res.content)
    # print(res.text)
    # print(res.json())

def test_get():
    res = s.request('get', HTTPBIN_BASE_URL + '/get')
    assert res.status_code == 200
    print(res.text)


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


def test_response_headers_with_requests():
    import requests
    res = requests.get('https://www.baidu.com/')
    print(res.headers)
    print(res.cookies)


def test_session_defaults():
    s.headers = {'x-text1': 'abc'}
    res = s.get(HTTPBIN_BASE_URL+'/get', headers={'x-text2': 'abc'})
    print(res.text)


def test_session_base_url():
    s.base_url = HTTPBIN_BASE_URL
    res = s.get('/get', headers={'x-text2': 'abc'})
    print(res.text)


@pytest.mark.xfail
def test_session_timeout():
    s.timeout = 1
    res = s.get('https://httpbin.org/get', headers={'x-text2': 'abc'})
    print(res.text)


def test_session_keep_cookies():
    s.base_url = 'http://115.28.108.130:5000'
    res = s.post('/api/user/login/', data={'name': '张三', 'password': '123456'})
    print(res.text)
    res = s.get('/api/user/getUserList/')
    print(res.text)



if __name__ == "__main__":
    pytest.main([__file__, '-qs'])
