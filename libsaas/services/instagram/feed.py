from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Feed(resource.ReadonlyResource):

    path = 'feed'

    @base.apimethod
    def get(self, count=None, min_id=None, max_id=None):
        """
        Fetch all of the objects.

        :var count: Count of media to return.
        :vartype count: int

        :var min_id: Return media later than this min_id.
        :vartype min_id: int

        :var max_id: Return media earlier than this max_id.
        :vartype max_id: int
        """
        params = base.get_params(('count', 'min_id', 'max_id'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
