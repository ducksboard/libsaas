import logging

from libsaas import http, port

from . import base
from .urllib2_executor import encode_uri, encode_data
from .urllib2_executor import RequestWithMethod, ErrorSwallower

__all__ = ['urllib2_cert_executor']


logger = logging.getLogger('libsaas.executor.urllib2_cert_executor')



class HTTPSClientAuthHandler(port.urllib_request.HTTPSHandler):
    """HTTPS Client Auth Handler.

    (c) Kalys Osmonov - http://www.osmonov.com/2009/04/client-certificates-with-urllib2.html
    """
    def __init__(self, key_file, cert_file):
        port.urllib_request.HTTPSHandler.__init__(self)
        self.key_file = key_file
        self.cert_file = cert_file

    def https_open(self, req):
        # Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return port.client.HTTPSConnection(host, key_file=self.key_file,
                                           cert_file=self.cert_file)


class urllib2_cert_executor(object):

    def __init__(self, key_file, cert_file):
        self.key_file = key_file
        self.cert_file = cert_file

    def __call__(self, request, parser):
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

        opener = port.urllib_request.build_opener(
            ErrorSwallower,
            HTTPSClientAuthHandler(self.key_file, self.cert_file)
        )
        resp = opener.open(req)

        body = resp.read()
        headers = dict(resp.info())
        logger.debug('response code: %r, body: %r, headers: %r',
                     resp.code, body, headers)

        return parser(body, resp.code, headers)


def use(key_file, cert_file):
    base.use_executor(urllib2_cert_executor(key_file, cert_file))
