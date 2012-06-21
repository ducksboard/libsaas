from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Privileges(resource.BitBucketResource):

    def __init__(self, parent, user, repo=None, specificuser=None):
        self.parent = parent
        self.user = user
        self.repo = repo
        self.specificuser = specificuser

    def get_url(self):
        url = '{0}/privileges/{1}/'.format(self.parent.get_url(), self.user)
        if self.repo is not None:
            url += '{0}/'.format(self.repo)
        if self.specificuser is not None:
            url += '{0}/'.format(self.specificuser)

        return url

    @base.apimethod
    def get(self, filter=None):
        """
        Fetch privileges

        :var filter: Can be one of read|write|admin to limit results
        """
        params = resource.get_params(('filter', ), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def grant(self, level='read'):
        """
        Grant privileges on this rsource.

        :var level: The privileges level for this user to use the repository
            can be one of read|write|admin
        """
        return \
            http.Request('PUT', self.get_url(), level), resource.parse_boolean

    @base.apimethod
    def revoke(self):
        """
        Revoke privileges on this resource.

        You can revoque privileges for users, repositories or full owner domain
        """
        return http.Request('DELETE', self.get_url()), resource.parse_boolean


class Invitations(resource.BitBucketResource):

    def __init__(self, parent, user, repo, address):
        self.parent = parent
        self.user = user
        self.repo = repo
        self.address = address

    def get_url(self):
        return '{0}/invitations/{1}/{2}/{3}'.format(
            self.parent.get_url(), self.user, self.repo, self.address)

    @base.apimethod
    def invite(self, permission='read'):
        """
        Send invitation with granted permission to an user for a repository

        :var permission: The permission to grant can be read|write|admin
        """
        url = self.get_url()
        request = http.Request('PUT', url, permission)

        return request, parsers.parse_json
