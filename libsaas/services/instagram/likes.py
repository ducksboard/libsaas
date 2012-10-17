from libsaas import http, parsers
from libsaas.services import base

from . import resource


class LikeBase(resource.InstagramResource):

    path = 'likes'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Likes(LikeBase):

    @base.apimethod
    def create(self):
        """
        Set a like on this media by the currently authenticated user.
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object({}))

        return request, parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Remove a like on this media by the currently authenticated user.
        """
        self.require_collection()
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_empty

