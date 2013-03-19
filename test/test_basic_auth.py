import unittest

from libsaas import http
from libsaas.filters import auth


class BasicAuthTestCase(unittest.TestCase):

    def test_simple(self):
        auth_filter = auth.BasicAuth('user', 'pass')
        req = http.Request('GET', 'http://example.net/')
        auth_filter(req)

        self.assertEqual(req.headers['Authorization'], 'Basic dXNlcjpwYXNz')

    def test_unicode(self):
        # try both a unicode and a bytes parameter
        _lambda = b'\xce\xbb'
        _ulambda = _lambda.decode('utf-8')

        auth_bytes = auth.BasicAuth('user', _lambda)
        auth_unicode = auth.BasicAuth('user', _ulambda)
        auth_mixed = auth.BasicAuth(_lambda, _ulambda)

        expected_bytes = 'Basic dXNlcjrOuw=='
        expected_unicode = expected_bytes
        expected_mixed = 'Basic zrs6zrs='

        for auth_filter, expected in ((auth_bytes, expected_bytes),
                                      (auth_unicode, expected_unicode),
                                      (auth_mixed, expected_mixed)):

            req = http.Request('GET', 'http://example.net/')
            auth_filter(req)

            self.assertEqual(req.headers['Authorization'], expected)
