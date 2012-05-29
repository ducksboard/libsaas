import base64
import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import mixpanel


class MixpanelTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'1', 200, {})

        self.service = mixpanel.Mixpanel('my-token', 'api-key', 'api-secret')

    def serialize(self, data):
        return base64.b64encode(json.dumps(data))

    def expect(self, uri, params=None, subdomain=None):
        if not subdomain:
            domain = 'mixpanel.com'
        else:
            domain = '{0}.mixpanel.com'.format(subdomain)

        if subdomain != 'api':
            uri = '/api/2.0{0}'.format(uri)

        self.assertEqual(self.executor.request.uri,
                         'http://{0}{1}'.format(domain, uri))
        if params:
            self.assertEquals(self.executor.request.params, params)

    def test_track(self):
        ret = self.service.track('login', {'user': 'foo'}, ip=True)
        data = self.serialize({'event': 'login',
                               'properties': {'token': 'my-token',
                                              'user': 'foo'}})
        self.expect('/data/track/', {'data': data, 'ip': '1'}, 'api')
        self.assertTrue(ret)

        ret = self.service.track('logout', test=True)
        data = self.serialize({'event': 'logout',
                               'properties': {'token': 'my-token'}})
        self.expect('/data/track/', {'data': data, 'test': '1'}, 'api')
        self.assertTrue(ret)

    def test_track_failure(self):
        self.executor.set_response(b'0', 200, {})

        ret = self.service.track('ev')
        self.assertFalse(ret)

    def test_events(self):
        self.service.events().get(['login', 'logout'], 'general', 'day', 10)
        self.expect('/events/', {'event': json.dumps(['login', 'logout']),
                                'type': 'general', 'unit': 'day', 'interval': 10})

        self.service.events().top('general', limit=10)
        self.expect('/events/top/', {'type': 'general', 'limit': 10})

        self.service.events().names('general')
        self.expect('/events/names/', {'type': 'general'})

    def test_event_properties(self):
        self.service.properties().get('login', 'plan', 'unique', 'day', 7,
                                      values=['standard', 'premium'])

        self.expect('/events/properties/',
                    {'event': 'login', 'name': 'plan', 'type': 'unique',
                     'unit': 'day', 'interval': '7',
                     'values': json.dumps(['standard', 'premium'])})

        self.service.properties().top('login')
        self.expect('/events/top/', {'event': 'login'})

        self.service.properties().values('login', 'plan', bucket='10')
        self.expect('/events/values/', {'event': 'login', 'name': 'plan',
                                        'bucket': 10})

    def test_funnels(self):
        self.service.funnels().get(10, '2012-01-01', length=5)
        self.expect('/funnels/', {'funnel_id': 10, 'from_date': '2012-01-01',
                                  'length': 5})

        self.service.funnels().list()
        self.expect('/funnels/list/', {})

    def test_segmentation(self):
        self.service.segmentation().get('login', '2011-01-01',
                                        '2012-01-01', type='unique')
        self.expect('/segmentation/',
                    {'event': 'login', 'from_date': '2011-01-01',
                     'to_date': '2012-01-01', 'type': 'unique'})

        self.service.segmentation().numeric('login', '2011-01-01',
                                            '2012-01-01', on='true', buckets=3)
        self.expect('/segmentation/numeric/',
                    {'event': 'login', 'from_date': '2011-01-01',
                     'to_date': '2012-01-01', 'on': 'true', 'buckets': 3})

        on = 'properties["succeeded"] - property["failed"]'
        self.service.segmentation().sum('buy', '2011-01-01', '2012-01-01', on)
        self.expect('/segmentation/sum/',
                    {'event': 'buy', 'from_date': '2011-01-01',
                     'to_date': '2012-01-01', 'on': on})

        on = 'property["amount"]', 'day'
        self.service.segmentation().average('pay', '2011-01-01',
                                            '2012-01-01', on, 'day')
        self.expect('/segmentation/average/',
                    {'event': 'pay', 'from_date': '2011-01-01',
                     'to_date': '2012-01-01', 'on': on, 'unit': 'day'})

    def test_retention(self):
        self.service.retention().get('2011-01-01', '2012-01-01',
                                     born_event='login', limit=10)
        self.expect('/retention/',
                    {'from_date': '2011-01-01', 'to_date': '2012-01-01',
                     'born_event': 'login', 'limit': 10})

    def test_export(self):
        self.service.export('2011-01-01', '2012-01-01', ['login', 'logout'])
        self.expect('/export/',
                    {'from_date': '2011-01-01', 'to_date': '2012-01-01',
                     'event': json.dumps(['login', 'logout'])}, 'data')

    def test_no_key(self):
        self.service = mixpanel.Mixpanel('my-token')

        # tracking is allowed without setting the api key and api secret
        self.service.track('login')
        data = self.serialize({'event': 'login',
                               'properties': {'token': 'my-token'}})
        self.expect('/data/track/', {'data': data}, 'api')

        # but data export methods fail
        self.assertRaises(mixpanel.Insufficient, self.service.funnels.list)
        self.assertRaises(mixpanel.ConfigurationError, self.service.export,
                          '2011-01-01', '2012-01-01', ['login', 'logout'])
