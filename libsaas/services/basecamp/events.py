from libsaas import http, parsers
from libsaas.services import base

from .resource import BasecampResource


class Events(BasecampResource):
    path = 'events'

    @base.apimethod
    def get(self, since, page=None):
        """
        Fetch all events.

        :var since: a datetime.
        :vartype since: str

        :var page: the page that will be return.
            If not indicated, first one is returned.
        :vartype page: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()
