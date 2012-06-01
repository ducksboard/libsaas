"""
HTTP utilities.
"""
from libsaas import port

URLENCODE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class HTTPError(Exception):
    """
    A non-2xx code has been returned.
    """
    def __init__(self, body, code, headers):
        self.body = body
        self.code = code
        self.headers = headers

    def __str__(self):
        return '<{0} code {1}>'.format(self.__class__.__name__, self.code)


class Request(object):
    """
    Everything that's needed to make a HTTP request.
    """
    def __init__(self, method, uri, params=None, headers=None):
        """
        :var method: the HTTP method
        :vartype method: str using only ASCII characters

        :var uri: the URI, without query parameters
        :vartype uri: str using only ASCII characters

        :var params: query parameters or body
        :vartype params: dict or string, keys and values can be text, binary or
            integer and the executor will encode and quote them

        :var headers: HTTP headers :vartype headers: dict of str to str, both
            keys and values using only ASCII characters
        """
        self.method = method
        self.uri = uri
        self.params = params if params is not None else {}
        self.headers = headers if headers is not None else {}

    def __repr__(self):
        return "<Request [%s %s] at 0x%x>" % (self.method, self.uri,
                                              id(self))

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False

        return ((other.method, other.uri, other.params, other.headers) ==
                (self.method, self.uri, self.params, self.headers))

    def __ne__(self, other):
        return not self == other



def quote_any(val):
    """
    Percent quite any value, be it binary, text or integer.
    """
    return port.quote(port.to_b(val))


def urlencode_any(d):
    """
    Encode a dictionary consisting of a mixture of bytes, text and integers
    into a str object that only uses ASCII characters.
    """
    as_bytes = dict((port.to_b(key), port.to_b(value))
                    for key, value in d.items())
    return port.urlencode(as_bytes)
