from libsaas.services import base

from . import resource


class CommentBase(resource.InstagramResource):

    path = 'comments'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Comments(CommentBase):

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Comment(CommentBase):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()
