from libsaas import http, parsers
from libsaas.services import base


class DeskResource(base.RESTResource):

    path = None

    @base.apimethod
    def update(self, obj):
        self.require_item()
        request = http.Request('PATCH', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def get(self, embed=None, fields=None):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.

        Upstream documentation: http://dev.desk.com/API/using-the-api/
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json


class PaginatedDeskResource(DeskResource):

    @base.apimethod
    def get(self, embed=None, fields=None, per_page=None, page=None):
        """
        Returns a paginated list of elements

        Upstream documentation: http://dev.desk.com/API/using-the-api/
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json
