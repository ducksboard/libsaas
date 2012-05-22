import json

from libsaas import http
from libsaas.filters import auth
from libsaas.services import base

from . import authorizations, gists, issues, repos, users


class GitHub(base.Resource):
    """
    """
    def __init__(self, token_or_username, password=None):
        """
        Create a GitHub service.

        :var token_or_username: Either an OAuth 2.0 token, or the username if
          you want to use Basic authentication.
        :vartype token_or_username: str

        :var password: Only used with the Basic authentication, leave this as
            `None` when using OAuth.
        :vartype password: str
        """
        self.apiroot = 'https://api.github.com'

        self.add_filter(self.use_json)

        if password is None:
            self.oauth_token = token_or_username
            self.add_filter(self.add_authorization)
        else:
            self.add_filter(auth.BasicAuth(token_or_username, password))

    def add_authorization(self, request):
        request.headers['Authorization'] = 'token {0}'.format(self.oauth_token)

    def use_json(self, request):
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = json.dumps(request.params)

    def get_url(self):
        return self.apiroot

    @base.resource(authorizations.Authorization)
    def authorization(self, authorization_id):
        """
        Return the resource corresponding to a single authorization.
        Authorizations can only be accessed when using Basic authentication.
        """
        return authorizations.Authorization(self, authorization_id)

    @base.resource(authorizations.Authorizations)
    def authorizations(self):
        """
        Return the resource corresponding to all the authorizations.
        Authorizations can only be accessed when using Basic authentication.
        """
        return authorizations.Authorizations(self)

    @base.resource(gists.Gist)
    def gist(self, gist_id):
        """
        Return the resource corresponding to a single gist.
        """
        return gists.Gist(self, gist_id)

    @base.resource(gists.Gists)
    def gists(self):
        """
        Return the resource corresponding to all the gists.
        """
        return gists.Gists(self)

    @base.resource(issues.Issues)
    def issues(self):
        """
        Return the resource corresponding to all the issues of the
        authenticated user.
        """
        return issues.Issues(self)

    @base.resource(repos.Repo)
    def repo(self, user, repo):
        """
        Return the resource corresponding to a single repo.
        """
        return repos.Repo(self, user, repo)

    @base.resource(repos.Repos)
    def repos(self):
        """
        Return the resource corresponding to all the repos.
        """
        return repos.Repos(self)

    @base.resource(users.User, users.CurrentUser)
    def user(self, name=None):
        """
        Return the resource corresponding to a single user. If `name` is `None`
        the returned resource is the currently authenticated user, otherwise it
        is the user with the given name.
        """
        if name is None:
            return users.CurrentUser(self)
        return users.User(self, name)


Github = GitHub
