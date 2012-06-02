from libsaas import http, parsers
from libsaas.services import base

from . import resource


class UserRepos(resource.GitHubResource):

    path = 'repos'

    @base.apimethod
    def get(self, type='all', page=None, per_page=None):
        """
        Fetch repos for this user.

        :var type: What type of repos to fetch. For details of allowed values,
            see http://developer.github.com/v3/repos/#list-user-repositories.
        :vartype type: str
        """
        params = base.get_params(('page', 'per_page'), locals())
        params['type'] = type
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class UserEmails(base.HierarchicalResource):

    path = 'emails'

    @base.apimethod
    def get(self):
        """
        Fetch all emails of the authenticated user.
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json

    @base.apimethod
    def add(self, emails):
        """
        Add emails to the authenticated user.

        :var emails: A list of emails to add.
        :vartype emails: list of str
        """
        request = http.Request('POST', self.get_url(), emails)

        return request, parsers.parse_json

    @base.apimethod
    def remove(self, emails):
        """
        Remove emails from the authenticated user.

        :var emails: A list of emails to remove.
        :vartype emails: list of str
        """
        request = http.Request('DELETE', self.get_url(), emails)

        return request, parsers.parse_empty


class UsersBase(resource.GitHubResource):

    path = 'user'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def followers(self, page=None, per_page=None):
        """
        Fetch the followers of this user.
        """
        url = '{0}/{1}'.format(self.get_url(), 'followers')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def following(self, page=None, per_page=None):
        """
        Fetch users that this user is following.
        """
        url = '{0}/{1}'.format(self.get_url(), 'following')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json


class CurrentUser(UsersBase):

    def require_collection(self):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        request = http.Request('PATCH', self.get_url(), obj)

        return request, parsers.parse_json
    update.__doc__ = UsersBase.__doc__

    @base.resource(UserEmails)
    def emails(self):
        """
        Return the resource corresponding to the emails of the authenticated
        user.
        """
        return UserEmails(self)

    @base.apimethod
    def follow(self, name):
        """
        Start following the given user.
        """
        url = '{0}/{1}/{2}'.format(self.get_url(), 'following', name)

        # include a body, because requests does not send content-length when no
        # body is present, and that makes GitHub respond with HTTP 411
        return http.Request('PUT', url, '*'), parsers.parse_empty

    @base.apimethod
    def unfollow(self, name):
        """
        Stop following the given user.
        """
        url = '{0}/{1}/{2}'.format(self.get_url(), 'following', name)

        return http.Request('DELETE', url), parsers.parse_empty

    @base.apimethod
    def follows(self, name):
        """
        Check if the authenticated user follows the given user.

        :return: bool
        """
        url = '{0}/{1}/{2}'.format(self.get_url(), 'following', name)

        return http.Request('GET', url), resource.parse_boolean


class User(UsersBase):

    path = 'users'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(UserRepos)
    def repos(self, page=None, per_page=None):
        """
        Return the resource corresponding to all the repos of this user.
        """
        return UserRepos(self)
