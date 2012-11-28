from libsaas import http, parsers
from libsaas.services import base


class DeskResource(base.RESTResource):

    path = None

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class PaginatedDeskResource(DeskResource):

    @base.apimethod
    def get(self, count=None, page=None):
        """
        Returns a paginated list of elements

        Upstream documentation: http://dev.desk.com/docs/api/articles
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json
