
import pytest

from requestz.utils import double_split, parse_cookies, params_check


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