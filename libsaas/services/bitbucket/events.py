from libsaas import http, parsers
from libsaas.services import base

from . import resource


class BaseEvents(resource.BitBucketResource):

    path = 'events'


class RepoEvents(BaseEvents):

    @base.apimethod
    def get(self, start=0, limit=10, etype=None):
        """
        Fetch events

        :var start: Event start, default is 0
        :var limit: Event result limit, default is 15
        :var type: Event type, for example 'issue_comment'
        """
        params = resource.get_params(('start', 'limit', 'etype'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class UserEvents(BaseEvents):

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
