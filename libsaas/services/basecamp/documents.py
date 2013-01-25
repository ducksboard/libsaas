from libsaas.services import base

from .resource import BasecampResource
from . import comments as c


class DocumentResource(BasecampResource):
    path = 'documents'


class Documents(DocumentResource):
    pass


class GlobalDocuments(DocumentResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Document(DocumentResource):

    @base.resource(c.Comments)
    def comments(self):
        """
        Return the resource corresponding to all comments.
        """
        return c.Comments(self)
