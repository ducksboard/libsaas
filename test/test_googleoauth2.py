import unittest

from libsaas.executors import test_executor
from libsaas.services import googleoauth2
from libsaas.port import urlencode


class GoogleOauth2TestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = googleoauth2.GoogleOAuth2('id', 'secret')

    def expect(self, method=None, uri=None, params=None):
        if method is not None:
            self.assertEqual(method, self.executor.request.method)
        if uri is not None:
            self.assertEqual(self.executor.request.uri,
                             self.service.APIROOT + uri)
        if params is not None:
            self.assertEqual(self.executor.request.params, params)

    def test_access_token(self):
        params = {'client_id': 'id',
                  'client_secret': 'secret',
                  'grant_type': 'authorization_code',
                  'code': 'code',
                  'redirect_uri': 'uri'}

        self.service.access_token('code', 'uri')
        self.expect('POST', '/token', params)

    def test_refresh_token(self):
        params = {'client_id': 'id',
                  'client_secret': 'secret',
                  'grant_type': 'refresh_token',
                  'refresh_token': 'token'}

        self.service.refresh_token('token')
        self.expect('POST', '/token', params)

    def test_get_auth_url(self):
        auth_url = self.service.get_auth_url('code', 'foo', 'openid',
            openid_realm='bar')
        self.assertTrue(urlencode({'openid.realm': 'bar'}) in auth_url)
