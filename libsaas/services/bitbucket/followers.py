from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Followers(resource.BitBucketResource):

    def __init__(self, parent, user=None, repo=None, issue=None):
        self.parent = parent
        self.user = user
        self.repo = repo
        self.issue = issue

    def get_url(self):
        url = '{0}/repositories'.format(self.parent.get_url())
        if self.user is not None and self.repo is not None:
            url += '/{0}/{1}'.format(self.user, self.repo)
        if self.issue is not None:
            url += '/issues/{0}'.format(self.issue)

        url += '/followers/'
        return url

    @base.apimethod
    def follows(self):
        """
        Return the users that you follow
        """
        request = http.Request('GET', '{0}/user/follows/'.format(
                                                        self.parent.get_url()))
        return request, parsers.parse_json
