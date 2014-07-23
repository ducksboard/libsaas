import unittest

from libsaas import http
from libsaas.filters import auth


class FakeOAuth(auth.OAuth):

    def generate_timestamp(self):
        return '123456789'

    def generate_nonce(self):
        return '987654321'


class FakeOAuth1a(auth.OAuth1a):

    def generate_timestamp(self):
        return '123456789'

    def generate_nonce(self):
        return '987654321'


class OAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.auth = FakeOAuth('key', 'secret', 'token', 'token_secret')
        self.tmp_auth = FakeOAuth(None, None, 'token', 'token_secret')
        self.auth1a = FakeOAuth1a('key', 'secret', 'token', 'token_secret')

    def check_signature(self, req, signature, with_token=True):
        expected = ('OAuth oauth_consumer_key="token",oauth_nonce="987654321",'
                    'oauth_signature="%s",oauth_signature_method="HMAC-SHA1",'
                    'oauth_timestamp="123456789"' % signature)
        if with_token:
            expected += ',oauth_token="key"'

        self.assertEquals(req.headers['Authorization'], expected)

    def test_oauth(self):
        req = http.Request('GET', 'http://example.net/', {'arg': 'val'})
        self.auth(req)
        self.check_signature(req, 'BCd8cSS%2FCujJjfYSwG9MzfJRA7o%3D')

        req = http.Request('POST', 'http://example.net/', {'arg': 'val'})
        self.auth(req)
        self.check_signature(req, '11x9m5rxVBRKjksv9Qei2QCFLMw%3D')

        req = http.Request('POST', 'http://example.net/', {'!foo': '~bar'})
        self.auth(req)
        self.check_signature(req, '6yW45xEiPMbEvVdt9bCbgFznrIc%3D')

        no_body_sig = 'WiLmVChCp3f75uueQM5viSLPHIo%3D'
        req = http.Request('POST', 'http://example.net/', 'foo')
        self.auth(req)
        self.check_signature(req, no_body_sig)

        req = http.Request('POST', 'http://example.net/', 'bar')
        self.auth(req)
        self.check_signature(req, no_body_sig)

    def test_temporary_credentials_oauth(self):
        req = http.Request('GET', 'http://example.net/', {'arg': 'val'})
        self.tmp_auth(req)
        self.check_signature(req, 'dtlFLYBqLEml4a0ud38C3g0ssDI%3D', False)

        req = http.Request('POST', 'http://example.net/', {'arg': 'val'})
        self.tmp_auth(req)
        self.check_signature(req, 'sLjJPIJQ%2BmtnOWz4K3gfafR9kSU%3D', False)

    def test_base_string(self):
        # this test comes directly from RFC5849
        url = 'http://example.com/request?b5=%3D%253D&a3=a&c%40=&a2=r%20b'
        params = {'c2': '', 'a3': '2 q'}
        req = http.Request('POST', url, params)

        auth = FakeOAuth('kkk9d7dh3k39sjv7', 'foo', '9djdj82h48djs9d2', 'bar')
        base = auth.get_base_string(req, '7d8f3e4a', '137131201')

        expected = ('POST&http%3A%2F%2Fexample.com%2Frequest&a2%3Dr%2520b%26a3'
                    '%3D2%2520q%26a3%3Da%26b5%3D%253D%25253D%26c%2540%3D%26c2'
                    '%3D%26oauth_consumer_key%3D9djdj82h48djs9d2%26oauth_nonce'
                    '%3D7d8f3e4a%26oauth_signature_method%3DHMAC-SHA1%26oauth_'
                    'timestamp%3D137131201%26oauth_token%3Dkkk9d7dh3k39sjv7')
        self.assertEquals(base, expected)

    def test_unicode(self):
        # try both a unicode and a bytes parameter
        _lambda = b'\xce\xbb'
        _ulambda = _lambda.decode('utf-8')

        params = {'p1': _lambda, 'p2': _ulambda,
                  _lambda: 'p3', _ulambda: 'p4'}
        altparams = {'p1': _ulambda, 'p2': _lambda,
                     _ulambda: 'p3', _lambda: 'p4'}
        tparams = (('p1', _lambda), ('p1', _ulambda),
                   (_lambda, 'p3'), (_ulambda, 'p4'))

        req = http.Request('GET', 'http://example.net/', params)
        self.auth(req)
        self.check_signature(req, 'SQvPY80rfkxjdxJVRHlbd9WxPbc%3D')

        req = http.Request('GET', 'http://example.net/', tparams)
        self.auth(req)
        self.check_signature(req, 'i15AUj5VNYENlqf1bENS7SUHyRA%3D')

        sig = '%2BAp62XpZaOLSQxK0WQ080LHrfJw%3D'
        req = http.Request('POST', 'http://example.net/', params)
        self.auth(req)
        self.check_signature(req, sig)

        req = http.Request('POST', 'http://example.net/', altparams)
        self.auth(req)
        self.check_signature(req, sig)

        req = http.Request('POST', 'http://example.net/', tparams)
        self.auth(req)
        self.check_signature(req, 'yNF3UZo7D7mLdX0gSab1UOSlJMw%3D')

        # just a string
        no_body_sig = 'fEfK0QCWQ7BRODCafiuzDehqc1A%3D'
        req = http.Request('PUT', 'http://example.net/', _lambda)
        self.auth(req)
        self.check_signature(req, no_body_sig)

        req = http.Request('PUT', 'http://example.net/', _ulambda)
        self.auth(req)
        self.check_signature(req, no_body_sig)

    def test_oauth1a(self):
        req = http.Request('POST', 'http://example.net/', {'arg': 'val'})
        self.auth1a(req)
        self.check_signature(req, '11x9m5rxVBRKjksv9Qei2QCFLMw%3D')

        put_sig = 'fEfK0QCWQ7BRODCafiuzDehqc1A%3D'
        req = http.Request('PUT', 'http://example.net/', {'arg': 'val'})
        self.auth1a(req)
        self.check_signature(req, put_sig)

        req = http.Request('PUT', 'http://example.net/', {'foo': 'bar'})
        self.auth1a(req)
        self.check_signature(req, put_sig)
