from requestz.session import Session


def session():
    return Session()


def request(method, url, params=None, headers=None, cookies=None, data=None, json=None, files=None,
            timeout=None, verify=None, allow_redirects=None, proxies=None, hooks=None, stream=None, cert=None):
    with Session as session:
        return session.request(method, url, params, headers, cookies, data, json, files,
                               timeout, verify, allow_redirects, proxies, hooks, stream, cert)


def get(url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None,
        verify=False):
    return request('GET', url, params, headers, cookies, data, json, files, timeout, verify)


def post(url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None,
         verify=False):
    return request('POST', url, params, headers, cookies, data, json, files, timeout, verify)


def head(url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None,
         verify=False):
    return request('HEAD', url, params, headers, cookies, data, json, files, timeout, verify)


def options(url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None,
            verify=False):
    return request('OPTIONS', url, params, headers, cookies, data, json, files, timeout, verify)


def put(url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None,
        verify=False):
    return request('PUT', url, params, headers, cookies, data, json, files, timeout, verify)


def patch(url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None,
          verify=False):
    return request('PATCH', url, params, headers, cookies, data, json, files, timeout, verify)


def delete(url, params=None, headers=None, cookies=None, data=None, json=None, files=None, timeout=None,
           verify=False):
    return request('DELETE', url, params, headers, cookies, data, json, files, timeout, verify)