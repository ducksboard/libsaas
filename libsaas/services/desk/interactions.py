from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Interactions(resource.DeskResource):

    path = 'interactions'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, case_id=None, channels=None, since_created_at=None,
            max_created_at=None, since_updated_at=None, max_updated_at=None,
            since_id=None, max_id=None, count=None, page=None):
        """
        Search interactions based on a combination of parameters with
        pagination.

        Upstream documentation: http://dev.desk.com/docs/api/interactions
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json
