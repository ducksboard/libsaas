from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Groups(resource.BitBucketResource):

    def __init__(self, parent, user):
        self.parent = parent
        self.user = user

    def get_url(self):
        url = '{0}/groups'.format(self.parent.get_url())
        if self.user is not None:
            url += '/{0}'.format(self.user)

        return url


class Group(resource.BitBucketResource):

    def __init__(self, parent, user, group=None):
        self.parent = parent
        self.user = user
        self.group = group

    def get_url(self):
        url = '{0}/groups'.format(self.parent.get_url())
        if self.user is not None:
            url += '/{0}'.format(self.user)
        if self.group is not None:
            url += '/{0}'.format(self.group)

        return url

    @base.apimethod
    def get(self):
        """
        Fetch groups

        :var group: Group name where to search
        """
        url = '{0}/members'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json

    @base.apimethod
    def create(self, obj):
        """
        Create a new Group.

        :var obj: a Python object with the needed params
        """
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def update(self, obj):
        """
        Update this Group.

        :var obj: a Python object with the update params
        """
        request = http.Request('PUT', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete(self, username=None):
        """
        Delete this Group.

        :var username: Optional Python string to delete an user from a group
        """
        url = self.get_url()
        if username is not None:
            url += '/members/{0}'.format(username)
        request = http.Request('DELETE', url)

        return request, parsers.parse_json

    @base.apimethod
    def add(self, username):
        """
        Adds an user to the Group

        :var username: a Python string that represents the group name
        """
        url = '{0}/members/{1}'.format(self.get_url(), username)
        request = http.Request('PUT', url)

        return request, parsers.parse_json


class GroupPrivileges(resource.BitBucketResource):

    def __init__(self, parent, user=None, group=None):
        self.parent = parent
        self.user = user
        self.group = group

    def get_url(self):
        url = '{0}/group-privileges'.format(self.parent.get_url())
        if self.user is not None:
            url += '/{0}'.format(self.user)
        if self.group is not None:
            url += '/{0}'.format(self.group)

        url += '/'

        return url

    @base.apimethod
    def get(self, filter=None, private=False):
        """
        Fetch group privileges

        :var filter: Can be one of read|write|admin to limit results
        :var private: Can be used to only include private repositories
        """
        params = resource.get_params(('filter', 'private'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def grant(self, group=None, privilege='read'):
        """
        Grant privileges to users to a repository

        :var privilege: The privilege to assign, can be read|write|admin
        """
        url = self.get_url()
        if privilege is not None and group is not None:
            url += '/{0}'.format(group)
        request = http.Request('PUT', url, privilege)

        return request, parsers.parse_json
