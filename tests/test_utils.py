from pprint import pprint

import pytest

from requestz.utils import double_split, parse_cookies, params_check, get_random_str, hmac_sha1


def test_double_split():
    line = 'BAIDUID=1874C759F48209DB07521C82EF9B6A77:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com'
    result = double_split(line, ';', '=')
    print(dict(result))


def test_parse_cookies():
    line = 'BAIDUID=7F9E96B69ECAA4758C3981749DDCFBC2:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com'
    result = parse_cookies(line)
    print(result)


def test_check_type():
    @params_check(a=int)
    def func(a):
        print(a)

    with pytest.raises(TypeError):
        func('1')


def test_random_str():
    oauth_nonce = get_random_str(6)
    print(oauth_nonce)


def test_hmac_sha1():
    key = 'qhn757Yhlmo8IgbusRLE2nUPb8TorbyA'
    data = 'test'
    result = hmac_sha1(key, data)
    assert 'lHoxbZ3jbNNiaORZiTM1vQgf5X8=' == result, result


def test_generate_oauth_signature(s):
    # import oauthlib
    from oauthlib.oauth1 import Client
    method = 'GET'
    url = 'https://postman-echo.com/oauth'
    params = {'code': "xWnkliVQJURqB2x1",
              'grant_type': "authorization_code",
              'redirect_uri': "https://www.getpostman.com/oauth2/callback",
              'client_id': "abc123",
              'client_secret': "ssh-secret"}


    # result = hmac_sha1(key, data)
    # assert 'lHoxbZ3jbNNiaORZiTM1vQgf5X8=' == result, result
    client = Client(client_key='RKCGzna7bv9YD57c', client_secret='D+EdQ-gs$-%@2Nu7',
                    signature_method= "HMAC-SHA1", signature_type='AUTH_HEADER')

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        'Accept-Encoding': ', '.join(('gzip', 'deflate')),
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    _, headers, _ = client.sign(
        url,  method, None ,DEFAULT_HEADERS
    )
    # headers = {key.decode(): value.decode() for key, value in headers.items()}
    pprint(headers)
    {'Authorization': 'OAuth oauth_nonce="96049072079483928221689159441", '
                      'oauth_timestamp="1689159441", '
                      'oauth_version="1.0", '
                      'oauth_signature_method="HMAC-SHA1", '
                      'oauth_consumer_key="RKCGzna7bv9YD57c", '
                      'oauth_signature="gre2cHxVya1xQGCO1QCU2NLTan4%3D"'}
    {b'User-Agent': b'python-requests/2.31.0',
     b'Accept-Encoding': b'gzip, deflate',
     b'Accept': b'*/*',
     b'Connection': b'keep-alive',
     b'Authorization': b'OAuth oauth_nonce="6007613826801266151689159453", '
                       b'oauth_timestamp="1689159453", '
                       b'oauth_version="1.0", '
                       b'oauth_signature_method="HMAC-SHA1", '
                       b'oauth_consumer_key="RKCGzna7bv9YD57c", '
                       b'oauth_signature="J0HbmRQIsmF23DVARHpqtgi%2Ba3E%3D"'}

    {'User-Agent': b'python-requests/2.31.0',
     'Accept-Encoding': b'gzip, deflate',
     'Accept': b'*/*',
     'Connection': b'keep-alive',
     'Authorization': b'OAuth oauth_nonce="35394617813833342091689159734", '
                      b'oauth_timestamp="1689159734", '
                      b'oauth_version="1.0",'
                      b'oauth_signature_method="HMAC-SHA1", '
                      b'oauth_consumer_key="RKCGzna7bv9YD57c", '
                      b'oauth_signature="QddO%2BvBqga7OGdOJK%2FyJ4Z4Fo%2FM%3D"'}

    res = s.get(url, headers=headers)
    print(res)
    pprint(res.request.headers)