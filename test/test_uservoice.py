import json
import unittest

from libsaas import http
from libsaas.executors import test_executor
from libsaas.services import base, uservoice


class UserVoiceTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = uservoice.UserVoice('domain', 'key', 'secret',
                                           'token', 'token_secret')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method is not None:
            self.assertEqual(method, self.executor.request.method)
        if uri is not None:
            self.assertEqual(self.executor.request.uri,
                             'http://domain.uservoice.com/api/v1' + uri)
        if params is not None:
            self.assertEqual(self.executor.request.params, params)
        if headers is not None:
            self.assertEqual(self.executor.request.headers, headers)

    def test_client_auth(self):
        service = uservoice.UserVoice('domain', 'key')
        service.articles().get()

        self.expect('GET', '/articles.json', {'client': 'key'})

    def test_articles(self):
        self.service.articles().get()
        self.expect('GET', '/articles.json')

        self.service.articles().create({'foo': 'bar'})
        self.expect('POST', '/articles.json', {'article[foo]': 'bar'})

        self.service.article(10).get()
        self.expect('GET', '/articles/10.json')

        # PUT requests get pre-urlencoded
        self.service.article(10).update({'foo': 'bar'})
        self.expect('PUT', '/articles/10.json',
                    http.urlencode_any({'article[foo]': 'bar'}))

        self.service.article(10).useful()
        self.expect('POST', '/articles/10/useful.json')

        self.service.articles().search(query='foo')
        self.expect('GET', '/articles/search.json', {'query': 'foo'})

    def test_categories(self):
        self.service.forum(4).categories().get()
        self.expect('GET', '/forums/4/categories.json')

        self.service.forum(4).category(3).get()
        self.expect('GET', '/forums/4/categories/3.json')

        self.service.forum(4).categories().create({'foo': 'bar'})
        self.expect('POST', '/forums/4/categories.json',
                    {'category[foo]': 'bar'})

        # PUT requests get pre-urlencoded
        self.service.forum(4).category(3).update({'foo': 'bar'})
        self.expect('PUT', '/forums/4/categories/3.json',
                    http.urlencode_any({'category[foo]': 'bar'}))

        self.service.forum(4).category(3).delete()
        self.expect('DELETE', '/forums/4/categories/3.json')

    def test_comments(self):
        self.service.comments().get()
        self.expect('GET', '/comments.json')

        self.service.forum(3).suggestion(5).comments().get()
        self.expect('GET', '/forums/3/suggestions/5/comments.json')

        self.service.forum(3).suggestion(5).comment(6).get()
        self.expect('GET', '/forums/3/suggestions/5/comments/6.json')

        self.service.forum(3).suggestion(5).comments().create('foo')
        self.expect('POST', '/forums/3/suggestions/5/comments.json',
                    {'comment[text]': 'foo'})

        # PUT requests get pre-urlencoded
        self.service.forum(3).suggestion(5).comment(6).update('bar')
        self.expect('PUT', '/forums/3/suggestions/5/comments/6.json',
                    http.urlencode_any({'comment[text]': 'bar'}))

        self.service.forum(3).suggestion(5).comment(6).delete()
        self.expect('DELETE', '/forums/3/suggestions/5/comments/6.json')

        self.service.user(3).comments().get()
        self.expect('GET', '/users/3/comments.json')

    def test_custom_fields(self):
        self.service.custom_fields().get()
        self.expect('GET', '/custom_fields.json')

        self.service.custom_fields().public()
        self.expect('GET', '/custom_fields/public.json')

    def test_flags(self):
        self.service.forum(5).suggestion(6).comment(2).flags().get()
        self.expect('GET', '/forums/5/suggestions/6/comments/2/flags.json')

        self.service.forum(5).suggestion(6).comment(2).flags().create(
            'duplicate')
        self.expect('POST', '/forums/5/suggestions/6/comments/2/flags.json',
                    {'code': 'duplicate'})

        self.service.forum(5).suggestion(6).flags().get()
        self.expect('GET', '/forums/5/suggestions/6/flags.json')

        self.service.forum(5).suggestion(6).flags().create('duplicate')
        self.expect('POST', '/forums/5/suggestions/6/flags.json',
                    {'code': 'duplicate'})

        self.service.faq(5).flags().get()
        self.expect('GET', '/faqs/5/flags.json')

        self.service.faq(5).flags().create('inappropriate')
        self.expect('POST', '/faqs/5/flags.json',
                    {'code': 'inappropriate'})

    def test_forums(self):
        self.service.forums().get()
        self.expect('GET', '/forums.json')

        self.service.forum(2).get()
        self.expect('GET', '/forums/2.json')

        self.service.forums().create({'foo': 'bar'})
        self.expect('POST', '/forums.json', {'forum[foo]': 'bar'})

        # PUT requests get pre-urlencoded
        self.service.forum(2).update({'foo': 'bar'})
        self.expect('PUT', '/forums/2.json',
                    http.urlencode_any({'forum[foo]': 'bar'}))

        self.service.forum(2).delete()
        self.expect('DELETE', '/forums/2.json')

    def test_gadgets(self):
        self.service.gadgets().get()
        self.expect('GET', '/gadgets.json')

        self.service.gadget(2).get()
        self.expect('GET', '/gadgets/2.json')

        self.service.gadgets().create({'foo': 'bar'})
        self.expect('POST', '/gadgets.json', {'gadget[foo]': 'bar'})

        # PUT requests get pre-urlencoded
        self.service.gadget(2).update({'foo': 'bar'})
        self.expect('PUT', '/gadgets/2.json',
                    http.urlencode_any({'gadget[foo]': 'bar'}))

        self.service.gadget(2).delete()
        self.expect('DELETE', '/gadgets/2.json')

    def test_notes(self):
        self.service.notes().get()
        self.expect('GET', '/notes.json')

        self.service.forum(6).suggestion(3).notes().get()
        self.expect('GET', '/forums/6/suggestions/3/notes.json')

        # PUT requests get pre-urlencoded
        self.service.forum(6).suggestion(3).note(4).update('note')
        self.expect('PUT', '/forums/6/suggestions/3/notes/4.json',
                    http.urlencode_any({'note[text]': 'note'}))

        self.service.forum(6).suggestion(3).notes().create('note')
        self.expect('POST', '/forums/6/suggestions/3/notes.json',
                    {'note[text]': 'note'})

        self.service.forum(6).suggestion(3).note(4).delete()
        self.expect('DELETE', '/forums/6/suggestions/3/notes/4.json')

        self.service.user(6).notes().get()
        self.expect('GET', '/users/6/notes.json')

    def test_oembed(self):
        self.service.oembed('forums/1/suggestions/2')
        self.expect('GET', '/oembed.json', {'url': 'forums/1/suggestions/2'})

    def test_search(self):
        self.service.search(query='foo')
        self.expect('GET', '/search.json', {'query': 'foo'})

        self.service.instant_answers_search(query='foo')
        self.expect('GET', '/instant_answers/search.json', {'query': 'foo'})

    def test_streams(self):
        self.service.stream().public()
        self.expect('GET', '/stream/public.json')

        self.service.stream().private()
        self.expect('GET', '/stream/private.json')

        self.service.forum(5).stream().public()
        self.expect('GET', '/forums/5/stream/public.json')

        self.service.forum(5).stream().private()
        self.expect('GET', '/forums/5/stream/private.json')

    def test_subdomains(self):
        self.service.subdomain('foo').get()
        self.expect('GET', '/subdomains/foo.json')

    def test_suggestions(self):
        self.service.suggestions().get()
        self.expect('GET', '/suggestions.json')

        self.service.suggestion(2).get()
        self.expect('GET', '/suggestions/2.json')

        self.service.suggestions().search(query='foo')
        self.expect('GET', '/suggestions/search.json', {'query': 'foo'})

        self.service.forum(4).suggestions().get()
        self.expect('GET', '/forums/4/suggestions.json')

        self.service.forum(3).suggestions().create({'title': 'foo'})
        self.expect('POST', '/forums/3/suggestions.json',
                    {'suggestion[title]': 'foo'})

        self.service.forum(3).suggestion(8).delete()
        self.expect('DELETE', '/forums/3/suggestions/8.json')

        self.service.user(9).suggestions().get()
        self.expect('GET', '/users/9/suggestions.json')

        self.service.forum(2).user_suggestions(9).get()
        self.expect('GET', '/forums/2/users/9/suggestions.json')

        self.service.forum(2).suggestions().search(query='foo')
        self.expect('GET', '/forums/2/suggestions/search.json',
                    {'query': 'foo'})

        # PUT requests get pre-urlencoded
        self.service.forum(5).suggestion(2).respond({'status': 'foo'})
        self.expect('PUT', '/forums/5/suggestions/2/respond.json',
                    http.urlencode_any({'response[status]': 'foo'}))

        self.service.forum(6).suggestion(5).vote()
        self.expect('POST', '/forums/6/suggestions/5/votes.json',
                    {'to': '1'})

    def test_supporters(self):
        self.service.forum(5).suggestion(2).supporters(sort='newest')
        self.expect('GET', '/forums/5/suggestions/2/supporters.json',
                    {'sort': 'newest'})

    def test_ticket_messages(self):
        self.service.ticket(5).messages().get()
        self.expect('GET', '/tickets/5/ticket_messages.json')

        self.service.ticket(5).messages().create({'foo': 'bar'})
        self.expect('POST', '/tickets/5/ticket_messages.json',
                    {'ticket_message[foo]': 'bar'})

    def test_ticket_notes(self):
        self.service.ticket(3).notes().get()
        self.expect('GET', '/tickets/3/notes.json')

        self.service.ticket(4).notes().create('note text')
        self.expect('POST', '/tickets/4/notes.json',
                    {'note[text]': 'note text'})

        # PUT requests get pre-urlencoded
        self.service.ticket(2).note(3).update('new text')
        self.expect('PUT', '/tickets/2/notes/3.json',
                    http.urlencode_any({'note[text]': 'new text'}))

        self.service.ticket(2).note(6).delete()
        self.expect('DELETE', '/tickets/2/notes/6.json')

    def test_tickets(self):
        self.service.tickets().get()
        self.expect('GET', '/tickets.json')

        self.service.ticket(2).get()
        self.expect('GET', '/tickets/2.json')

        self.service.tickets().create({'foo': 'bar'})
        self.expect('POST', '/tickets.json', {'ticket[foo]': 'bar'})

        # PUT requests get pre-urlencoded
        self.service.ticket(2).update({'foo': 'bar'})
        self.expect('PUT', '/tickets/2.json',
                    http.urlencode_any({'ticket[foo]': 'bar'}))

        self.service.ticket(2).delete()
        self.expect('DELETE', '/tickets/2.json')

        # PUT requests get pre-urlencoded
        self.service.tickets().upsert({'foo': 'bar'})
        self.expect('PUT', '/tickets/upsert.json',
                    http.urlencode_any({'ticket[foo]': 'bar'}))

        self.service.tickets().search(query='foo', page=2)
        self.expect('GET', '/tickets/search.json', {'query': 'foo', 'page': 2})

    def test_topics(self):
        self.service.topics().get()
        self.expect('GET', '/topics.json')

        self.assertRaises(base.MethodNotSupported,
                          self.service.topics().create, {'foo': 'bar'})

        self.service.topic(4).search(query='foo')
        self.expect('GET', '/topics/4/articles/search.json', {'query': 'foo'})

        self.service.topic(4).articles(sort='newest', page=3)
        self.expect('GET', '/topics/4/articles.json',
                    {'sort': 'newest', 'page': 3})

    def test_users(self):
        self.service.users().get()
        self.expect('GET', '/users.json')

        self.service.user(2).get()
        self.expect('GET', '/users/2.json')

        self.service.user().get()
        self.expect('GET', '/users/current.json')

        self.service.users().create({'foo': 'bar'})
        self.expect('POST', '/users.json', {'user[foo]': 'bar'})

        # PUT requests get pre-urlencoded
        self.service.user(2).update({'foo': 'bar'})
        self.expect('PUT', '/users/2.json',
                    http.urlencode_any({'user[foo]': 'bar'}))

        self.service.user(2).delete()
        self.expect('DELETE', '/users/2.json')

        self.service.users().search(query='foo', page=2)
        self.expect('GET', '/users/search.json', {'query': 'foo', 'page': 2})
