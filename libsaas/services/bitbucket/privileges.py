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

    @base.apimethod
    def get(self, filter=None):
        url = self.get_url()

        params = base.get_params(('filter', ), locals())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def grant(self, privilege):
        """
        Grant a privilege on the repo.

        :var privilege: The privilege to grant.
        :vartype privilege: str
        """
        request = http.Request('PUT', self.get_url(), privilege)

        return request, parsers.parse_empty

    @base.apimethod
    def revoke(self):
        """
        Revoke privileges on the repo from the user.
        """
        return http.Request('DELETE', self.get_url()), parsers.parse_empty


class GroupPrivileges(resource.BitBucketResource):

    def __init__(self, parent, user, group=None, repo=None):
        self.parent = parent
        self.user = user
        self.group = http.quote_any(group) if group else None
        self.repo = http.quote_any(repo) if repo else None

    @base.apimethod
    def get(self, filter=None, private=None):
        """
        Fetch the group privileges.

        :var filter: Only return specific privileges (read, write, admin).
        :vartype filter: str

        :var private: Only include private repositories.
        :vartype private: bool
        """
        params = base.get_params(('filter', 'private'), locals())
        url = '{0}/group-privileges/{1}/'.format(self.parent.parent.get_url(),
                                                 self.user)

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def grant(self, group, repo, privilege):
        """
        Grant a privilege for a repository to a group.
        """
        url = '{0}/group-privileges/{1}/{2}/{1}/{3}/'.format(
            self.parent.parent.get_url(), self.user, repo, group)

        return http.Request('PUT', url, privilege), parsers.parse_empty

    @base.apimethod
    def revoke(self, group, repo):
        """
        Revoke privileges for a repository from a group.
        """
        url = '{0}/group-privileges/{1}/{2}/{1}/{3}/'.format(
            self.parent.parent.get_url(), self.user, repo, group)

        return http.Request('DELETE', url), parsers.parse_empty

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
