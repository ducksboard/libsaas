from libsaas import http, parsers
from libsaas.services import base

from . import resource


class SupportQueueBase(resource.UserVoiceResource):

    path = 'support_queues'

    def wrap_object(self, obj):
        return {'support_queue': obj}


class SupportQueues(SupportQueueBase):

    @base.apimethod
    def get(self, page=None, per_page=None):
        """
        Fetch all the support queues.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def sort(self, order):
        """
        Change the order of support queues.

        :var order: A list of support queue IDs in the desired new ordering.
        :vartype order: list
        """
        params = base.get_params(None, locals())
        url = '{0}/sort'.format(self.get_url())

        request = http.Request('PUT', url, params)

        return request, parsers.parse_json


class SupportQueue(SupportQueueBase):
    pass
