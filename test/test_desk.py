import json
import unittest

from libsaas import http, port
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
                             'https://domain.desk.com/api/v2' + uri)
        if params is not None:
            params = (json.dumps(params)
                      if method not in http.URLENCODE_METHODS else params)
            self.assertEqual(self.executor.request.params, params)
        if headers is not None:
            self.assertEqual(self.executor.request.headers, headers)

    def test_cases(self):
        paging = {'page': 1, 'per_page': 5}
        self.service.cases().get()
        self.expect('GET', '/cases')

        self.service.cases().get(page=1, per_page=5)
        self.expect('GET', '/cases', paging)

        self.service.case(10).get()
        self.expect('GET', '/cases/10')

        self.service.case(10, is_external=True).get()
        self.expect('GET', '/cases/e-10')

        self.service.case(10).update({'foo': 'bar'})
        self.expect('PATCH', '/cases/10', {'foo': 'bar'})

        with port.assertRaises(base.MethodNotSupported):
            self.service.cases().create()
            self.service.cases().update()
            self.service.cases().delete()
            self.service.case(10).delete()

    def test_companies(self):
        obj = {'name': 'test'}
        paging = {'page': 1, 'per_page': 5}

        self.service.companies().get(per_page=5, page=1)
        self.expect('GET', '/companies', paging)

        self.service.company(4).get()
        self.expect('GET', '/companies/4')

        self.service.company(4).update(obj)
        self.expect('PATCH', '/companies/4', obj)

        self.service.companies().create(obj)
        self.expect('POST', '/companies', obj)

        self.service.companies().search('foo')
        self.expect('GET', '/companies/search', {'q': 'foo'})

        self.assertRaises(base.MethodNotSupported,
                          self.service.customer(4).delete)

    def test_customers(self):
        obj = {'email': 'test@test.com'}
        paging = {'page': 1, 'per_page': 5}

        self.service.customers().get(per_page=5, page=1)
        self.expect('GET', '/customers', paging)

        self.service.customer(4).get()
        self.expect('GET', '/customers/4')

        self.service.customer(4).update(obj)
        self.expect('PATCH', '/customers/4', obj)

        self.service.customers().create(obj)
        self.expect('POST', '/customers', obj)

        self.assertRaises(base.MethodNotSupported,
            self.service.customer(4).delete)

    def test_insights(self):
        self.service.insights().meta()
        self.expect('GET', '/insights/meta')

        self.service.insights().report(metrics='1,2,3')
        self.expect('POST', '/insights/reports', {'metrics': '1,2,3'})

    def test_groups(self):
        paging = {'page': 1, 'per_page': 5}
        self.service.groups().get()
        self.expect('GET', '/groups')

        self.service.groups().get(page=1, per_page=5)
        self.expect('GET', '/groups', paging)

        self.service.group(10).get()
        self.expect('GET', '/groups/10')

        self.assertRaises(base.MethodNotSupported,
            self.service.groups().create, {'foo': 'bar'})
        self.assertRaises(base.MethodNotSupported,
            self.service.group(10).delete)
        self.assertRaises(base.MethodNotSupported,
            self.service.group(10).update, {})

    def test_users(self):
        paging = {'page': 1, 'per_page': 5}
        self.service.users().get()
        self.expect('GET', '/users')

        self.service.users().get(page=1, per_page=5)
        self.expect('GET', '/users', paging)

        self.service.user(10).get()
        self.expect('GET', '/users/10')

        self.assertRaises(base.MethodNotSupported,
            self.service.users().create, {'foo': 'bar'})
        self.assertRaises(base.MethodNotSupported,
            self.service.user(10).delete)
        self.assertRaises(base.MethodNotSupported,
            self.service.user(10).update, {})

    def test_topics(self):
        obj = {'subject': 'test'}
        paging = {'page': 1, 'per_page': 5}

        self.service.topics().get(per_page=5, page=1)
        self.expect('GET', '/topics', paging)

        self.service.topic(4).get()
        self.expect('GET', '/topics/4')

        self.service.topic(4).update(obj)
        self.expect('PATCH', '/topics/4', obj)

        self.service.topics().create(obj)
        self.expect('POST', '/topics', obj)

        self.service.topic(4).delete()
        self.expect('DELETE', '/topics/4')

        self.service.topic(4).articles().get(per_page=5, page=1)
        self.expect('GET', '/topics/4/articles', paging)

        self.service.topic(4).articles().create(obj)
        self.expect('POST', '/topics/4/articles', obj)

        self.service.article(4).update(obj)
        self.expect('PATCH', '/articles/4', obj)

        self.service.article(4).get()
        self.expect('GET', '/articles/4')

        self.service.article(4).delete()
        self.expect('DELETE', '/articles/4')

    def test_macros(self):
        obj = {'foo': 'bar'}
        paging = {'page': 1, 'per_page': 5}

        self.service.macros().get(per_page=5, page=1)
        self.expect('GET', '/macros', paging)

        self.service.macro(4).get()
        self.expect('GET', '/macros/4')

        self.service.macro(4).update(obj)
        self.expect('PATCH', '/macros/4', obj)

        self.service.macros().create(obj)
        self.expect('POST', '/macros', obj)

        self.service.macro(4).delete()
        self.expect('DELETE', '/macros/4')

        self.service.macro(4).actions().get(per_page=5, page=1)
        self.expect('GET', '/macros/4/actions', paging)

        self.service.macro(4).action(1).get()
        self.expect('GET', '/macros/4/actions/1')

        self.service.macro(4).action(1).update(obj)
        self.expect('PATCH', '/macros/4/actions/1', obj)

        self.assertRaises(base.MethodNotSupported,
            self.service.macro(4).action(1).delete)

    def test_full_domain(self):
        service = desk.Desk('support.domain.com', 'key', 'secret',
                            'token', 'token_secret')
        service.users().get()
        self.assertEqual(self.executor.request.uri,
                         'https://support.domain.com/api/v2/users')
