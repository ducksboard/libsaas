import json
import unittest

from libsaas.services import segmentio
from libsaas.executors import test_executor


class SegmentIOTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = segmentio.SegmentIO('my-api-secret')

    def expect(self, uri, params):
        self.assertEqual('POST', self.executor.request.method)

        self.assertEqual(self.executor.request.uri,
                         'https://api.segment.io/v1' + uri)

        params.update({'secret': 'my-api-secret'})
        self.assertEqual(json.loads(self.executor.request.params), params)

    def test_identify(self):
        self.service.user('user_id').identify()
        self.expect('/identify', {
            'userId': 'user_id',
        })

        self.service.user('user_id').identify(traits={'foo': 'bar'})
        self.expect('/identify', {
            'userId': 'user_id',
            'traits': {'foo': 'bar'}
        })

        self.service.user('user_id').identify(
            context={'providers':{'all': False}})
        self.expect('/identify', {
            'userId': 'user_id',
            'context': {'providers': {'all': False}}
        })

    def test_track(self):
        self.service.user('user_id').track('new event')
        self.expect('/track', {
            'userId': 'user_id',
            'event': 'new event',
        })

        self.service.user('user_id').track('new event', properties={'foo': 'bar'})
        self.expect('/track', {
            'userId': 'user_id',
            'properties': {'foo': 'bar'},
            'event': 'new event',
        })

        self.service.user('user_id').track(
            'new event', context={'providers':{'all': False}})
        self.expect('/track', {
            'userId': 'user_id',
            'event': 'new event',
            'context': {'providers': {'all': False}}
        })

    def test_alias(self):
        self.service.alias('from_user_id', 'to_user_id')
        self.expect('/alias', {
            'from': 'from_user_id',
            'to': 'to_user_id',
        })

    def test_import(self):
        actions = [{'action': 'track'}, {'action': 'identify'}]
        context = {'providers': {'all': False}}

        self.service.batch_import(actions)
        self.expect('/import', {'batch': actions})

        self.service.batch_import(actions, context)
        self.expect('/import', {'batch': actions,
                                'context': context})
