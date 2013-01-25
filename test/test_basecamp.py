import json
import unittest

from libsaas.services.base import MethodNotSupported
from libsaas.executors import test_executor
from libsaas.services import basecamp


class BasecampTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = basecamp.Basecamp('my-account-id','my-access-token')

    def expect(self, method=None, uri=None, params={}):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if uri:
            self.assertEqual(
                self.executor.request.uri,
                'https://basecamp.com/my-account-id/api/v1' + uri + '.json')

        if params:
            self.assertEqual(self.executor.request.params, params)

    def test_projects(self):
        self.service.projects().get()
        self.expect('GET', '/projects', {})

        self.service.projects().archived()
        self.expect('GET', '/projects/archived', {})

        self.service.project('1234').get()
        self.expect('GET', '/projects/1234', {})

        obj = {'foo': 'bar'}
        self.service.projects().create(obj)
        self.expect('POST', '/projects', json.dumps(obj))

        self.service.project(1234).update(obj)
        self.expect('PUT', '/projects/1234', json.dumps(obj))

        self.service.project(1234).delete()
        self.expect('DELETE', '/projects/1234', {})

        self.service.project('1234').accesses().get()
        self.expect('GET', '/projects/1234/accesses', {})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).accesses().create({})
        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).access(1234).update({})
        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).access(1234).delete({})

        self.service.project(1234).accesses().grant(obj)
        self.expect('POST', '/projects/1234/accesses', json.dumps(obj))

        self.service.project(1234).access(1234).revoke()
        self.expect('DELETE', '/projects/1234/accesses/1234', {})

        self.service.project('1234').events().get(since='2013-01-01')
        self.expect('GET', '/projects/1234/events', {'since': '2013-01-01'})

        self.service.project('1234').topics().get()
        self.expect('GET', '/projects/1234/topics', {})
        self.service.project('1234').topics().get(page=2)
        self.expect('GET', '/projects/1234/topics', {'page': 2})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).topics().create({})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).messages().get()

        self.service.project(1234).messages().create(obj)
        self.expect('POST', '/projects/1234/messages', json.dumps(obj))

        self.service.project('1234').message(1234).get()
        self.expect('GET', '/projects/1234/messages/1234', {})
        self.service.project('1234').message(1234).update(obj)
        self.expect('PUT', '/projects/1234/messages/1234', json.dumps(obj))
        self.service.project('1234').message(1234).delete()
        self.expect('DELETE', '/projects/1234/messages/1234', {})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).message(1234).comments().get()

        self.service.project(1234).message(1234).comments().create(obj)
        self.expect('POST', '/projects/1234/messages/1234/comments',
                    json.dumps(obj))

        self.service.project(1234).comment(1234).delete()
        self.expect('DELETE', '/projects/1234/comments/1234', {})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).comment(1234).get()
        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).comment(1234).update(obj)

        self.service.project(1234).todolists().get()
        self.expect('GET', '/projects/1234/todolists', {})

        self.service.project(1234).todolists().completed()
        self.expect('GET', '/projects/1234/todolists/completed', {})

        self.service.project(1234).todolists().create(obj)
        self.expect('POST', '/projects/1234/todolists', json.dumps(obj))

        self.service.project(1234).todolist(1234).get()
        self.expect('GET', '/projects/1234/todolists/1234', {})

        self.service.project(1234).todolist(1234).update(obj)
        self.expect('PUT', '/projects/1234/todolists/1234', json.dumps(obj))

        self.service.project(1234).todolist(1234).delete()
        self.expect('DELETE', '/projects/1234/todolists/1234', {})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).todolist(1234).todos().get()

        self.service.project(1234).todolist(1234).todos().create(obj)
        self.expect('POST', '/projects/1234/todolists/1234/todos',
                    json.dumps(obj))

        self.service.project(1234).todo(1234).get()
        self.expect('GET', '/projects/1234/todos/1234', {})

        self.service.project(1234).todo(1234).update(obj)
        self.expect('PUT', '/projects/1234/todos/1234', json.dumps(obj))

        self.service.project(1234).todo(1234).delete()
        self.expect('DELETE', '/projects/1234/todos/1234', {})

        self.service.project(1234).documents().get()
        self.expect('GET', '/projects/1234/documents', {})

        self.service.project(1234).documents().create(obj)
        self.expect('POST', '/projects/1234/documents', json.dumps(obj))

        self.service.project(1234).document(1234).get()
        self.expect('GET', '/projects/1234/documents/1234', {})

        self.service.project(1234).document(1234).update(obj)
        self.expect('PUT', '/projects/1234/documents/1234', json.dumps(obj))

        self.service.project(1234).document(1234).delete()
        self.expect('DELETE', '/projects/1234/documents/1234', {})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).document(1234).comments().get()

        self.service.project(1234).document(1234).comments().create(obj)
        self.expect('POST', '/projects/1234/documents/1234/comments',
                    json.dumps(obj))

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).uploads().get()

        self.service.project(1234).uploads().create(obj)
        self.expect('POST', '/projects/1234/uploads', json.dumps(obj))

        self.service.project(1234).upload(1234).get()
        self.expect('GET', '/projects/1234/uploads/1234', {})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).upload(1234).comments().get()

        self.service.project(1234).upload(1234).comments().create(obj)
        self.expect('POST', '/projects/1234/uploads/1234/comments',
                    json.dumps(obj))

        self.service.project(1234).attachments().get()
        self.expect('GET', '/projects/1234/attachments', {})

        with self.assertRaises(MethodNotSupported):
            self.service.project(1234).attachments().create(obj)

        self.service.project('1234').calendar_events().get()
        self.expect('GET', '/projects/1234/calendar_events', {})

        self.service.project(1234).calendar_events().create(obj)
        self.expect('POST', '/projects/1234/calendar_events', json.dumps(obj))

        self.service.project('1234').calendar_events().past()
        self.expect('GET', '/projects/1234/calendar_events/past', {})

        self.service.project('1234').calendar_event(1234).get()
        self.expect('GET', '/projects/1234/calendar_events/1234', {})

        self.service.project('1234').calendar_event(1234).update(obj)
        self.expect('PUT', '/projects/1234/calendar_events/1234',
                    json.dumps(obj))

        self.service.project('1234').calendar_event(1234).delete()
        self.expect('DELETE', '/projects/1234/calendar_events/1234', {})

    def test_people(self):
        self.service.people().get()
        self.expect('GET', '/people', {})

        self.service.person().get()
        self.expect('GET', '/people/me', {})

        self.service.person('1234').get()
        self.expect('GET', '/people/1234', {})

        with self.assertRaises(MethodNotSupported):
            self.service.people().create({})
        with self.assertRaises(MethodNotSupported):
            self.service.person(1234).update({})

        self.service.person(1234).delete()
        self.expect('DELETE', '/people/1234', {})

        self.service.person('1234').events().get(since='2013-01-01')
        self.expect('GET', '/people/1234/events', {'since': '2013-01-01'})

    def test_events(self):
        self.service.events().get(since='2013-01-01')
        self.expect('GET', '/events', {'since': '2013-01-01'})
        self.service.events().get(since='2013-01-01', page=3)
        self.expect('GET', '/events', {'since': '2013-01-01', 'page': 3})

        with self.assertRaises(MethodNotSupported):
            self.service.events().create({})

    def test_calendars(self):
        self.service.calendars().get()
        self.expect('GET', '/calendars', {})

        self.service.calendar('1234').get()
        self.expect('GET', '/calendars/1234', {})

        obj = {'foo': 'bar'}
        self.service.calendars().create(obj)
        self.expect('POST', '/calendars', json.dumps(obj))

        self.service.calendar('1234').accesses().get()
        self.expect('GET', '/calendars/1234/accesses', {})

        with self.assertRaises(MethodNotSupported):
            self.service.calendar(1234).accesses().create({})
        with self.assertRaises(MethodNotSupported):
            self.service.calendar(1234).access(1234).update({})
        with self.assertRaises(MethodNotSupported):
            self.service.calendar(1234).access(1234).delete({})

        self.service.calendar(1234).accesses().grant(obj)
        self.expect('POST', '/calendars/1234/accesses', json.dumps(obj))

        self.service.calendar(1234).access(1234).revoke()
        self.expect('DELETE', '/calendars/1234/accesses/1234', {})

        self.service.calendar('1234').calendar_events().get()
        self.expect('GET', '/calendars/1234/calendar_events', {})

        self.service.calendar(1234).calendar_events().create(obj)
        self.expect('POST', '/calendars/1234/calendar_events', json.dumps(obj))

        self.service.calendar('1234').calendar_events().past()
        self.expect('GET', '/calendars/1234/calendar_events/past', {})

        self.service.calendar('1234').calendar_event(1234).get()
        self.expect('GET', '/calendars/1234/calendar_events/1234', {})

        self.service.calendar('1234').calendar_event(1234).update(obj)
        self.expect('PUT', '/calendars/1234/calendar_events/1234',
                    json.dumps(obj))

        self.service.calendar('1234').calendar_event(1234).delete()
        self.expect('DELETE', '/calendars/1234/calendar_events/1234', {})

    def test_topics(self):
        self.service.topics().get()
        self.expect('GET', '/topics', {})

    def test_todolists(self):
        self.service.todolists().get()
        self.expect('GET', '/todolists', {})

        self.service.todolists().completed()
        self.expect('GET', '/todolists/completed', {})

        with self.assertRaises(MethodNotSupported):
            self.service.todolists().create({})

        with self.assertRaises(MethodNotSupported):
            self.service.todolists().create({})

    def test_documents(self):
        self.service.documents().get()
        self.expect('GET', '/documents', {})

        with self.assertRaises(MethodNotSupported):
            self.service.documents().create({})

    def test_attachments(self):
        self.service.attachments().get()
        self.expect('GET', '/attachments', {})

        obj = {'foo': 'bar'}
        self.service.attachments().create(obj)
        self.expect('POST', '/attachments', json.dumps(obj))
