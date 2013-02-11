import unittest

from libsaas.executors import test_executor
from libsaas.services import mailchimp


class MailchimpTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = mailchimp.Mailchimp('apikey-us2')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://us2.api.mailchimp.com/1.3' + uri)
        if params:
            self.assertEqual(sorted(self.executor.request.params), sorted(params))
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_serialize(self):
        """
        Verify that parameters are serialized correctly.
        """
        self.service.listBatchSubscribe(3, [{'EMAIL': 'foo@example.com'},
                                            {'EMAIL': 'bar@example.com'}])
        self.expect('POST', '/?method=listBatchSubscribe',
                    (('id', '3'), ('batch[0][EMAIL]', 'foo@example.com'),
                     ('batch[1][EMAIL]', 'bar@example.com'), ('output', 'json'),
                     ('double_optin', 'true'), ('update_existing', 'false'),
                     ('replace_interests', 'true'), ('apikey', 'apikey')))
