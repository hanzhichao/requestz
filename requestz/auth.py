from collections import namedtuple

HTTPBasicAuth = namedtuple('HTTPBasicAuth', 'username password')
HTTPDigestAuth = namedtuple('HTTPDigestAuth', 'username password')
HTTPNTLMAuth = namedtuple('HTTPNTLMAuth', 'username password')

OAuth1 = namedtuple('OAuth1', '')