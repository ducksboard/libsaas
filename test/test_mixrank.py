import unittest

from libsaas import http
from libsaas.executors import test_executor
from libsaas.services import mixrank


class MixRankTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})
        self.service = mixrank.MixRank('api-key')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'http://api.mixrank.com/v2/json/api-key' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_echo(self):
        self.service.echo()
        self.expect('GET', '/echo')

        self.executor.set_response(b'{}', 401, {})
        self.assertRaises(http.HTTPError, self.service.echo)

    def test_advertisers(self):
        adv = self.service.advertiser('foo.net')

        adv.summary()
        self.expect('GET', '/advertisers/foo.net')

        adv.textads(min_avg_position=10, last_seen_after='2010-01-01')
        self.expect('GET', '/advertisers/foo.net/gdn/textads',
                    {'min_avg_position': 10, 'last_seen_after': '2010-01-01'})

        adv.displayads(offset=1)
        self.expect('GET', '/advertisers/foo.net/gdn/displayads', {'offset': 1})

        adv.publishers(min_monthly_uniques=45)
        self.expect('GET', '/advertisers/foo.net/gdn/publishers',
                    {'min_monthly_uniques': 45})

        adv.keywords(page_size=10)
        self.expect('GET', '/advertisers/foo.net/gdn/keywords', {'page_size': 10})

    def test_publishers(self):
        pub = self.service.publisher('bar.com')

        pub.summary()
        self.expect('GET', '/publishers/bar.com')

        pub.advertisers(max_times_seen=3)
        self.expect('GET', '/publishers/bar.com/gdn/advertisers',
                    {'max_times_seen': 3})

        pub.textads(min_avg_position=2)
        self.expect('GET', '/publishers/bar.com/gdn/textads',
                    {'min_avg_position': 2})

        pub.displayads(sort_field='last_seen')
        self.expect('GET', '/publishers/bar.com/gdn/displayads',
                    {'sort_field': 'last_seen'})

    def test_keywords(self):
        kw = self.service.keyword('happy donuts')

        kw.summary()
        self.expect('GET', '/keywords/happy%20donuts')

        kw.advertisers(max_times_seen=10)
        self.expect('GET', '/keywords/happy%20donuts/gdn/advertisers',
                    {'max_times_seen': 10})

        kw.textads(offset=10)
        self.expect('GET', '/keywords/happy%20donuts/gdn/textads',
                    {'offset': 10})

        kw.displayads(max_times_seen=4)
        self.expect('GET', '/keywords/happy%20donuts/gdn/displayads',
                    {'max_times_seen': 4})

    def test_textads(self):
        ad = self.service.advertiser('foo.net').textad('19cd891ba98d8f9')

        ad.publishers(last_seen_before='2000-02-03')
        self.expect('GET', '/advertisers/foo.net/gdn/textads/'
                    '19cd891ba98d8f9/publishers',
                    {'last_seen_before': '2000-02-03'})

        ad.destinations(min_avg_position=5)
        self.expect('GET', '/advertisers/foo.net/gdn/textads/'
                    '19cd891ba98d8f9/destinations', {'min_avg_position': 5})

    def test_displayads(self):
        ad = self.service.advertiser('foo.net').displayad('19cd891ba98d8f9')

        ad.publishers(min_times_seen=100)
        self.expect('GET', '/advertisers/foo.net/gdn/displayads/'
                    '19cd891ba98d8f9/publishers',
                    {'min_times_seen': 100})

        ad.destinations()
        self.expect('GET', '/advertisers/foo.net/gdn/displayads/'
                    '19cd891ba98d8f9/destinations')
