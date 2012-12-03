from libsaas import http, parsers
from libsaas.services import base

from . import resource


class CustomFields(resource.UserVoiceResource):

    path = 'custom_fields'

    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, page=None, per_page=None, filter=None, sort=None):
        """
        Fetch all custom fields.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var filter: The kind of fields to return, see upstream
            documentation for possible values.
        :vartype filter: str

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def public(self, page=None, per_page=None, sort=None):
        """
        Fetch public custom fields.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var filter: The kind of fields to return, see upstream
            documentation for possible values.
        :vartype filter: str

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        url = '{0}/public'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json
