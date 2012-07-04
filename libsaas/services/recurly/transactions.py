from libsaas import http, parsers
from libsaas.services import base

from . import resource


class TransactionsBase(resource.RecurlyResource):

    path = 'transactions'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Transactions(TransactionsBase):

    @base.apimethod
    def get(self, state=None, type=None, cursor=None, per_page=None):
        """
        Fetch all your transactions.

        :var state: The state of transactions to return:
            "successful", "failed", or "voided".
        :vartype state: str

        :var type: The type of transactions to return:
            "authorization", "refund", or "purchase".
        :vartype type: str
        """
        params = base.get_params(
            ('state', 'type', 'cursor', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_xml


class Transaction(TransactionsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def refund(self, amount_in_cents=None):
        """
        Refund or void a previous, successful transaction.
        """
        self.require_item()

        url = self.get_url()
        params = base.get_params(('amount_in_cents',), locals())
        if params:
            url = url + '?' + http.urlencode_any(params)

        request = http.Request('DELETE', url)

        return request, parsers.parse_empty


class AccountTransactions(TransactionsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()
