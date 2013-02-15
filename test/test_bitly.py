import unittest

from libsaas.executors import test_executor
from libsaas.services import bitly


class BitlyTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = bitly.Bitly('my-access-token')

    def expect(self, method=None, uri=None, params={}):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if uri:
            self.assertEqual(
                self.executor.request.uri,
                'https://api-ssl.bitly.com/v3' + uri)

        if params:
            params.update({'access_token': 'my-access-token'})
            self.assertEqual(self.executor.request.params, params)

    def test_users(self):
        self.service.user().info()
        self.expect('GET', '/user/info', {})
        self.service.user().info(login='1234')
        self.expect('GET', '/user/info', {'login': '1234'})
        self.service.user().info(login='1234', full_name='foo')
        self.expect('GET', '/user/info', {
            'login': '1234', 'full_name': 'foo'
        })

        self.service.user().link_history()
        self.expect('GET', '/user/link_history', {})
        self.service.user().link_history(link='http://foo.bar')
        self.expect('GET', '/user/link_history', {
            'link': 'http://foo.bar'
        })
        self.service.user().link_history(expand_client_id=True)
        self.expect('GET', '/user/link_history', {
            'expand_client_id': 'true'
        })

        self.service.user().network_history()
        self.expect('GET', '/user/network_history', {})
        self.service.user().network_history(expand_client_id=True)
        self.expect('GET', '/user/network_history', {
            'expand_client_id': 'true'
        })

        self.service.user().tracking_domain_list()
        self.expect('GET', '/user/tracking_domain_list', {})

        for method_name in ['clicks', 'countries', 'popular_links',
                            'referrers', 'referring_domains', 'share_counts']:
            method = getattr(self.service.user(), method_name)

            method()
            self.expect('GET', '/user/%s' % method_name, {})
            method(timezone='Europe/Andorra')
            self.expect('GET', '/user/%s' % method_name, {
                'timezone': 'Europe/Andorra'
            })
            method(timezone='Europe/Andorra', unit='month')
            self.expect('GET', '/user/%s' % method_name, {
                'unit': 'month',
                'timezone': 'Europe/Andorra'
            })
            method(timezone='Europe/Andorra', unit='month')
            self.expect('GET', '/user/%s' % method_name, {
                'unit': 'month',
                'timezone': 'Europe/Andorra'
            })

    def test_links(self):
        for method_name in ['info', 'category', 'social',
                            'location', 'language', 'encoders_count']:
            method = getattr(
                    self.service.link(link='http://foo.bar'), method_name)
            method()
            self.expect('GET', '/link/%s' % method_name, {
                'link': 'http://foo.bar'
            })

        self.service.link(link='http://foo.bar').content()
        self.expect('GET', '/link/content', {
            'link': 'http://foo.bar'
        })
        self.service.link(link='http://foo.bar').content(content_type='text')
        self.expect('GET', '/link/content', {
            'content_type': 'text',
            'link': 'http://foo.bar'
        })

        for method_name in ['clicks', 'countries', 'referrers',
                            'referrers_by_domain', 'referring_domains',
                            'shares']:
            method = getattr(
                    self.service.link(link='http://foo.bar'), method_name)

            method()
            self.expect('GET', '/link/%s' % method_name, {
                'link': 'http://foo.bar'
            })
            method(timezone='Europe/Andorra')
            self.expect('GET', '/link/%s' % method_name, {
                'link': 'http://foo.bar',
                'timezone': 'Europe/Andorra'
            })
            method(timezone='Europe/Andorra', unit='month')
            self.expect('GET', '/link/%s' % method_name, {
                'link': 'http://foo.bar',
                'unit': 'month',
                'timezone': 'Europe/Andorra'
            })
            method(timezone='Europe/Andorra', unit='month')
            self.expect('GET', '/link/%s' % method_name, {
                'link': 'http://foo.bar',
                'unit': 'month',
                'timezone': 'Europe/Andorra'
            })

    def test_highvalue(self):
        self.service.highvalue().get(limit=10)
        self.expect('GET', '/highvalue', {'limit': 10})

    def test_search(self):
        self.service.search().get()
        self.expect('GET', '/search', {})
        self.service.search().get(limit=10)
        self.expect('GET', '/search', {'limit': 10})

    def test_realtime(self):
        self.service.realtime().bursting_phrases()
        self.expect('GET', '/realtime/bursting_phrases', {})

        self.service.realtime().bursting_phrases()
        self.expect('GET', '/realtime/bursting_phrases', {})

        self.service.realtime().clickrate(phrase='foo')
        self.expect('GET', '/realtime/clickrate', {'phrase': 'foo'})
