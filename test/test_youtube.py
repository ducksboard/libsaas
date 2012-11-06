import unittest

from libsaas.executors import test_executor
from libsaas.services import youtube
from libsaas.services.base import MethodNotSupported, get_params


class YouTubeTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = youtube.YouTube('my-access-token')


    def expect(self, uri=None, params=None, headers=None):
        if uri:
            self.assertEqual(self.executor.request.uri,
                             '{0}/{1}'.format(self.service.get_url(), uri))
        else:
            self.assertEqual(self.executor.request.uri,
                             youtube.Analytics.APIROOT)

        if params:
            self.assertEqual(self.executor.request.params, params)

        if headers is not None:
            self.assertEqual(self.executor.request.headers, headers)

    def test_auth(self):
        self.service.channels().get(part='snippet', mine=True)
        self.expect('channels',
                    {'mine': 'true', 'part': 'snippet'},
                    {'Authorization': 'Bearer my-access-token'})

    def test_analytics(self):
        self.service.analytics().get('CHANNEL==id1', 'm1,m2', '10-10-2010',
                                     '12-12-2012', dimensions='d1,d2',
                                     max_results=5, start_index=1, sort='m1')
        self.expect(None, {'ids': 'CHANNEL==id1', 'metrics': 'm1,m2',
                           'start-date': '10-10-2010', 'end-date': '12-12-2012',
                           'dimensions': 'd1,d2', 'max-results': 5,
                           'start-index': 1, 'sort': 'm1'})

    def test_activities(self):
        with self.assertRaises(MethodNotSupported):
            self.service.activities().create()
            self.service.activities().update()
            self.service.activities().delete()

        kwargs = {'part': 'snippet', 'mine': True, 'maxResults': 5,
                  'publishedBefore': '2012-01-01'}
        self.service.activities().get(**kwargs)
        self.expect('activities', get_params(None, kwargs))

    def test_channels(self):
        with self.assertRaises(MethodNotSupported):
            self.service.channels().create()
            self.service.channels().update()
            self.service.channels().delete()

        kwargs = {'part': 'snippet', 'mine': True, 'maxResults': 5,
                  'pageToken': 'token'}
        self.service.channels().get(**kwargs)
        self.expect('channels', get_params(None, kwargs))

    def test_guide_categories(self):
        with self.assertRaises(MethodNotSupported):
            self.service.guide_categories().create()
            self.service.guide_categories().update()
            self.service.guide_categories().delete()

        kwargs = {'part': 'snippet', 'id': 'ID', 'regionCode': 'CODE',
                  'hl': 'en_US'}
        self.service.guide_categories().get(**kwargs)
        self.expect('guideCategories', get_params(None, kwargs))

    def test_playlist_items(self):
        with self.assertRaises(MethodNotSupported):
            self.service.playlist_items().create()
            self.service.playlist_items().update()
            self.service.playlist_items().delete()

        kwargs = {'part': 'snippet', 'id': 'id1,id2', 'playlistId': 'id',
                  'maxResults': 5, 'pageToken': 'token'}
        self.service.playlist_items().get(**kwargs)
        self.expect('playlistItems', get_params(None, kwargs))

    def test_playlists(self):
        with self.assertRaises(MethodNotSupported):
            self.service.playlists().create()
            self.service.playlists().update()
            self.service.playlists().delete()

        kwargs = {'part': 'snippet', 'mine': True, 'maxResults': 5,
                  'pageToken': 'token'}
        self.service.playlists().get(**kwargs)
        self.expect('playlists', get_params(None, kwargs))

    def test_search(self):
        with self.assertRaises(MethodNotSupported):
            self.service.search().create()
            self.service.search().update()
            self.service.search().delete()

        kwargs = {'part': 'snippet', 'q': 'Leo Messi best goals', 'maxResults': 5,
                  'pageToken': 'token'}
        self.service.search().get(**kwargs)
        self.expect('search', get_params(None, kwargs))

    def test_subscriptions(self):
        with self.assertRaises(MethodNotSupported):
            self.service.subscriptions().create()
            self.service.subscriptions().update()
            self.service.subscriptions().delete()

        kwargs = {'part': 'snippet', 'id': 'subs_id', 'maxResults': 5,
                  'order': 'releveance', 'pageToken': 'token'}
        self.service.subscriptions().get(**kwargs)
        self.expect('subscriptions', get_params(None, kwargs))

    def test_video_categories(self):
        with self.assertRaises(MethodNotSupported):
            self.service.video_categories().create()
            self.service.video_categories().update()
            self.service.video_categories().delete()

        kwargs = {'part': 'snippet', 'id': 'ID', 'regionCode': 'CODE',
                  'hl': 'en_US'}
        self.service.video_categories().get(**kwargs)
        self.expect('videoCategories', get_params(None, kwargs))

    def test_videos(self):
        with self.assertRaises(MethodNotSupported):
            self.service.videos().create()
            self.service.videos().update()
            self.service.videos().delete()

        kwargs = {'part': 'snippet', 'id': 'videoid'}
        self.service.videos().get(**kwargs)
        self.expect('videos', get_params(None, kwargs))
