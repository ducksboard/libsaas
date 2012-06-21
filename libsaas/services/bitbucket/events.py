from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Events(resource.BitBucketResource):

    def __init__(self, parent, user=None, repo=None):
        self.parent = parent
        self.user = user
        self.repo = repo

    def get_url(self):
        url = self.parent.get_url()
        if self.user is not None and self.repo is None:
            url += '/users/{0}/events/'.format(self.user)
        elif self.user is not None and self.repo is not None:
            url += '/repositories/{0}/{1}/events/'.format(self.user, self.repo)

        return url

    @base.apimethod
    def get(self, start=0, limit=15, etype=None):
        """
        Fetch events

        :var start: Event start, default is 0
        :var limit: Event result limit, default is 15
        :var type: Event type, for example 'issue_comment'
        """
        params = resource.get_params(('start', 'limit', 'etype'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
