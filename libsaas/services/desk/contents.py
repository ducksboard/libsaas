from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Translations(resource.PaginatedDeskResource):

    path = 'translations'


class Translation(resource.DeskResource):

    path = 'translations'


class Articles(resource.PaginatedDeskResource):

    path = 'articles'

    @base.apimethod
    def search(self, text=None, topic_ids=None, per_page=None, page=None):
        """
        Perform a search across all public articles.

        Upstream documentation: http://dev.desk.com/API/articles#search
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'search')
        return http.Request('GET', url, params), parsers.parse_json

    @base.resource(Translations)
    def translations(self):
        """
        Return the resource corresponding to the article translations
        """
        return Translations(self)

    @base.resource(Translation)
    def translation(self, translation_id):
        """
        Return the resource corresponding to a single translation
        """
        return Translation(self, translation_id)


class Article(resource.DeskResource):

    path = 'articles'


class Topics(resource.PaginatedDeskResource):

    path = 'topics'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Topic(resource.DeskResource):

    path = 'topics'

    @base.resource(Articles)
    def articles(self):
        """
        Return the resource corresponding to topic articles
        """
        return Articles(self)

    @base.resource(Translations)
    def translations(self):
        """
        Return the resource corresponding to the topic translations
        """
        return Translations(self)

    @base.resource(Translation)
    def translation(self, translation_id):
        """
        Return the resource corresponding to a single translation
        """
        return Translation(self, translation_id)
