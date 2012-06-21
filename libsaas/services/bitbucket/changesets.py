from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Changesets(resource.BitBucketResource):

    def __init__(self, parent, user, repo, commit=None):
        self.parent = parent
        self.user = user
        self.repo = repo
        self.commit = commit

    def get_url(self):
        url = '{0}/{1}/{2}/changesets'.format(
            self.parent.get_url(), self.user, self.repo)
        if self.commit is not None:
            url += '/{0}/diffstat'.format(self.commit)

        return url

    @base.apimethod
    def get(self, start='tip', limit=15):
        """
        Fetch changesets

        :var start: Changesets start default is 'tip'
        :var limit: Limit of changesets, default is 15
        """
        params = resource.get_params(('start', 'limit'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
