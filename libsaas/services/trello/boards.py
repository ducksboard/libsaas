from libsaas import http, parsers
from libsaas.services import base

from .resource import (
    serialize_param, TrelloFieldMixin, TrelloFilterMixin,
    TrelloResource, TrelloCollection,
    TrelloReadonlyResource, TrelloReadonlyCollection)


class Actions(TrelloReadonlyCollection):
    path = 'actions'


class Card(TrelloReadonlyResource):
    path = 'cards'


class Cards(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'cards'


class Checklists(TrelloCollection):
    path = 'checklists'


class Lists(TrelloCollection, TrelloFilterMixin):
    path = 'lists'


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

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Organization(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'organization'


class Board(TrelloResource, TrelloFieldMixin):
    path = 'boards'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, **kwargs):
        """
        Fetch a single object.

        Upstream documentation:
        https://trello.com/docs/api/board/index.html#get-1-boards-board-id
        """
        params = base.get_params(None, kwargs, serialize_param=serialize_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def calendar_key(self):
        """
        Generates a calendar key.
        """
        url = '{0}/calendarKey/generate'.format(self.get_url())
        request = http.Request('POST', url)
        return request, parsers.parse_json

    @base.apimethod
    def email_key(self):
        """
        Generates a email key.
        """
        url = '{0}/emailKey/generate'.format(self.get_url())
        request = http.Request('POST', url)
        return request, parsers.parse_json

    @base.apimethod
    def mark_as_viewed(self):
        """
        Marks board as viewed.
        """
        url = '{0}/markAsViewed'.format(self.get_url())
        request = http.Request('POST', url)
        return request, parsers.parse_json

    @base.resource(Actions)
    def actions(self):
        """
        Returns all actions
        """
        return Actions(self)

    @base.resource(Card)
    def card(self, card_id):
        """
        Returns a single card
        """
        return Card(self, card_id)

    @base.resource(Cards)
    def cards(self):
        """
        Returns all cards
        """
        return Cards(self)

    @base.resource(Checklists)
    def checklists(self):
        """
        Returns all checklists
        """
        return Checklists(self)

    @base.resource(Lists)
    def lists(self):
        """
        Returns all lists
        """
        return Lists(self)

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

    @base.resource(Organization)
    def organization(self):
        """
        Returns a single organization
        """
        return Organization(self)


class Boards(TrelloCollection):
    path = 'boards'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()
