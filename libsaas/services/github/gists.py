from libsaas import http, parsers
from libsaas.services import base

from . import resource


class GistCommentsBase(resource.GitHubResource):

    path = 'comments'

    def wrap_object(self, obj):
        return {'body': obj}


class GistComments(GistCommentsBase):

    @base.apimethod
    def get(self, format=None, page=None, per_page=None):
        url = self.get_url()
        params = base.get_params(('page', 'per_page'), locals())
        headers = resource.mimetype_accept(format)

        return http.Request('GET', url, params, headers), parsers.parse_json


class GistComment(GistCommentsBase):

    @base.apimethod
    def get(self, format=None, page=None, per_page=None):
        url = self.get_url()
        params = base.get_params(('page', 'per_page'), locals())
        headers = resource.mimetype_accept(format)

        return http.Request('GET', url, params, headers), parsers.parse_json


class Gists(resource.GitHubResource):

    path = 'gists'

    @base.apimethod
    def public(self, page=None, per_page=None):
        """
        Fetch public gists. The parameters are the same as for `get`.
        """
        url = '{0}/public'.format(self.get_url())
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def starred(self, page=None, per_page=None):
        """
        Fetch gists starred by the authenticated user. The parameters are the
        same as for `get`.
        """
        url = '{0}/starred'.format(self.get_url())
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.resource(GistComment)
    def comment(self, comment_id):
        """
        Return the resource corresponding to a single comment on a gist.

        When updating comments, use a simple string as the parameter to
        `update`, you don't have to use `{"body": <comment body>}`.
        """
        return GistComment(self, comment_id)


class Gist(resource.GitHubResource):

    path = 'gists'

    @base.apimethod
    def star(self):
        """
        Star this gist.
        """
        url = '{0}/{1}'.format(self.get_url(), 'star')

        # include a body, because requests does not send content-length when no
        # body is present, and that makes GitHub respond with HTTP 411
        return http.Request('PUT', url, params='*'), parsers.parse_empty

    @base.apimethod
    def unstar(self):
        """
        Unstar this gist.
        """
        url = '{0}/{1}'.format(self.get_url(), 'star')

        return http.Request('DELETE', url), parsers.parse_empty

    @base.apimethod
    def is_starred(self):
        """
        Check if this gist is starred.

        :return: bool
        """
        url = '{0}/{1}'.format(self.get_url(), 'star')

        return http.Request('GET', url), resource.parse_boolean

    @base.apimethod
    def fork(self):
        """
        Fork this gist.
        """
        url = '{0}/{1}'.format(self.get_url(), 'fork')

        return http.Request('POST', url), parsers.parse_json

    def comments(self):
        """
        Return the resource corresponding to all comments on this gist.

        When creating comments, use a simple string as the parameter to
        `create`, you don't have to use `{"body": <comment body>}`.
        """
        return GistComments(self)
