from libsaas import http, parsers
from libsaas.services import base

from .resource import NewRelicResource


class Users(NewRelicResource):

    path = 'users'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, ids=None, email=None, page=None):
        """
        List of all Users.

        :var ids: Filter by ids.
        :vartype ids: str

        :var email: Filter by email.
        :vartype email: str

        :var page: Pagination index.
        :vartype page: int
        """
        params = base.get_params(None, locals())
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json


class User(NewRelicResource):

    path = 'users'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self):
        """
        Fetch a single User.
        """
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json
