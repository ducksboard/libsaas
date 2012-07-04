import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import zendesk


class ZendeskTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = zendesk.Zendesk('mydomain', 'user', 'pass')

    def serialize(self, data):
        return json.dumps(data).encode('utf-8')

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

        self.service.ticket(23).audits()
        self.expect('GET', '/tickets/23/audits.json')

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

        self.service.user(6).tickets_requested(2)
        self.expect('GET', '/users/6/tickets/requested.json', {'page': 2})

        self.service.user().get()
        self.service.user(6).tickets_ccd()
        self.expect('GET', '/users/6/tickets/ccd.json', {})

    def test_groups(self):
        self.service.groups().get(page=3)
        self.expect('GET', '/groups.json', {'page': 3})

        self.service.group(3).get()
        self.expect('GET', '/groups/3.json')

        self.service.groups().create({'group': {'x': 'x'}})
        self.expect('POST', '/groups.json',
                    json.dumps({'group': {'x': 'x'}}))

        self.service.group(23).update({'group': {'x': 'x'}})
        self.expect('PUT', '/groups/23.json',
                    json.dumps({'group': {'x': 'x'}}))

        self.service.group(23).delete()
        self.expect('DELETE', '/groups/23.json')

        self.service.groups().assignable()
        self.expect('GET', '/groups/assignable.json')

    def test_activities(self):
        self.service.activities().get(page=3)
        self.expect('GET', '/activities.json', {'page': 3})

        self.service.activities().get(since="2012-03-05T10:38:52Z")
        self.expect('GET', '/activities.json',
                    {'since': "2012-03-05T10:38:52Z"})

        self.service.activity(3).get()
        self.expect('GET', '/activities/3.json')

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

    def test_views(self):
        self.service.views().get(page=3)
        self.expect('GET', '/views.json', {'page': 3})

        self.service.views().active()
        self.expect('GET', '/views/active.json')

        self.service.views().count_many([1, 2])
        self.expect('GET', '/views/count_many.json', {'ids': '1,2'})

        conditions = {
            "all": [
                {"operator": "is",
                 "value": ["open"],
                 "field": "status"}
            ]
        }
        self.service.views().preview(conditions, columns=['subject'])
        conditions.update({'output': {'columns': ['subject']}})
        self.expect('POST', '/views/preview.json',
                    self.serialize({'view': conditions}))

        self.service.view(1).count()
        self.expect('GET', '/views/1/count.json')

        self.service.view(1).execute(sort_by='status')
        self.expect('GET', '/views/1/execute.json', {'sort_by': 'status'})

    def test_exports(self):
        self.service.exports().tickets(start_time=1340184927)
        self.expect('GET', '/exports/tickets.json',
                    {'start_time': 1340184927})
