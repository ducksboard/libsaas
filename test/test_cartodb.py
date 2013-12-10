import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import cartodb


class CartoDBTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.api_key = 'test_key'
        self.service = cartodb.CartoDB('mydomain', self.api_key)

    def serialize(self, data):
        return json.dumps(data)

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://mydomain.cartodb.com/api/v2' + uri)
        if params:
            params['api_key'] = self.api_key
            self.assertEqual(self.executor.request.params, params)

    def test_sql(self):
        query = 'select * from test'
        self.service.sql(q=query)
        self.expect('POST', '/sql', {'q': query})
