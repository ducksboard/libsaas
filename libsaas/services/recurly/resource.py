from libsaas import http, parsers
from libsaas.services import base


def parse_count(body, code, headers):
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)

    # default to 1 if the header is not present - usually it means that the
    # endpoint returns a single resource and not a collection
    return int(headers.get('x-records', 1))


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
    def count(self, *args, **kwargs):
        """
        Fetch an integer count of the number of objects of a collection. This
        is an absolute number, regardless of paging limits, so use this if you
        want to tally up a collection instead of iterating through all of its
        objects.

        For single-object resources, returns one.

        Accepts the same arguments as `get`.
        """
        with base.extract_request():
            kwargs['per_page'] = 1
            request = self.get(*args, **kwargs)

        return request, parse_count

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
