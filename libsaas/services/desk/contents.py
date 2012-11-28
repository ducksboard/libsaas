from libsaas.services import base

from . import resource


class Articles(resource.PaginatedDeskResource):

    path = 'articles'


class Article(base.RESTResource):

    path = 'articles'


class Topics(resource.PaginatedDeskResource):

    path = 'topics'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Topic(base.RESTResource):

    path = 'topics'

    @base.resource(Articles)
    def articles(self):
        """
        Return the resource corresponding to topic articles
        """
        return Articles(self)
