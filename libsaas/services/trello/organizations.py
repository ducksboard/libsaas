from libsaas import http, parsers
from libsaas.services import base

from .resource import (
    serialize_param, TrelloFieldMixin, TrelloFilterMixin,
    TrelloResource, TrelloCollection,
    TrelloReadonlyResource, TrelloReadonlyCollection)


class Actions(TrelloReadonlyCollection):
    path = 'actions'


class Boards(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'boards'


class Members(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'members'


class Member(TrelloResource):
    path = 'members'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class MembersInvited(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'membersInvited'


class Memberships(TrelloReadonlyCollection):
    path = 'memberships'


class Membership(TrelloResource):
    path = 'memberships'


class Organization(TrelloResource, TrelloFieldMixin):
    path = 'organizations'

    @base.apimethod
    def get(self, **kwargs):
        """
        Fetch a single object.

        Upstream documentation:
        https://trello.com/docs/api/organization/index.html
        """
        params = base.get_params(None, kwargs, serialize_param=serialize_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.resource(Actions)
    def actions(self):
        """
        Returns all actions
        """
        return Actions(self)

    @base.resource(Boards)
    def boards(self):
        """
        Returns all boards
        """
        return Boards(self)

    @base.resource(Members)
    def members(self):
        """
        Returns all members
        """
        return Members(self)

    @base.resource(Member)
    def member(self, member_id):
        """
        Returns a single member
        """
        return Member(self, member_id)

    @base.resource(MembersInvited)
    def members_invited(self):
        """
        Returns all invited members
        """
        return MembersInvited(self)

    @base.resource(Memberships)
    def memberships(self):
        """
        Returns all memberships
        """
        return Memberships(self)

    @base.resource(Membership)
    def membership(self, membership_id):
        """
        Returns a single membership
        """
        return Membership(self, membership_id)


class Organizations(TrelloCollection):
    path = 'organizations'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()
