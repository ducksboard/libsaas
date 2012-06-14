from libsaas import http, parsers
from libsaas.services import base


class RecurlyResource(base.RESTResource):

    @base.apimethod
    def get(self, cursor=None, per_page=None):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.

        :var cursor: For collections, where should paging start. If left as
            `None`, the first page is returned.
        :vartype cursor: int

        :var per_page: For collections, how many objects sould be returned. The
            maximum is 200. If left as `None`, 50 objects are returned.
        :vartype per_page: int
        """
        params = base.get_params(('cursor', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_xml

    @base.apimethod
    def create(self, obj):
        """
        Create a new resource.

        :var obj: a Python object representing the resource to be created,
            usually in the same as returned from `get`. Refer to the upstream
            documentation for details.
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_xml

    @base.apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        """
        self.require_item()
        request = http.Request('PUT', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_xml

