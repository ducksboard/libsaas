from libsaas import http, parsers
from libsaas.services import base

from .resource import BasecampResource


class TopicResource(BasecampResource):
    path = 'topics'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Topics(TopicResource):
    pass


class ProjectTopics(TopicResource):

    @base.apimethod
    def get(self, page=None):
        """
        Fetch all topics.

        :var page: the page that will be return.
            If not indicated, first one is returned.
        :vartype page: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
