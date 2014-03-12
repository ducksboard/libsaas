import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import newrelic


class InsightsTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.insert_key = 'insert_key'
        self.query_key = 'query_key'
        self.service = newrelic.Insights('account_id', self.query_key,
                                        self.insert_key)

    def serialize(self, data):
        return json.dumps(data)

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if self.executor.request.method.upper() == 'POST':
            self.assertEqual(self.executor.request.headers['X-Insert-Key'],
                             self.insert_key)
        else:
            self.assertEqual(self.executor.request.headers['X-Query-Key'],
                             self.query_key)

        if uri:
            self.assertEqual(self.executor.request.uri,
                             'https://rubicon.newrelic.com/beta_api/' +
                             'accounts/account_id/' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)

    def test_insert(self):
        events = [{'eventType': 'test', 'amount': 10}]
        self.service.insert(events)
        self.expect('POST', 'events', self.serialize(events))

    def test_sql(self):
        query = 'select * from TestEvent'
        self.service.query(query)
        self.expect('GET', 'query', {'nrql': query})
