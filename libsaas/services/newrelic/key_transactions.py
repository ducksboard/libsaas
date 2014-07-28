from libsaas import http, parsers
from libsaas.services import base

from .resource import NewRelicResource


class KeyTransactions(NewRelicResource):

    path = 'key_transactions'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, name=None, ids=None, page=None):
        """
        List of the key transactions associated with your New Relic account.

        :var name: Filter by name.
        :vartype name: str

        :var ids: Filter by ids.
        :vartype ids: str

        :var language: Filter by language.
        :vartype language: str

        :var page: Pagination index.
        :vartype page: int
        """
        params = base.get_params(None, locals())
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json


class KeyTransaction(NewRelicResource):

    path = 'key_transactions'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self):
        """
        Fetch a single key transaction.
        """
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json
