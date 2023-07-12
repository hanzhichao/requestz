from typing import Union, Tuple

from requestz.response import Response
from requestz.session import Session
from requestz.auth import HTTPDigestAuth, HTTPNTLMAuth, HTTPBasicAuth, OAuth1

__copyright__ = '2023, Han Zhichao'
__author__ = 'Han Zhichao'
__version__ = '0.13'


def session():
    return Session()

# request = Session().request
# get = Session().get
# post = Session().post
# put = Session().put
# delete = Session().delete
# patch = Session().patch
# options = Session().options

def request(method: str, url: str, params: dict = None, headers: dict = None, cookies: dict = None,
            data: Union[dict, str, bytes] = None, json: dict = None, files: dict = None,
            timeout: int = None, verify: bool = None, allow_redirects: bool = None, proxies: tuple = None,
            hooks: dict = None,
            stream=None, cert=None, auth: Tuple[str] = None,
            http_version: str = None) -> Response:
    """
    Send a HTTP request.
    :param method:
    :param url:
    :param params:
    :param headers:
    :param cookies:
    :param data:
    :param json:
    :param files:
    :param timeout:
    :param verify:
    :param allow_redirects:
    :param proxies:
    :param hooks:
    :param stream:
    :param cert:
    :param http_version:
    :return:
    """
    with Session() as session:
        return session.request(method, url, params, headers, cookies, data, json, files,
                               timeout, verify, allow_redirects, proxies, hooks, stream, cert,
                               auth=auth, http_version=http_version)


def get(url, params: dict = None, headers: dict = None, cookies: dict = None,
        data: Union[dict, str, bytes] = None, json: dict = None,
        files: dict = None, timeout: int = None, auth: Tuple[str] = None,
        verify: bool = False, http_version: str = None) -> Response:
    """
    Sends a HTTP GET request.
    :param url: request url
    :param params: request params
    :param headers: request headers
    :param cookies: request cookies
    :param data: request data
    :param json: request json data
    :param files: request files
    :param timeout: request timeout
    :param verify: if verify certificate
    :param http_version: http version
    :return: Response object
    """
    return request('GET', url, params, headers, cookies, data, json, files, timeout, verify,
                   auth=auth, http_version=http_version)


def post(url, params: dict = None, headers: dict = None, cookies: dict = None,
         data: Union[dict, str, bytes] = None, json: dict = None,
         files: dict = None, timeout: int = None, auth: Tuple[str] = None,
         verify: bool = False, http_version: str = None) -> Response:
    """
    Sends a HTTP POST request.
    :param url: request url
    :param params: request params
    :param headers: request headers
    :param cookies: request cookies
    :param data: request data
    :param json: request json data
    :param files: request files
    :param timeout: request timeout
    :param verify: if verify certificate
    :param http_version: http version
    :return: Response object
    """
    return request('POST', url, params, headers, cookies, data, json, files, timeout, verify,
                   auth=auth, http_version=http_version)


def head(url, params: dict = None, headers: dict = None, cookies: dict = None,
         data: Union[dict, str, bytes] = None, json: dict = None,
         files: dict = None, timeout: int = None, auth: Tuple[str] = None,
         verify: bool = False, http_version: str = None) -> Response:
    """
    Send a HTTP Head request.
    :param url: request url
    :param params: request params
    :param headers: request headers
    :param cookies: request cookies
    :param data: request data
    :param json: request json data
    :param files: request files
    :param timeout: request timeout
    :param verify: if verify certificate
    :param http_version: http version
    :return: Response object
    """
    return request('HEAD', url, params, headers, cookies, data, json, files, timeout, verify,
                   auth=auth, http_version=http_version)


def options(url, params: dict = None, headers: dict = None, cookies: dict = None,
            data: Union[dict, str, bytes] = None, json: dict = None,
            files: dict = None, timeout: int = None, auth: Tuple[str] = None,
            verify: bool = False, http_version: str = None) -> Response:
    """
    Send a HTTP Options request.
    :param url: request url
    :param params: request params
    :param headers: request headers
    :param cookies: request cookies
    :param data: request data
    :param json: request json data
    :param files: request files
    :param timeout: request timeout
    :param verify: if verify certificate
    :param http_version: http version
    :return: Response object
    """
    return request('OPTIONS', url, params, headers, cookies, data, json, files, timeout, verify,
                   auth=auth, http_version=http_version)


def put(url, params: dict = None, headers: dict = None, cookies: dict = None,
        data: Union[dict, str, bytes] = None, json: dict = None,
        files: dict = None, timeout: int = None, auth: Tuple[str] = None,
        verify: bool = False, http_version: str = None) -> Response:
    """
    Send a HTTP Put request.
    :param url: request url
    :param params: request params
    :param headers: request headers
    :param cookies: request cookies
    :param data: request data
    :param json: request json data
    :param files: request files
    :param timeout: request timeout
    :param verify: if verify certificate
    :param http_version: http version
    :return: Response object
    """
    return request('PUT', url, params, headers, cookies, data, json, files, timeout, verify,
                   auth=auth, http_version=http_version)


def patch(url, params: dict = None, headers: dict = None, cookies: dict = None,
          data: Union[dict, str, bytes] = None, json: dict = None,
          files: dict = None, timeout: int = None, auth: Tuple[str] = None,
          verify: bool = False, http_version: str = None) -> Response:
    """
    Send a HTTP Patch request.
    :param url: request url
    :param params: request params
    :param headers: request headers
    :param cookies: request cookies
    :param data: request data
    :param json: request json data
    :param files: request files
    :param timeout: request timeout
    :param verify: if verify certificate
    :param http_version: http version
    :return: Response object
    """
    return request('PATCH', url, params, headers, cookies, data, json, files, timeout, verify,
                   auth=auth, http_version=http_version)


def delete(url, params: dict = None, headers: dict = None, cookies: dict = None,
           data: Union[dict, str, bytes] = None, json: dict = None,
           files: dict = None, timeout: int = None, auth: Tuple[str] = None,
           verify: bool = False, http_version: str = None) -> Response:
    """
    Send a HTTP Delete request.
    :param url: request url
    :param params: request params
    :param headers: request headers
    :param cookies: request cookies
    :param data: request data
    :param json: request json data
    :param files: request files
    :param timeout: request timeout
    :param verify: if verify certificate
    :param http_version: http version
    :return: Response object
    """
    return request('DELETE', url, params, headers, cookies, data, json, files, timeout, verify,
                   auth=auth, http_version=http_version)
