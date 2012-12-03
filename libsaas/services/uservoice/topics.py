from libsaas import http, parsers
from libsaas.services import base

from . import resource


class TopicsBase(resource.UserVoiceResource):

    path = 'topics'

    def get_url(self):
        if self.object_id is None:
            return '{0}/{1}'.format(self.parent.get_url(), self.path)

        return '{0}/{1}/{2}/articles'.format(self.parent.get_url(), self.path,
                                             self.object_id)


class Topics(TopicsBase):

    def create(self, obj):
        raise base.MethodNotSupported()


class Topic(TopicsBase):

    def get(self):
        raise base.MethodNotSupported()

    def update(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def articles(self, page=None, per_page=None, sort=None):
        """
        Fetch the articles on a given topic.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def search(self, page=None, per_page=None, query=None):
        """
        Search for articles on a given topic.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var query: Search string.
        :vartype query: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'search')

        return http.Request('GET', url, params), parsers.parse_json
