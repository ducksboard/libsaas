from libsaas import http, parsers
from libsaas.services import base


class FiltersResource(base.RESTResource):

    path = 'filters'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Filters(FiltersResource):

    @base.apimethod
    def get(self, type=None):
        """
        Returns all filters.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Filters
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple filters as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Filters
        """
        params = base.get_params(None, locals())
        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json


class Filter(FiltersResource):
    pass
