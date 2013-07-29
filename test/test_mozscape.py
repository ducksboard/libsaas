import json
import time
import unittest

from libsaas import port
from libsaas.executors import test_executor
from libsaas.services import mozscape
from libsaas.services.mozscape import constants


class MozscapeTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = mozscape.Mozscape('access-id', 'secret-key')
        self.service.timesource = self._timesource

    def _timesource(self):
        return time.struct_time((2000, 1, 1, 1, 1, 1, 1, 1, 1))

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://lsapi.seomoz.com/linkscape' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_urlmetrics(self):
        params = {'Cols': '9', 'Signature': '/pZ83jzQ+0589L0giwQkHg5yui0=',
                     'AccessID': 'access-id', 'Expires': '946688761'}

        self.service.urlmetrics('example.org/dir',
                                constants.TITLE + constants.SUBDOMAIN)
        self.expect('GET', '/url-metrics/example.org/dir/', params)

        urls = ['example.org/dir', 'example.net/other']
        self.service.urlmetrics(urls, constants.TITLE + constants.SUBDOMAIN)
        self.assertEqual(self.executor.request.method, 'POST')

        parsed = port.urlparse(self.executor.request.uri)
        self.assertEqual(
            (parsed.scheme, parsed.netloc, parsed.path),
            ('https', 'lsapi.seomoz.com', '/linkscape/url-metrics/'))
        self.assertEqual(dict(port.parse_qsl(parsed.query)), params)
        self.assertEqual(json.loads(self.executor.request.params), urls)

    def test_metadata(self):
        self.service.metadata().last_update()
        self.expect('GET', '/metadata/last_update.json')

        self.service.metadata().next_update()
        self.expect('GET', '/metadata/next_update.json')

        self.service.metadata().index_stats()
        self.expect('GET', '/metadata/index_stats')
