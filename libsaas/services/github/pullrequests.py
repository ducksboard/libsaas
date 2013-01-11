from libsaas import http, parsers
from libsaas.services import base

from . import resource


class PullRequestsBase(resource.GitHubResource):

    path = 'pulls'


class PullRequests(PullRequestsBase):

    @base.apimethod
    def get(self, state=None, page=None, per_page=None):
        """
        Fetch pull requests.

        :var state: Optional filter pull requests by state  state:
            open or closed (default is open)
        :vartype path: str
        """
        params = base.get_params(None, locals())
        url = self.get_url()

        return http.Request('GET', url, params), parsers.parse_json


class PullRequest(PullRequestsBase):

    @base.apimethod
    def commits(self):
        """
        Fetch commits on this pull request.
        """
        url = '{0}/commits'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def files(self):
        """
        Fetch files on this pull request.
        """
        url = '{0}/files'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def is_merged(self):
        """
        Check if this pull request has been merged.
        """
        url = '{0}/merge'.format(self.get_url())

        return http.Request('GET', url), resource.parse_boolean
