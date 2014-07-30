from libsaas import http, parsers
from libsaas.services import base

from .resource import NewRelicResource


class Plugins(NewRelicResource):

    path = 'plugins'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, guids=None, ids=None, page=None, detailed=None):
        """
        List of the Plugins associated with your New Relic account.

        :var guids: Filter by guids.
        :vartype guids: str

        :var ids: Filter by ids.
        :vartype ids: str

        :var page: Pagination index.
        :vartype page: int

        :var detailed: If True, include all data about a plugin.
        :vartype detailed: bool
        """
        params = base.get_params(None, locals())
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json


class Plugin(NewRelicResource):

    path = 'plugins'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, detailed=None):
        """
        Fetch a single Plugin.

        :var detailed: If True, include all data about a plugin.
        :vartype detailed: bool
        """
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json
