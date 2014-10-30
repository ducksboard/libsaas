from libsaas import http, parsers
from libsaas.services import base

from . import resource


class MembersBase(resource.GitHubResource):

    path = 'members'


class Members(MembersBase):
    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Member(MembersBase):
    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class PublicMembersBase(resource.GitHubResource):

    path = 'public_members'


class PublicMembers(PublicMembersBase):
    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class PublicMember(PublicMembersBase):
    @base.apimethod
    def publicize(self):
        request = http.Request('PUT', self.get_url())

        return request, parsers.parse_json

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class UserMembership(resource.GitHubResource):
    @base.apimethod
    def get(self):
        request = http.Request('GET',
            '{0}/{1}'.format(self.parent.get_url(), self.object_id))

        return request, parsers.parse_json

    @base.apimethod
    def update(self, obj):
        request = http.Request('PATCH',
            '{0}/{1}'.format(self.parent.get_url(), self.object_id),
            obj)

        return request, parsers.parse_json


class UserMemberships(resource.GitHubResource):

    path = 'memberships/orgs'

    @base.apimethod
    def get(self, state=None):
        """
        List your organization memberships.

        :var state: Specify whether only active or pending
            memberships are returned. If left as `None`,
            all memberships are returned.
        :vartype state: str
        """
        params = base.get_params(('state',), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.resource(UserMembership)
    def org(self, org):
        """
        Return the resource corresponding to the current user's
        membership of the specified organization.
        """
        return UserMembership(self, org)
