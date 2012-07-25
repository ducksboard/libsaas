import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import spotify


class SpotifyTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = spotify.Spotify()

    def serialize(self, data):
        return json.dumps(data)

    def expect(self, uri, params=None):
        self.assertEqual(self.executor.request.uri,
                         '{0}/{1}'.format(self.service.get_url(),
                                                  uri))
        if params:
            self.assertEqual(self.executor.request.params, params)

    def test_search(self):
        self.service.search().artist('test')
        self.expect('search/1/artist', {'q': 'test'})

        self.service.search().album('test')
        self.expect('search/1/album', {'q': 'test'})

        self.service.search().track('test')
        self.expect('search/1/track', {'q': 'test'})

        self.service.search().artist('test', 2)
        self.expect('search/1/artist', {'q': 'test', 'page': 2})

        self.service.search().album('test', 2)
        self.expect('search/1/album', {'q': 'test', 'page': 2})

        self.service.search().track('test', 2)
        self.expect('search/1/track', {'q': 'test', 'page': 2})

    def test_lookup(self):
        self.service.lookup().artist('test')
        self.expect('lookup/1/', {'uri': 'test'})

        self.service.lookup().album('test')
        self.expect('lookup/1/', {'uri': 'test'})

        self.service.lookup().track('test')
        self.expect('lookup/1/', {'uri': 'test'})

        self.service.lookup().artist('test', 2)
        self.expect('lookup/1/', {'uri': 'test',
                                       'extras': 'albumdetail'})

        self.service.lookup().album('test', 2)
        self.expect('lookup/1/', {'uri': 'test',
                                       'extras': 'trackdetail'})

        self.service.lookup().artist('test', 1)
        self.expect('lookup/1/', {'uri': 'test',
                                       'extras': 'album'})

        self.service.lookup().album('test', 1)
        self.expect('lookup/1/', {'uri': 'test',
                                       'extras': 'track'})
