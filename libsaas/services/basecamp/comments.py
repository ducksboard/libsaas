from libsaas.services import base

from .resource import BasecampResource


class CommentResource(BasecampResource):
    path = 'comments'


class Comments(CommentResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Comment(CommentResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()
