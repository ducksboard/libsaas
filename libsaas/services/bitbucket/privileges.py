from libsaas import http, parsers
from libsaas.services import base

from . import resource


class RepoPrivileges(resource.BitBucketResource):

    def __init__(self, parent, user, repo, specific_user=None):
        self.parent = parent
        self.user = user
        self.repo = repo
        self.specific_user = specific_user

    def get_url(self):
        url = '{0}/privileges/{1}/'.format(self.parent.parent.get_url(),
                                                                    self.user)

        if self.repo is not None:
            url += '{0}/'.format(self.repo)
        if self.specific_user is not None:
            url += '{0}/'.format(self.specific_user)

        return url

    def wrap_object(self, obj):
        return {'body': obj}

    @base.apimethod
    def get(self, filter=None):
        url = self.get_url()

        params = base.get_params(('filter', ), locals())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def grant(self, obj):
        request = http.Request('PUT', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def revoke(self):
        return http.Request('DELETE', self.get_url()), parsers.parse_json
