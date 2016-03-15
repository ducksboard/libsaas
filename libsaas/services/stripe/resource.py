from libsaas import http, parsers
from libsaas.services import base


class StripeResource(base.RESTResource):

    @base.apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        """
        self.require_item()
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json


class ListResourceMixin(object):

    @base.apimethod
    def get(self, limit=None, ending_before=None,
            starting_after=None):
        """
        Fetch all of the objects.

        :var limit: A limit on the number of objects to be returned.
            Count can range between 1 and 100 objects.
        :vartype count: int

        :var ending_before: A cursor (object ID) for use in pagination. Fetched
            objetcs will be newer than the given object.
        :vartype ending_before: str

        :var starting_after: A cursor (object ID) for use in pagination.
            Fetched objetcs will be older than the given object.
        :vartype starting_after: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
