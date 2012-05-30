from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Forks(resource.GitHubResource):

    path = 'forks'

    @base.apimethod
    def get(self, sort='newest', page=None, per_page=None):
        """
        Fetch this repo's forks.

        :var sort: The sort order for the result.
        :vartype sort: str

        :var page: The starting page of the result. If left as `None`, the
            first page is returned.
        :vartype page: int

        :var per_page: The amount of results per page.
        :vartype per_page: int
        """
        params = base.get_params(('sort', 'page', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def create(self):
        """
        Fork this repo.
        """
        request = http.Request('POST', self.get_url())

        return request, parsers.parse_json

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
