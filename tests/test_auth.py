import base64
from pprint import pprint

from requestz.auth import HTTPBasicAuth, HTTPDigestAuth


class TestAuth:
    def test_basic_auth_by_headers(self, s):
        url = 'https://postman-echo.com/basic-auth'
        auth = ('postman', 'password')
        auth_data = base64.b64encode('{}:{}'.format(*auth).encode()).decode()
        assert auth_data == 'cG9zdG1hbjpwYXNzd29yZA=='
        headers = {'Authorization': f'Basic {auth_data}'}

        res = s.get(url, headers=headers)
        assert res.ok

    def test_basic_auth_with_tuple_data(self, s):
        url = 'https://postman-echo.com/basic-auth'
        auth = ('postman', 'password')
        res = s.get(url, auth=auth)
        assert res.ok

    def test_basic_auth_with_dict_data(self, s):
        url = 'https://postman-echo.com/basic-auth'
        auth = {'basic': ('postman', 'password')}
        res = s.get(url, auth=auth)
        assert res.ok

    def test_basic_auth_with_HTTPBasicAuth_data(self, s):
        url = 'https://postman-echo.com/basic-auth'
        auth = HTTPBasicAuth('postman', 'password')
        res = s.get(url, auth=auth)
        assert res.ok

    def test_digest_auth_with_dict_data(self, s):
        url = 'https://postman-echo.com/digest-auth'
        auth = {'digest': ('postman', 'password')}
        res = s.get(url, auth=auth)
        assert res.ok

    def test_digest_auth_with_HTTPDigestAuth_data(self, s):
        url = 'https://postman-echo.com/digest-auth'
        auth = HTTPDigestAuth('postman', 'password')
        res = s.get(url, auth=auth)
        assert res.ok

    def test_hawk_auth(self, s):
        url = 'https://postman-echo.com/auth/hawk'
        auth = ('postman', 'password')
        # headers = {'Authorization': 'Basic cG9zdG1hbjpwYXNzd29yZA =='}

        auth = {'auth_id': 'dh37fgj492je',
                'auth_key': 'werxhqb98rpaxn39848xrunpaw3489ruxnpa98w4rxn',
                'algorithm': 'sha256'}

    def test_oauth1(self, s):
        url = 'https://postman-echo.com/oauth1'
        auth = ('postman', 'password')
        # headers = {'Authorization': 'Basic cG9zdG1hbjpwYXNzd29yZA =='}
        app_key = 'RKCGzna7bv9YD57c'
        app_secret = 'D+EdQ-gs$-%@2Nu7'
        auth_data = '''
        oauth_consumer_key="RKCGzna7bv9YD57c",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1472121261",oauth_nonce="ki0RQW",
        oauth_version="1.0",oauth_signature="s0rK92Myxx7ceUBVzlMaxiiXU00%3D"'''


        _auth_data = {
            'oauth_consumer_key': 'RKCGzna7bv9YD57c',
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': '1472121261',
            'oauth_nonce': 'ki0RQW',
            'oauth_version': '1.0',
            'oauth_signature': 's0rK92Myxx7ceUBVzlMaxiiXU00%3D'
        }
        '''
        
        ('Authorization', b'OAuth oauth_nonce="105856640399040064261689156557",
         oauth_timestamp="1689156557", 
         oauth_version="1.0", 
         oauth_signature_method="HMAC-SHA1", 
         oauth_consumer_key="RKCGzna7bv9YD57c", 
         oauth_signature="IhCK%2BQaaw4D%2BNMVOxe4y94Aofs0%3D"'
         )
        '''
        headers = {
            'Authorization': 'OAuth '
        }

        res = s.get(url, auth=auth)
        assert res.ok

        res = s.get(url, auth=auth)
        assert res.ok

    def test_requests_oauth1(self):
        import requests
        from requests_oauthlib import OAuth1
        url = 'https://postman-echo.com/oauth1'
        app_key = 'RKCGzna7bv9YD57c'
        app_secret = 'D+EdQ-gs$-%@2Nu7'
        token = ''
        token_secret = ''

        auth = OAuth1(app_key, app_secret)
        res = requests.get(url, auth=auth)
        req = res.request

        # print(req)
        pprint(res.request.headers)