import unittest

from libsaas.executors import test_executor
from libsaas.services import googleanalytics


class GoogleAnalyticsTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = googleanalytics.GoogleAnalytics('access_token')

    def expect(self, method=None, uri=None, params=None):
        if method is not None:
            self.assertEqual(method, self.executor.request.method)
        if uri is not None:
            self.assertEqual(self.executor.request.uri,
                             self.service.APIROOT + uri)
        if params is not None:
            self.assertEqual(self.executor.request.params, params)

    def test_reporting(self):
        params = {'ids': 'ga:1111', 'metrics': 'm1,m2', 'dimensions':'dim1'}

        self.service.reporting().realtime('ga:1111', 'm1,m2', 'dim1')
        self.expect('GET', '/data/realtime', params)

        params.update({'start-date': '1992-05-20', 'end-date': '1992-05-21'})
        self.service.reporting().core('ga:1111', '1992-05-20', '1992-05-21',
                                          'm1,m2', 'dim1')
        self.expect('GET', '/data/ga', params)
