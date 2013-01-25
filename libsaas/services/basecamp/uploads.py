from libsaas.services import base

from .resource import BasecampResource
from . import comments as c

class UploadResource(BasecampResource):
    path = 'uploads'


class Uploads(UploadResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Upload(UploadResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(c.Comments)
    def comments(self):
        """
        Return the resource corresponding to all comments.
        """
        return c.Comments(self)
