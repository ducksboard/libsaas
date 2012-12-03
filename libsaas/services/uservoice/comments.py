from libsaas import http, parsers
from libsaas.services import base

from . import resource, flags


class CommentsBase(resource.UserVoiceTextResource):

    path = 'comments'

    def wrap_object(self, name):
        return {'comment': {'text': name}}


class Comments(CommentsBase):

    def create(self, obj):
        raise base.MethodNotSupported()


class ForumSuggestionComment(CommentsBase):

    @base.resource(flags.SuggestionCommentFlags)
    def flags(self):
        """
        Return the resource corresponding to all the flags of this comment.
        """
        return flags.SuggestionCommentFlags(self)


class ForumSuggestionComments(CommentsBase):

    @base.apimethod
    def get(self, page=None, per_page=None, filter=None, sort=None):
        """
        Fetch comments on this suggestion.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var filter: The kind of comments to return, see upstream
            documentation for possible values.
        :vartype filter: str

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class UserComments(CommentsBase):

    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, page=None, per_page=None, filter=None, sort=None):
        """
        Fetch comments from this user.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var filter: The kind of comments to return, see upstream
            documentation for possible values.
        :vartype filter: str

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
