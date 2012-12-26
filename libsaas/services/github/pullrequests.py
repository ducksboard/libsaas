from libsaas import http, parsers
from libsaas.services import base

from . import resource


class PullRequests(base.HierarchicalResource):

    path = 'pulls'

    @base.apimethod
    def get(self, state=None, number=None):
        """
        Method lists pull requests.

        :var state: Optional filter pull requests by state  state:
        open or closed (default is open)
        :vartype path: str

        :var number: Optional gets a single pull request
        :vartype number: int
        """
        params = base.get_params(('state',), locals())
        url = self.get_url()

        if number != None:
            url = '{0}/{1}'.format(url, number)

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def get_commits(self, number):
        """
        Method lists commits on a pull request.

        :var number: pull request number
        :vartype number: int
        """
        url = '{0}/{1}/commits'.format(self.get_url(), number)

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def files(self, number):
        """
        Method lists pull requests files.

        :var number: pull request number
        :vartype number: int
        """
        url = '{0}/{1}/files'.format(self.get_url(), number)

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def is_merged(self, number):
        """
        Method gets if a pull request has been merged.

        :var number: pull request number
        :vartype number: int
        """
        url = '{0}/pulls/{1}/merge'.format(self.parent.get_url(), number)

        return http.Request('GET', url), resource.parse_boolean

