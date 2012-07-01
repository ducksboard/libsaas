from libsaas import http, parsers
from libsaas.services import base

from . import resource


class BaseChangesets(resource.BitBucketResource):

    path = 'changesets'


class Changeset(BaseChangesets):

    @base.apimethod
    def diffstat(self):
        """
        Return the diffstat for this changeset
        """
        url = '{0}/diffstat'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json


class Changesets(BaseChangesets):

    @base.apimethod
    def get(self, start='tip', limit=15):
        """
        Fetch changesets

        :var start: Changesets start default is 'tip'
        :var limit: Limit of changesets, default is 15
        """
        params = base.get_params(('start', 'limit'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
