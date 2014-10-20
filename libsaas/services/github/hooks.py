from libsaas import http, parsers
from libsaas.services import base

from . import resource


class RepoHooksBase(resource.GitHubResource):

    path = 'hooks'


class RepoHook(RepoHooksBase):

    @base.apimethod
    def test(self):
        """
        Trigger the hook with the latest push to the repository.
        """
        url = '{0}/tests'.format(self.get_url())
        request = http.Request('POST', url, '')

        return request, parsers.parse_empty

    @base.apimethod
    def ping(self):
        """
        Send a ping event to the hook.
        """
        url = '{0}/pings'.format(self.get_url())
        request = http.Request('POST', url, '')

        return request, parsers.parse_empty



class RepoHooks(RepoHooksBase):
    pass
