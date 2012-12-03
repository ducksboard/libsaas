from libsaas import http, parsers
from libsaas.services import base

from . import resource


class ArticlesBase(resource.UserVoiceResource):

    path = 'articles'

    def wrap_object(self, obj):
        return {'article': obj}


class Articles(ArticlesBase):

    @base.apimethod
    def search(self, page=None, per_page=None, query=None):
        """
        Search for articles.

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


class Article(ArticlesBase):

    @base.apimethod
    def useful(self):
        """
        Mark the article as useful.
        """
        url = '{0}/{1}'.format(self.get_url(), 'useful')

        return http.Request('POST', url), parsers.parse_json
