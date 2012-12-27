import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import googlecalendar
from libsaas.services.base import MethodNotSupported


class GoogleCalendarTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = googlecalendar.GoogleCalendar(access_token='my-access-token')

    def expect(self, method=None, uri=None, params={}, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if uri:
            self.assertEqual(self.executor.request.uri,
                            'https://www.googleapis.com/calendar/v3' + uri)

        self.assertEqual(self.executor.request.params, params)

        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_user(self):
        with self.assertRaises(MethodNotSupported):
            self.service.me().get()
        with self.assertRaises(MethodNotSupported):
            self.service.me().create()
        with self.assertRaises(MethodNotSupported):
            self.service.me().update()
        with self.assertRaises(MethodNotSupported):
            self.service.me().patch()
        with self.assertRaises(MethodNotSupported):
            self.service.me().delete()

        with self.assertRaises(MethodNotSupported):
            self.service.me().settings().create()
        with self.assertRaises(MethodNotSupported):
            self.service.me().settings().update()
        with self.assertRaises(MethodNotSupported):
            self.service.me().settings().patch()
        with self.assertRaises(MethodNotSupported):
            self.service.me().settings().delete()

        self.service.me().settings().get()
        self.expect('GET', '/users/me/settings', {})

        with self.assertRaises(MethodNotSupported):
            self.service.me().setting('1234').create()
        with self.assertRaises(MethodNotSupported):
            self.service.me().setting('1234').update()
        with self.assertRaises(MethodNotSupported):
            self.service.me().setting('1234').patch()
        with self.assertRaises(MethodNotSupported):
            self.service.me().setting('1234').delete()

        self.service.me().setting('1234').get()
        self.expect('GET', '/users/me/settings/1234', {})

        with self.assertRaises(MethodNotSupported):
            self.service.me().calendar_lists().update()
        with self.assertRaises(MethodNotSupported):
            self.service.me().calendar_lists().patch()
        with self.assertRaises(MethodNotSupported):
            self.service.me().calendar_lists().delete()
        with self.assertRaises(MethodNotSupported):
            self.service.me().calendar_list('1234').create()

        self.service.me().calendar_lists().get()
        self.expect('GET', '/users/me/calendarList', {})
        obj = {'foo': 'bar'}
        self.service.me().calendar_lists().create(obj)
        self.expect('POST', '/users/me/calendarList', json.dumps(obj))

        self.service.me().calendar_list('1234').get()
        self.expect('GET', '/users/me/calendarList/1234', {})
        self.service.me().calendar_list('1234').update(obj)
        self.expect('PUT', '/users/me/calendarList/1234', json.dumps(obj))
        self.service.me().calendar_list('1234').patch(obj)
        self.expect('PATCH', '/users/me/calendarList/1234', json.dumps(obj))
        self.service.me().calendar_list('1234').delete()
        self.expect('DELETE', '/users/me/calendarList/1234', {})

    def test_colors(self):
        with self.assertRaises(MethodNotSupported):
            self.service.colors().create()
        with self.assertRaises(MethodNotSupported):
            self.service.colors().update()
        with self.assertRaises(MethodNotSupported):
            self.service.colors().patch()
        with self.assertRaises(MethodNotSupported):
            self.service.colors().delete()

        self.service.colors().get()
        self.expect('GET', '/colors', {})

    def test_freebusy(self):
        with self.assertRaises(MethodNotSupported):
            self.service.freebusy().get()
        with self.assertRaises(MethodNotSupported):
            self.service.freebusy().create()
        with self.assertRaises(MethodNotSupported):
            self.service.freebusy().update()
        with self.assertRaises(MethodNotSupported):
            self.service.freebusy().patch()
        with self.assertRaises(MethodNotSupported):
            self.service.freebusy().delete()

        obj = {'foo': 'bar'}
        self.service.freebusy().query(obj)
        self.expect('POST', '/freeBusy', json.dumps(obj))

    def test_calendar(self):
        with self.assertRaises(MethodNotSupported):
            self.service.calendars().get()
        with self.assertRaises(MethodNotSupported):
            self.service.calendars().update()
        with self.assertRaises(MethodNotSupported):
            self.service.calendars().patch()
        with self.assertRaises(MethodNotSupported):
            self.service.calendars().delete()

        obj = {'foo': 'bar'}
        self.service.calendars().create(obj)
        self.expect('POST', '/calendars', json.dumps(obj))

        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').create()

        self.service.calendar('1234').get()
        self.expect('GET', '/calendars/1234', {})
        self.service.calendar('1234').update(obj)
        self.expect('PUT', '/calendars/1234', json.dumps(obj))
        self.service.calendar('1234').patch(obj)
        self.expect('PATCH', '/calendars/1234', json.dumps(obj))
        self.service.calendar('1234').delete()
        self.expect('DELETE', '/calendars/1234', {})

        self.service.calendar('1234').clear()
        self.expect('POST', '/calendars/1234/clear', {})

        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').rules().update()
        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').rules().patch()
        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').rules().delete()

        self.service.calendar('1234').rules().get()
        self.expect('GET', '/calendars/1234/acl', {})
        obj = {'foo': 'bar'}
        self.service.calendar('1234').rules().create(obj)
        self.expect('POST', '/calendars/1234/acl', json.dumps(obj))

        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').rule('1234').create()

        self.service.calendar('1234').rule('1234').get()
        self.expect('GET', '/calendars/1234/acl/1234', {})
        self.service.calendar('1234').rule('1234').update(obj)
        self.expect('PUT', '/calendars/1234/acl/1234', json.dumps(obj))
        self.service.calendar('1234').rule('1234').patch(obj)
        self.expect('PATCH', '/calendars/1234/acl/1234', json.dumps(obj))
        self.service.calendar('1234').rule('1234').delete()
        self.expect('DELETE', '/calendars/1234/acl/1234', {})

        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').events().update()
        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').events().patch()
        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').events().delete()

        self.service.calendar('1234').events().get()
        self.expect('GET', '/calendars/1234/events', {})
        self.service.calendar('1234').events().get(timeZone='UTC')
        self.expect('GET', '/calendars/1234/events', {'timeZone': 'UTC'})
        obj = {'foo': 'bar'}
        self.service.calendar('1234').events().create(obj)
        self.expect('POST', '/calendars/1234/events', json.dumps(obj))
        self.service.calendar('1234').events().importing(obj)
        self.expect('POST', '/calendars/1234/events/import', json.dumps(obj))
        self.service.calendar('1234').events().quick_add('text', True)
        self.expect('POST',
            '/calendars/1234/events/quickAdd?text=text&sendNotifications=true')

        with self.assertRaises(MethodNotSupported):
            self.service.calendar('1234').event('1234').create()

        self.service.calendar('1234').event('1234').get()
        self.expect('GET', '/calendars/1234/events/1234', {})
        self.service.calendar('1234').event('1234').instances()
        self.expect('GET', '/calendars/1234/events/1234/instances', {})
        self.service.calendar('1234').event('1234').instances(maxResults=1)
        self.expect('GET', '/calendars/1234/events/1234/instances',
                    {'maxResults': 1})
        self.service.calendar('1234').event('1234').update(obj)
        self.expect('PUT', '/calendars/1234/events/1234', json.dumps(obj))
        self.service.calendar('1234').event('1234').update(obj, True)
        self.expect('PUT', '/calendars/1234/events/1234?alwaysIncludeEmail=true',
                    json.dumps(obj))
        self.service.calendar('1234').event('1234').patch(obj)
        self.expect('PATCH', '/calendars/1234/events/1234', json.dumps(obj))
        self.service.calendar('1234').event('1234').patch(obj, sendNotifications=True)
        self.expect('PATCH', '/calendars/1234/events/1234?sendNotifications=true',
                    json.dumps(obj))
        self.service.calendar('1234').event('1234').delete()
        self.expect('DELETE', '/calendars/1234/events/1234', {})
        self.service.calendar('1234').event('1234').delete(True)
        self.expect('DELETE', '/calendars/1234/events/1234?sendNotifications=true')
        self.service.calendar('1234').event('1234').move('1234')
        self.expect('POST', '/calendars/1234/events/1234/move?destination=1234')
