from libsaas.filters import auth
from libsaas.services import base

from . import emails, repositories, users


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
        # although not consistent throughout the documentation, BitBucket
        # resources seem to end with a trailing slash, regardless of whether
        # they represent a single object or a collection
        self.add_filter(self.add_trailing_slash)

    def add_trailing_slash(self, request):
        if not '?' in request.uri and not request.uri.endswith('/'):
            request.uri += '/'

    def get_url(self):
        return self.apiroot

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

    @base.resource(repositories.Repo)
    def repo(self, user, repo):
        """
        Return the resource corresponding to one repository
        """
        return repositories.Repo(self, user, repo)

    @base.resource(repositories.Repos)
    def repos(self):
        """
        Return the resource corresponding to all the repositories
        """
        return repositories.Repos(self)

    @base.resource(users.User)
    def user(self, user_id=None):
        """
        Return the resource corresponding to all the users
        """
        return users.User(self, user_id)


Bitbucket = BitBucket
