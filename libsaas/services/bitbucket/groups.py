from libsaas import http, parsers
from libsaas.services import base

from . import resource


class GroupMembersBase(resource.BitBucketResource):

    path = 'members'


class GroupMember(GroupMembersBase):
    pass


class GroupMembers(GroupMembersBase):

    @base.apimethod
    def create(self, username):
        # BitBucket uses PUT to create new group members
        url = '{0}/{1}/'.format(self.get_url(), username)
        return http.Request('PUT', url, '*'), parsers.parse_json


class GroupsBase(resource.BitBucketResource):

    path = 'groups'

    def get_url(self):
        # the groups resource puts the 'groups' part of the path before the
        # user part
        if self.object_id is None:
            return '{0}/{1}/{2}'.format(
                self.parent.parent.get_url(), self.path, self.parent.user_id)

        return '{0}/{1}/{2}/{3}'.format(
            self.parent.parent.get_url(), self.path,
            self.parent.user_id, self.object_id)


class Groups(GroupsBase):
    pass


class Group(GroupsBase):

    @base.resource(GroupMember)
    def member(self, member):
        """
        Return the resource corresponding to a member of the group.
        """
        return GroupMember(self, member)

    @base.resource(GroupMembers)
    def members(self):
        """
        Return the resource corresponding to all members of the group.
        """
        return GroupMembers(self)
