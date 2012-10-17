import unittest

from libsaas.executors import test_executor
from libsaas.services import instagram
from libsaas.services.base import MethodNotSupported


class InstagramTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = instagram.Instagram(access_token='my-access-token')

    def expect(self, method=None, uri=None, params={}, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if method == 'DELETE':
            uri += '?access_token=my-access-token'
        else:
            params.update({'access_token': 'my-access-token'})

        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://api.instagram.com/v1' + uri)

        self.assertEqual(self.executor.request.params, params)

        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_users(self):
        with self.assertRaises(MethodNotSupported):
            self.service.user('1234').create()
            self.service.user('1234').update()
            self.service.user('1234').delete()

        self.service.user('1234').get()
        self.expect('GET', '/users/1234', {})
        self.service.user('1234').recent_media().get()
        self.expect('GET', '/users/1234/media/recent', {})
        self.service.user('1234').recent_media().get(count=1)
        self.expect('GET', '/users/1234/media/recent', {'count': 1})
        self.service.user('1234').recent_media().get(count=1, min_id=1234)
        self.expect('GET', '/users/1234/media/recent',
                    {'count': 1, 'min_id': 1234})
        self.service.user('1234').follows().get()
        self.expect('GET', '/users/1234/follows', {})
        self.service.user('1234').followed_by().get()
        self.expect('GET', '/users/1234/followed-by', {})
        self.service.user('1234').relationship().get()
        self.expect('GET', '/users/1234/relationship', {})
        self.service.user('1234').relationship().update('unfollow')
        self.expect('POST', '/users/1234/relationship', {'action': 'unfollow'})

        with self.assertRaises(MethodNotSupported):
            self.service.authenticated_user().create()
            self.service.authenticated_user().update()
            self.service.authenticated_user().delete()

        self.service.authenticated_user().get()
        self.expect('GET', '/users/self', {})
        self.service.authenticated_user().feed().get()
        self.expect('GET', '/users/self/feed', {})
        self.service.authenticated_user().feed().get(count=1)
        self.expect('GET', '/users/self/feed', {'count': 1})
        self.service.authenticated_user().feed().get(count=1, max_id=1234)
        self.expect('GET', '/users/self/feed', {'count': 1, 'max_id': 1234})
        self.service.authenticated_user().liked_media().get()
        self.expect('GET', '/users/self/media/liked', {})
        self.service.authenticated_user().liked_media().get(count=2)
        self.expect('GET', '/users/self/media/liked', {'count': 2})
        self.service.authenticated_user().requested_by().get()
        self.expect('GET', '/users/self/requested-by', {})

        with self.assertRaises(MethodNotSupported):
            self.service.users().create()
            self.service.users().update()
            self.service.users().delete()

        self.service.users().get('test')
        self.expect('GET', '/users/search', {'q': 'test'})
        self.service.users().get('test', count=3)
        self.expect('GET', '/users/search', {'q': 'test', 'count': 3})

    def test_media(self):
        with self.assertRaises(MethodNotSupported):
            self.service.media('1234').create()
            self.service.media('1234').update()
            self.service.media('1234').delete()

        self.service.media('1234').get()
        self.expect('GET', '/media/1234', {})
        self.service.media('1234').comments().get()
        self.expect('GET', '/media/1234/comments', {})
        self.service.media('1234').comments().create({'text': 'testing'})
        self.expect('POST', '/media/1234/comments', {'text': 'testing'})
        self.service.media('1234').comment('1234').delete()
        self.expect('DELETE', '/media/1234/comments/1234', {})
        self.service.media('1234').likes().get()
        self.expect('GET', '/media/1234/likes', {})
        self.service.media('1234').likes().create()
        self.expect('POST', '/media/1234/likes', {})
        self.service.media('1234').likes().delete()
        self.expect('DELETE', '/media/1234/likes', {})

        with self.assertRaises(MethodNotSupported):
            self.service.medias().create()
            self.service.medias().update()
            self.service.medias().delete()

        self.service.medias().get()
        self.expect('GET', '/media/search', {})
        self.service.medias().get(lat=48.858844, lng=2.294351)
        self.expect('GET', '/media/search', {'lat': 48.858844, 'lng':2.294351})

        with self.assertRaises(MethodNotSupported):
            self.service.popular_media().create()
            self.service.popular_media().update()
            self.service.popular_media().delete()

        self.service.popular_media().get()
        self.expect('GET', '/media/popular', {})

    def test_tags(self):
        with self.assertRaises(MethodNotSupported):
            self.service.tag('1234').create()
            self.service.tag('1234').update()
            self.service.tag('1234').delete()

        self.service.tag('1234').get()
        self.expect('GET', '/tags/1234', {})
        self.service.tag('1234').recent_media().get()
        self.expect('GET', '/tags/1234/media/recent', {})
        self.service.tag('1234').recent_media().get(min_id=1)
        self.expect('GET', '/tags/1234/media/recent', {'min_id': 1})

        with self.assertRaises(MethodNotSupported):
            self.service.tags().create()
            self.service.tags().update()
            self.service.tags().delete()

        self.service.tags().get('tag-name')
        self.expect('GET', '/tags/search', {'q': 'tag-name'})

    def test_locations(self):
        with self.assertRaises(MethodNotSupported):
            self.service.location('1234').create()
            self.service.location('1234').update()
            self.service.location('1234').delete()

        self.service.location('1234').get()
        self.expect('GET', '/locations/1234', {})
        self.service.location('1234').recent_media().get()
        self.expect('GET', '/locations/1234/media/recent', {})
        self.service.location('1234').recent_media().get(min_id=1)
        self.expect('GET', '/locations/1234/media/recent', {'min_id': 1})

        with self.assertRaises(MethodNotSupported):
            self.service.locations().create()
            self.service.locations().update()
            self.service.locations().delete()

        self.service.locations().get()
        self.expect('GET', '/locations/search', {})
        self.service.locations().get(lat=48.858844, lng=2.294351)
        self.expect('GET', '/locations/search',
                    {'lat': 48.858844, 'lng':2.294351})

    def test_geographies(self):
        with self.assertRaises(MethodNotSupported):
            self.service.geography('1234').get()
            self.service.geography('1234').create()
            self.service.geography('1234').update()
            self.service.geography('1234').delete()

        self.service.geography('1234').recent_media().get()
        self.expect('GET', '/geographies/1234/media/recent', {})
        self.service.geography('1234').recent_media().get(count=2)
        self.expect('GET', '/geographies/1234/media/recent', {'count': 2})
