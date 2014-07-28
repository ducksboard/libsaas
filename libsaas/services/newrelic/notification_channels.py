from libsaas import http, parsers
from libsaas.services import base

from .resource import NewRelicResource


class NotificationChannels(NewRelicResource):

    path = 'notification_channels'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, type=None, ids=None, page=None):
        """
        List of the Notification Channels associated with your New Relic
        account.

        :var name: Filter by name.
        :vartype name: str

        :var type: Filter by notification channel types.
        :vartype type: str

        :var ids: Filter by ids.
        :vartype ids: str

        :var page: Pagination index.
        :vartype page: int
        """
        params = base.get_params(None, locals())
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json


class NotificationChannel(NewRelicResource):

    path = 'notification_channels'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self):
        """
        Fetch a single Notification Channel.
        """
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json
