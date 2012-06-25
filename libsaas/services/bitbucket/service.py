import json

from libsaas import http
from libsaas.filters import auth
from libsaas.services import base

from . import emails, groups, repositories, invitations, users


class BitBucket(base.Resource):
    """
    """
    def __init__(self, username, password=None):
        """
        Create a BitBucket service.

        :var username: The username for the authenticated user.
        :vartype username: str

        :var password: The password for the authenticated user.
        :vartype password: str
        """
        self.apiroot = 'https://api.bitbucket.org/1.0'

        self.add_filter(auth.BasicAuth(username, password))
        self.add_filter(self.use_json)

    def add_authorization(self, request):
        request.headers['Authorization'] = 'token {0}'.format(self.oauth_token)

    def use_json(self, request):
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = json.dumps(request.params)

    def get_url(self):
        return self.apiroot

    @base.resource(invitations.Invitations)
    def invitations(self, user, repo):
        """
        Perform invitations.
        """
        return invitations.Invitations(self, user, repo)

    @base.resource(emails.Email)
    def email(self, email_id):
        """
        Return the resource corresponding to a single email
        """
        return emails.Email(self, email_id)

    @base.resource(emails.Emails)
    def emails(self):
        """
        Return the resource corresponding to all the emails
        """
        return emails.Emails(self)

    @base.resource(groups.GroupPrivileges)
    def group_privileges(self, user=None, group=None):
        return groups.GroupPrivileges(self, user, group)

    @base.resource(groups.Group)
    def group(self, user, group=None):
        """
        Return the resource corresponding to one group
        """
        return groups.Group(self, user, group)

    @base.resource(groups.Groups)
    def groups(self, user):
        """
        Return the resource corresponding to all the groups
        """
        return groups.Groups(self, user)

    @base.resource(repositories.Repo)
    def repo(self, user, repo=None):
        """
        Return the resource corresponding to one repository
        """
        return repositories.Repo(self, user, repo)

    @base.resource(repositories.Repos)
    def repos(self, user=None, repo=None):
        """
        Return the resource corresponding to all the repositories
        """
        return repositories.Repos(self, user, repo)

    @base.resource(users.User)
    def user(self, user_id=None):
        """
        Return the resource corresponding to all the users
        """
        return users.User(self, user_id)


Bitbucket = BitBucket
