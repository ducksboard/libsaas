import logging

try:
    # Python 2.x
    import urllib2 as urllib_request
    from urllib import urlencode
except ImportError:
    # Python 3.x
    from urllib import request as urllib_request
    from urllib.parse import urlencode

from libsaas import http

from . import base

__all__ = ['urllib2_executor']


logger = logging.getLogger('libsaas.executor.urllib2_executor')


class RequestWithMethod(urllib_request.Request):

    def set_method(self, method):
        self.method = method

    def get_method(self):
        return self.method


def encode_uri(request):
    if not request.params:
        return request.uri

    return request.uri + '?' + urlencode(request.params)


def encode_data(request):
    if not request.params:
        return ''

    if not isinstance(request.params, dict):
        return request.params

    return urlencode(request.params)


class ErrorSwallower(urllib_request.HTTPErrorProcessor):

    def http_response(self, request, response):
        return response

    https_response = http_response


def urllib2_executor(request, parser):
    """
    The default executor, using Python's builtin urllib2 module.
    """
    logger.info('requesting %r', request)

    uri = request.uri
    data = None

    if request.method.upper() in http.URLENCODE_METHODS:
        uri = encode_uri(request)
    else:
        data = encode_data(request)

    logger.debug('request uri: %r, data: %r, headers: %r',
                 uri, data, request.headers)

    req = RequestWithMethod(uri, data, request.headers)
    req.set_method(request.method)

    opener = urllib_request.build_opener(ErrorSwallower)
    resp = opener.open(req)

    body = resp.read()
    headers = dict(resp.info())
    logger.debug('response code: %r, body: %r, headers: %r',
                 body, resp.code, headers)

    return parser(body, resp.code, headers)


def use():
    base.use_executor(urllib2_executor)
