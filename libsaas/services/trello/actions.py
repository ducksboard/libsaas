from libsaas import http, parsers
from libsaas.services import base

from .resource import (
    serialize_param, TrelloFieldMixin,
    TrelloResource, TrelloReadonlyResource)


class Board(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'board'


class Card(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'card'


class List(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'list'


class Member(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'member'


class MemberCreator(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'memberCreator'


class Organization(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'organization'


class Action(TrelloResource, TrelloFieldMixin):
    path = 'actions'

    @base.apimethod
    def get(self, fields=None, entities=None, member=None, member_fields=None,
            memberCreator=None, memberCreator_fields=None):
        """
        Fetch a single object.

        Upstream documentation:
        https://trello.com/docs/api/action/index.html#get-1-actions-idaction
        """
        self.require_item()

        params = base.get_params(
            None, locals(), serialize_param=serialize_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


    @base.resource(Board)
    def board(self):
        """
        Returns a single board
        """
        return Board(self)

    @base.resource(Card)
    def card(self):
        """
        Returns a single card
        """
        return Card(self)

    @base.resource(List)
    def list(self):
        """
        Returns a single list
        """
        return List(self)

    @base.resource(Member)
    def member(self):
        """
        Returns a single member
        """
        return Member(self)

    @base.resource(MemberCreator)
    def creator(self):
        """
        Returns a single creator
        """
        return MemberCreator(self)

    @base.resource(Organization)
    def organization(self):
        """
        Returns a single organization
        """
        return Organization(self)
