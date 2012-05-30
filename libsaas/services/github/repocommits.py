from libsaas import http, parsers
from libsaas.services import base

from . import resource


class RepoCommitsCommentsBase(resource.GitHubResource):

    path = 'comments'

    def wrap_object(self, obj):
        return {'body': obj}


class RepoCommitsComment(RepoCommitsCommentsBase):

    @base.apimethod
    def get(self, format=None):
        """
        Fetch the comment.

        :var format: Which format should be requested, either `raw`, `text`,
            `html` or `full`. For details on formats, see
            http://developer.github.com/v3/mime/#comment-body-properties.
        """
        params = base.get_params(('format', ), locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json


class RepoCommitsComments(RepoCommitsCommentsBase):

    @base.apimethod
    def get(self, format=None, page=None, per_page=None):
        """
        Fetch all comments for this commit.

        :var format: Which format should be requested, either `raw`, `text`,
            `html` or `full`. For details on formats, see
            http://developer.github.com/v3/mime/#comment-body-properties.
        """
        url = self.get_url()
        params = base.get_params(('page', 'per_page'), locals())
        headers = resource.mimetype_accept(format)

        return http.Request('GET', url, params, headers), parsers.parse_json

    @base.apimethod
    def create(self, comment):
        """
        Create a comment on this commit.

        :var comment: The comment body.
        :vartype comment: str
        """
        url = self.get_url()

        # when creating commits they don't get wrapped in {"body": <comment>}
        return http.Request('POST', url, params=comment), parsers.parse_json


class RepoCommits(base.HierarchicalResource):

    path = 'commits'

    @base.apimethod
    def get(self, sha=None, path=None, page=None, per_page=None):
        """
        Fetch commits for this repo.

        :var sha: Optional commit hash or branch to start listing commits from.
        :vartype sha: str

        :var path: Optional filter to only include commits that include this
            file path.
        :vartype path: str
        """
        params = base.get_params(
            ('sha', 'path', 'page', 'per_page'), locals())
        url = '{0}/{1}'.format(self.parent.get_url(), self.path)

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def compare(self, base, head):
        """
        Fetch the comparison of two commits.

        :var base: The commit hash of the first commit.
        :vartype base: str

        :var head: The commit hash of the second commit.
        :vartype head: str
        """
        url = '{0}/compare/{1}...{2}'.format(self.parent.get_url(), base, head)

        return http.Request('GET', url), parsers.parse_json

    @base.resource(RepoCommitsComments)
    def comments(self):
        """
        Return the resource corresponding to all comments of this commit.
        """
        return RepoCommitsComments(self.parent)

    @base.resource(RepoCommitsComment)
    def comment(self, comment_id):
        """
        Return the resource corresponding to a single comment of this commit.
        """
        return RepoCommitsComment(self.parent, comment_id)


class RepoCommit(base.HierarchicalResource):

    path = 'commits'

    @base.apimethod
    def get(self):
        """
        Fetch all commits from this repo.
        """
        return http.Request('GET', self.get_url()), parsers.parse_json

    @base.resource(RepoCommitsComments)
    def comments(self):
        """
        Return a resource corresponding to all comments of this commit.
        """
        return RepoCommitsComments(self)
