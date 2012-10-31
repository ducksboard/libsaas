import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import compete
from libsaas.services.base import MethodNotSupported


class CompeteTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = compete.Compete('my-api-key')

    def expect(self, method=None, uri=None, params=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'http://apps.compete.com' + uri)
        params = params or {}
        params['apikey'] = 'my-api-key'
        self.assertEqual(self.executor.request.params, params)

    def test_sites(self):
        with self.assertRaises(MethodNotSupported):
            self.service.site('libsaas.net').get()
            self.service.site('libsaas.net').create()
            self.service.site('libsaas.net').update()
            self.service.site('libsaas.net').delete()

        with self.assertRaises(MethodNotSupported):
            self.service.site('libsaas.net').metric('rank').create()
            self.service.site('libsaas.net').metric('rank').update()
            self.service.site('libsaas.net').metric('rank').delete()

        self.service.site('libsaas.net').metric('rank').get()
        self.expect('GET', '/sites/libsaas.net/trended/rank/', {})
        self.service.site('libsaas.net').metric('rank').get(latest=9)
        self.expect('GET', '/sites/libsaas.net/trended/rank/', {'latest': 9})
        (self.service.site('libsaas.net')
             .metric('rank').get(start_date='201209', end_date='201210'))
        self.expect('GET', '/sites/libsaas.net/trended/rank/', {
            'start_date': '201209',
            'end_date': '201210'
        })
        (self.service.site('libsaas.net')
             .metric('rank').get(start_date='20120901', end_date='20120915'))
        self.expect('GET', '/sites/libsaas.net/trended/rank/', {
            'start_date': '20120901',
            'end_date': '20120915'
        })

