import json

import pytest

HTTPBIN_BASE_URL = 'http://localhost'


def test_http2(s):
    url = 'https://http2.pro/api/v1'
    res = s.get(url)
    data = res.json()
    assert data['http2'] == 1, '不支持http2'


def test_http1_1(s):
    url = 'https://http2.pro/api/v1'
    res = s.get(url, http_version='1.1')
    data = res.json()
    assert data['http2'] == 0, '不支持http1.1'


def test_baidu(s):
    res = s.request('get', 'https://www.baidu.com')
    assert res.status_code == 200
    assert res.reason == 'OK'
    assert res.url == 'https://www.baidu.com'
    assert 'Connection' in res.headers.keys()
    assert 'BAIDUID' in res.cookies
    assert res.elapsed is not None
    assert res.apparent_encoding == 'utf-8'
    assert res.encoding == 'utf-8'
    # print(res.content)
    # print(res.text)
    # print(res.json())


def test_get(s):
    res = s.request('get', HTTPBIN_BASE_URL + '/get')
    assert res.status_code == 200
    print(res.text)


def test_get_with_query(s):
    res = s.request('get', 'https://httpbin.org/get?a=1&b=2')
    assert res.status_code == 200
    try:
        res_dict = json.loads(res.text)
    except Exception as ex:
        raise AssertionError(f'{res.text} not json')
    else:
        form = res_dict.get('args')
        assert form == {'a': '1', 'b': '2'}


def test_get_with_query2(s):
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


def test_post_form(s):
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


def test_post_json(s):
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


def test_response_headers_with_requests(s):
    import requests
    res = requests.get('https://www.baidu.com/')
    print(res.headers)
    print(res.cookies)


def test_session_defaults(s):
    s.headers = {'x-text1': 'abc'}
    res = s.get(HTTPBIN_BASE_URL + '/get', headers={'x-text2': 'abc'})
    print(res.text)


def test_session_base_url(s):
    s.base_url = HTTPBIN_BASE_URL
    res = s.get('/get', headers={'x-text2': 'abc'})
    print(res.text)


@pytest.mark.xfail
def test_session_timeout(s):
    s.timeout = 1
    res = s.get('https://httpbin.org/get', headers={'x-text2': 'abc'})
    print(res.text)


def test_session_keep_cookies(s):
    s.base_url = 'http://115.28.108.130:5000'
    res = s.post('/api/user/login/', data={'name': '张三', 'password': '123456'})
    print(res.text)
    res = s.get('/api/user/getUserList/')
    print(res.text)


def test_response_find_by_jsonpath_re(s):
    res = s.get(HTTPBIN_BASE_URL + '/get', headers={'x-text2': 'abc'})
    print(res.text)
    assert res.find('$.headers.X-Text2') == 'abc'
    assert res.find('"Connection": "(.*)"') == 'keep-alive'


def test_response_find_by_xpath(s):
    res = s.get('https://www.baidu.com/')
    assert res.find('//title/text()') == '百度一下，你就知道'


def test_response_verify_by_schema(s):
    res = s.get(HTTPBIN_BASE_URL + '/get', headers={'x-text2': 'abc'})
    print(res.text)
    schema1 = {
        "type": "object",
        "properties": {
            "args": {"type": "object"},
            "headers": {"type": "object"}
        }
    }
    schema2 = {
        "type": "object",
        "properties": {
            "args": {"type": "object"},
            "headers": {"type": "array"}
        }
    }
    assert res.check(schema1) is True
    assert res.check(schema2) is False


def test_request_with_files(s):
    res = s.post(HTTPBIN_BASE_URL + '/post', files={'file1': 'demo_apis.yaml', 'file2': '300.jpg'})
    print(res.text)





if __name__ == "__main__":
    pytest.main([__file__, '-qs'])
