from libsaas import http, parsers
from libsaas.services import base

from . import groups, privileges, resource


class User(resource.BitBucketResource):

    def __init__(self, parent, user_id=None):
        self.parent = parent
        self.user_id = user_id

    def get_url(self):
        if self.user_id is None:
            return '{0}/user'.format(self.parent.get_url())

        return '{0}/users/{1}'.format(self.parent.get_url(), self.user_id)

    @base.apimethod
    def follows(self):
        """
        Fetch the list of repositories the authenticated user follows.
        """
        request = http.Request('GET', '{0}/follows/'.format(self.get_url()))

        return request, parsers.parse_json

    @base.apimethod
    def followers(self):
        """
        Fetch the followers of this user.
        """
        request = http.Request('GET', '{0}/followers/'.format(self.get_url()))

        return request, parsers.parse_json

    @base.apimethod
    def events(self, start=0, limit=15, etype=None):
        """
        Fetch events for this user.

        :var start: Event start, default is 0.
        :var limit: Event result limit, default is 15.
        :var type: Event type, for example 'issue_comment'.
        """
        params = base.get_params(('start', 'limit', 'etype'), locals())
        url = '{0}/events/'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.resource(groups.Group)
    def group(self, group_name):
        """
        Return a resource corresponding a single user's groups.

        This resource only exists for User resources that specify a concrete
        username.
        """
        if not self.user_id:
            raise base.MethodNotSupported()

        return groups.Group(self, group_name)

    @base.resource(groups.Groups)
    def groups(self):
        """
        Return a resource corresponding to all of the user's groups.

        This resource only exists for User resources that specify a concrete
        username.
        """
        if not self.user_id:
            raise base.MethodNotSupported()

        return groups.Groups(self)

    @base.resource(privileges.GroupPrivileges)
    def group_privileges(self, group=None, repo=None):
        """
        Return a resource corresponding to the group privileges for a user.

        This resource only exists for User resources that specify a concrete
        username.
        """
        if not self.user_id:
            raise base.MethodNotSupported()

        return privileges.GroupPrivileges(self, self.user_id, group, repo)
