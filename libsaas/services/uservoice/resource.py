from libsaas import http, parsers
from libsaas.services import base


class UserVoiceResource(base.RESTResource):

    @base.apimethod
    def get(self, page=None, per_page=None, sort=None):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.

        :var page: For collections, where should paging start. If left as
            `None`, the first page is returned.
        :vartype page: int

        :var per_page: For collections, how many objects sould be returned. If
            left as `None`, 10 objects are returned.
        :vartype per_page: int

        :var sort: For collections, how should the returned collection be
            sorted. Refer to upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def create(self, obj):
        """
        Create a new resource.

        :var obj: a Python dictionary representing the resource to be created,
            in the same as returned from `get`, but one level less nested. For
            instance, if `get` returns `{'forum': {'name': 'Forum Name'}}`,
            then `obj` should be `{'name': 'New Forum'}`.

            Refer to the upstream documentation for details.
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python dictionary representing the resource to be created,
            in the same as returned from `get`, but one level less nested. For
            instance, if `get` returns `{'forum': {'name': 'Forum Name'}}`,
            then `obj` should be `{'name': 'New Forum'}`.

            Refer to the upstream documentation for details.
        """
        self.require_item()
        request = http.Request('PUT', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json


class UserVoiceTextResource(UserVoiceResource):

    @base.apimethod
    def create(self, text):
        """
        Create a new resource.

        :var text: the text of the resource to be created.
        :vartype text: str
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object(text))

        return request, parsers.parse_json

    @base.apimethod
    def update(self, text):
        """
        Update this resource.

        :var text: the new text of the resource.
        :vartype text: str
        """
        self.require_item()
        request = http.Request('PUT', self.get_url(), self.wrap_object(text))

        return request, parsers.parse_json
