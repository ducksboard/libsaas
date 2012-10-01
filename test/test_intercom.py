import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import intercom
from libsaas.services.base import MethodNotSupported


class IntercomTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = intercom.Intercom('my-app-id', 'my-api-key')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://api.intercom.io/v1' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_users(self):
        with self.assertRaises(MethodNotSupported):
            self.service.users().delete()

        self.service.users().get()
        self.expect('GET', '/users', {})
        self.service.users().get(per_page=3)
        self.expect('GET', '/users', {'per_page': 3})
        self.service.users().get(page=3)
        self.expect('GET', '/users', {'page': 3})

        user = {'user': 'x'}
        self.service.users().create(user)
        self.expect('POST', '/users', json.dumps(user))
        self.service.users().update(user)
        self.expect('PUT', '/users', json.dumps(user))

        with self.assertRaises(TypeError):
            self.service.user().get()

        with self.assertRaises(MethodNotSupported):
            self.service.user().create()
            self.service.user().update()
            self.service.user().delete()

        self.service.user().get(user_id=1)
        self.expect('GET', '/users', {'user_id': 1})
        self.service.user().get(email='name@domain.com')
        self.expect('GET', '/users', {'email': 'name@domain.com'})

    def test_impressions(self):
        with self.assertRaises(MethodNotSupported):
            self.service.impressions().get()
            self.service.impressions().update()
            self.service.impressions().delete()

        impression = {'impression': 'x'}
        self.service.impressions().create(impression)
        self.expect('POST', '/users/impressions', json.dumps(impression))

    def test_messages(self):
        with self.assertRaises(MethodNotSupported):
            self.service.message_threads().update()
            self.service.message_threads().delete()

        with self.assertRaises(TypeError):
            self.service.message_threads().get()

        self.service.message_threads().get(user_id=1)
        self.expect('GET', '/users/message_threads', {'user_id': 1})
        self.service.message_threads().get(email='name@domain.com')
        self.expect('GET', '/users/message_threads',
                    {'email': 'name@domain.com'})

        message_thread = {'message_thread': 'x'}
        self.service.message_threads().create(message_thread)
        self.expect('POST', '/users/message_threads',
                    json.dumps(message_thread))
        self.service.message_threads().reply(message_thread)
        self.expect('PUT', '/users/message_threads',
                    json.dumps(message_thread))

        with self.assertRaises(MethodNotSupported):
            self.service.message_thread().create()
            self.service.message_thread().update()
            self.service.message_thread().delete()

        with self.assertRaises(TypeError):
            self.service.message_thread().get(1234)

        self.service.message_thread().get(1234, user_id=1)
        self.expect('GET', '/users/message_threads',
                    {'thread_id': 1234, 'user_id': 1})
        self.service.message_thread().get(1234, email='name@domain.com')
        self.expect('GET', '/users/message_threads',
                    {'thread_id': 1234, 'email': 'name@domain.com'})
