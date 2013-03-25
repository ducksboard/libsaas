from libsaas import http, parsers
from libsaas.services import base


class Authorizations(base.HierarchicalResource):

    path = 'authorizations'

    @base.apimethod
    def get(self, email, password):
        """
        Returns all authorizations for a particular user.
        Authorization objects contain the API tokens the user has with
        different company accounts in Pipedrive.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Authorizations
        """
        params = base.get_params(None, locals())

        return http.Request('POST', self.get_url(), params), parsers.parse_json


class UserConnections(base.HierarchicalResource):

    path = 'userConnections'

    @base.apimethod
    def get(self):
        """
        Returns data about all connections for the authorized user.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-UserConnections
        """
        return http.Request('GET', self.get_url()), parsers.parse_json


class UsersResource(base.RESTResource):

    path = 'users'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Users(UsersResource):

    @base.apimethod
    def find(self, term):
        """
        Searches all users by their name.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Users
        """
        params = base.get_params(None, locals())
        url = '{0}/find'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class User(UsersResource):

    @base.apimethod
    def merge(self, merge_with_id):
        """
        Merges a user with another user.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Users
        """
        params = base.get_params(None, locals())
        url = '{0}/merge'.format(self.get_url())
        return http.Request('POST', url, params), parsers.parse_json

    @base.apimethod
    def activities(self, start=None, limit=None, done=None, exclude=None):
        """
        Lists activities associated with a user.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Users
        """
        params = base.get_params(None, locals())
        url = '{0}/activities'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def followers(self):
        """
        Lists the followers of a user.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Users
        """
        url = '{0}/followers'.format(self.get_url())
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def updates(self, start=None, limit=None):
        """
        Lists updates about a user.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Users
        """
        params = base.get_params(None, locals())
        url = '{0}/updates'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json
