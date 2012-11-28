import unittest

from libsaas.executors import test_executor
from libsaas.services import base, desk


class DeskTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = desk.Desk('domain', 'key', 'secret',
                                           'token', 'token_secret')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method is not None:
            self.assertEqual(method, self.executor.request.method)
        if uri is not None:
            self.assertEqual(self.executor.request.uri,
                             'https://domain.desk.com/api/v1' + uri)
        if params is not None:
            self.assertEqual(self.executor.request.params, params)
        if headers is not None:
            self.assertEqual(self.executor.request.headers, headers)

    def test_cases(self):
        paging = {'page': 1, 'count': 5}
        self.service.cases().get()
        self.expect('GET', '/cases.json')

        self.service.cases().get(page=1, count=5)
        self.expect('GET', '/cases.json', paging)

        self.service.case(10).get()
        self.expect('GET', '/cases/10.json')

        self.service.case(10, is_external=True).get()
        self.expect('GET', '/cases/10.json', {'by': 'external_id'})

        self.service.case(10).update({'foo': 'bar'})
        self.expect('PUT', '/cases/10.json', {'foo': 'bar'})

        with self.assertRaises(base.MethodNotSupported):
            self.service.cases().create()
            self.service.cases().update()
            self.service.cases().delete()
            self.service.case(10).delete()

    def test_customers(self):
        obj = {'email': 'test@test.com'}
        paging = {'page': 1, 'count': 5}

        self.service.customers().get(count=5, page=1)
        self.expect('GET', '/customers.json', paging)

        self.service.customer(4).get()
        self.expect('GET', '/customers/4.json')

        self.service.customer(4).update(obj)
        self.expect('PUT', '/customers/4.json', obj)

        self.service.customers().create(obj)
        self.expect('POST', '/customers.json', obj)

        self.service.customer(4).emails().create(obj)
        self.expect('POST', '/customers/4/emails.json', obj)

        self.service.customer(4).email(1).update(obj)
        self.expect('PUT', '/customers/4/emails/1.json', obj)

        self.service.customer(4).phones().create(obj)
        self.expect('POST', '/customers/4/phones.json', obj)

        self.service.customer(4).phone(1).update(obj)
        self.expect('PUT', '/customers/4/phones/1.json', obj)

        with self.assertRaises(base.MethodNotSupported):
            self.service.customer(4).delete()
            self.service.customer(4).phone(1).delete()
            self.service.customer(4).phones().get()
            self.service.customer(4).phone(1).get()

    def test_interactions(self):
        obj = {'email': 'test@test.com'}
        paging = {'page': 1, 'count': 5}

        self.service.interactions().get(count=5, page=1)
        self.expect('GET', '/interactions.json', paging)

        self.service.interactions().create(obj)
        self.expect('POST', '/interactions.json', obj)

    def test_groups(self):
        paging = {'page': 1, 'count': 5}
        self.service.groups().get()
        self.expect('GET', '/groups.json')

        self.service.groups().get(page=1, count=5)
        self.expect('GET', '/groups.json', paging)

        self.service.group(10).get()
        self.expect('GET', '/groups/10.json')

        with self.assertRaises(base.MethodNotSupported):
            self.service.groups().create({'foo': 'bar'})
            self.service.group(10).delete()
            self.service.group(10).update()

    def test_users(self):
        paging = {'page': 1, 'count': 5}
        self.service.users().get()
        self.expect('GET', '/users.json')

        self.service.users().get(page=1, count=5)
        self.expect('GET', '/users.json', paging)

        self.service.user(10).get()
        self.expect('GET', '/users/10.json')

        with self.assertRaises(base.MethodNotSupported):
            self.service.users().create({'foo': 'bar'})
            self.service.user(10).delete()
            self.service.user(10).update()

    def test_topics(self):
        obj = {'subject': 'test'}
        paging = {'page': 1, 'count': 5}

        self.service.topics().get(count=5, page=1)
        self.expect('GET', '/topics.json', paging)

        self.service.topic(4).get()
        self.expect('GET', '/topics/4.json')

        self.service.topic(4).update(obj)
        self.expect('PUT', '/topics/4.json', obj)

        self.service.topics().create(obj)
        self.expect('POST', '/topics.json', obj)

        self.service.topic(4).delete()
        self.expect('DELETE', '/topics/4.json')

        self.service.topic(4).articles().get(count=5, page=1)
        self.expect('GET', '/topics/4/articles.json', paging)

        self.service.topic(4).articles().create(obj)
        self.expect('POST', '/topics/4/articles.json', obj)

        self.service.article(4).update(obj)
        self.expect('PUT', '/articles/4.json', obj)

        self.service.article(4).get()
        self.expect('GET', '/articles/4.json')

        self.service.article(4).delete()
        self.expect('DELETE', '/articles/4.json')

    def test_macros(self):
        obj = {'foo': 'bar'}
        paging = {'page': 1, 'count': 5}

        self.service.macros().get(count=5, page=1)
        self.expect('GET', '/macros.json', paging)

        self.service.macro(4).get()
        self.expect('GET', '/macros/4.json')

        self.service.macro(4).update(obj)
        self.expect('PUT', '/macros/4.json', obj)

        self.service.macros().create(obj)
        self.expect('POST', '/macros.json', obj)

        self.service.macro(4).delete()
        self.expect('DELETE', '/macros/4.json')

        self.service.macro(4).actions().get(count=5, page=1)
        self.expect('GET', '/macros/4/actions.json', paging)

        self.service.macro(4).action(1).get()
        self.expect('GET', '/macros/4/actions/1.json')

        self.service.macro(4).action(1).update(obj)
        self.expect('PUT', '/macros/4/actions/1.json', obj)

        with self.assertRaises(base.MethodNotSupported):
            self.service.macro(4).action(1).delete()
