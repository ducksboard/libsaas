import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import zendesk


class ZendeskTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = zendesk.Zendesk('mydomain', 'user', 'pass')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://mydomain.zendesk.com/api/v2' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_tickets(self):
        self.service.tickets().get(page=3)
        self.expect('GET', '/tickets.json', {'page': 3})

        self.service.ticket(3).get()
        self.expect('GET', '/tickets/3.json')

        self.service.tickets().recent(per_page=10)
        self.expect('GET', '/tickets/recent.json', {'per_page': 10})

        self.service.tickets().create({'ticket': {'x': 'x'}})
        self.expect('POST', '/tickets.json',
                    json.dumps({'ticket': {'x': 'x'}}))

        self.service.ticket(23).update({'ticket': {'x': 'x'}})
        self.expect('PUT', '/tickets/23.json',
                    json.dumps({'ticket': {'x': 'x'}}))

        self.service.ticket(23).delete()
        self.expect('DELETE', '/tickets/23.json')

        self.service.ticket(23).collaborators(page=3)
        self.expect('GET', '/tickets/23/collaborators.json', {'page': 3})

    def test_users(self):
        self.service.users().get(page=10)
        self.expect('GET', '/users.json', {'page': 10})

        self.service.user(6).get()
        self.expect('GET', '/users/6.json')

        self.service.users().create({'user': {'name': 'foo'}})
        self.expect('POST', '/users.json',
                    json.dumps({'user': {'name': 'foo'}}))

        self.service.user(6).update({'user': {'name': 'bar'}})
        self.expect('PUT', '/users/6.json',
                    json.dumps({'user': {'name': 'bar'}}))

        self.service.user(6).delete()
        self.expect('DELETE', '/users/6.json')

        self.service.users().search('user@example.org')
        self.expect('GET', '/users/search.json', {'query': 'user@example.org'})

        self.service.user().get()
        self.expect('GET', '/users/me.json')

    def test_satisfaction(self):
        self.service.satisfaction_ratings().get(page=3)
        self.expect('GET', '/satisfaction_ratings.json', {'page': 3})

        self.service.satisfaction_ratings().received(page=3)
        self.expect('GET', '/satisfaction_ratings/received.json', {'page': 3})

        self.service.satisfaction_rating(3).get()
        self.expect('GET', '/satisfaction_ratings/3.json')

    def test_search(self):
        self.service.search('a term', sort_by='status')
        self.expect('GET', '/search.json',
                    {'query': 'a term', 'sort_by': 'status'})
