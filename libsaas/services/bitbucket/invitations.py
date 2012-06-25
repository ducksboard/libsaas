from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Invitations(resource.BitBucketResource):

    path = 'invitations'

    def __init__(self, parent, user, repo):
        self.parent = parent
        self.user = user
        self.repo = repo

    def get_url(self):
        return '{0}/invitations/{1}/{2}'.format(
            self.parent.get_url(), self.user, self.repo)

    @base.apimethod
    def invite(self, email, permission='read'):
        """
        Send invitation with granted permission to an user for a repository

        :var email: The person email that you wish to invite
        :var permission: The permission to grant can be read|write|admin
        """
        url = '{0}/{1}'.format(self.get_url(), email)
        params = base.get_params(('permission', ), locals())
        request = http.Request('PUT', url, params)

        return request, parsers.parse_json
