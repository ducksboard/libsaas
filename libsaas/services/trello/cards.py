from libsaas import http, parsers, port
from libsaas.services import base

from .resource import (
    serialize_param, TrelloFieldMixin,
    TrelloResource, TrelloCollection,
    TrelloReadonlyResource, TrelloReadonlyCollection)


class Comments(TrelloCollection):
    path = 'comments'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        request = http.Request('PUT', self.get_url(), self.wrap_object(obj))
        return request, parsers.parse_json

    @base.apimethod
    def delete(self):
        request = http.Request('DELETE', self.get_url())
        return request, parsers.parse_empty


class Actions(TrelloReadonlyCollection):
    path = 'actions'

    @base.resource(Comments)
    def comments(self):
        """
        Returns all comments
        """
        return Comments(self)


class Attachments(TrelloCollection):
    path = 'attachments'


class Attachment(TrelloResource):
    path = 'attachments'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Board(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'board'


class CheckItemStates(TrelloReadonlyCollection):
    path = 'checkItemStates'


class CheckItems(TrelloCollection):
    path = 'checkItem'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class CheckItem(TrelloResource):
    path = 'checkItem'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def convert_to_card(self):
        """
        Converts checkitem to card.
        """
        url = '{0}/convertToCard'.format(self.get_url())
        request = http.Request('POST', url)
        return request, parsers.parse_json


class Checklists(TrelloCollection):
    path = 'checklists'


class Checklist(TrelloReadonlyResource):
    path = 'checklist'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(CheckItems)
    def checkitems(self):
        """
        Returns all checkitems
        """
        return CheckItems(self)

    @base.resource(CheckItem)
    def checkitem(self, checkitem_id):
        """
        Returns a single checkitem
        """
        return CheckItem(self, checkitem_id)


class List(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'list'


class Members(TrelloReadonlyCollection):
    path = 'members'


class MembersVoted(TrelloCollection):
    path = 'membersVoted'


class Stickers(TrelloCollection):
    path = 'stickers'


class Sticker(TrelloResource):
    path = 'stickers'


class Labels(TrelloCollection):
    path = 'labels'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Label(TrelloResource):
    path = 'labels'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Card(TrelloResource, TrelloFieldMixin):
    path = 'cards'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, **kwargs):
        params = base.get_params(None, kwargs, serialize_param=serialize_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def mark_as_read(self):
        """
        Marks associated notification as read.
        """
        url = '{0}/markAssociatedNotificationsRead'.format(self.get_url())
        request = http.Request('POST', url)
        return request, parsers.parse_json

    @base.resource(Actions)
    def actions(self):
        """
        Returns all actions
        """
        return Actions(self)

    @base.resource(Attachments)
    def attachments(self):
        """
        Returns all attachments
        """
        return Attachments(self)

    @base.resource(Attachment)
    def attachment(self, attachment_id):
        """
        Returns a single checklist
        """
        return Attachment(self, attachment_id)

    @base.resource(Board)
    def board(self):
        """
        Returns a single board
        """
        return Board(self)

    @base.resource(CheckItemStates)
    def checkitem_states(self):
        """
        Returns all checkitem states
        """
        return CheckItemStates(self)

    @base.resource(Checklists)
    def checklists(self):
        """
        Returns all checklists
        """
        return Checklists(self)

    @base.resource(Checklist)
    def checklist(self, checklist_id):
        """
        Returns a single checklist
        """
        return Checklist(self, checklist_id)

    @base.resource(List)
    def list(self):
        """
        Returns a single list
        """
        return List(self)

    @base.resource(Members)
    def members(self):
        """
        Returns all members
        """
        return Members(self)

    @base.resource(MembersVoted)
    def members_voted(self):
        """
        Returns all voted members
        """
        return MembersVoted(self)

    @base.resource(Stickers)
    def stickers(self):
        """
        Returns all stickers
        """
        return Stickers(self)

    @base.resource(Sticker)
    def sticker(self, sticker_id):
        """
        Returns a single sticker
        """
        return Sticker(self, sticker_id)

    @base.resource(Labels)
    def labels(self):
        """
        Returns all labels
        """
        return Labels(self)

    @base.resource(Label)
    def label(self, color):
        """
        Returns a single label
        """
        return Label(self, color)


class Cards(TrelloCollection):
    path = 'cards'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


port.method_func(Card, 'get').__doc__ = """
Fetch a single object.

Upstream documentation:
https://trello.com/docs/api/card/index.html#get-1-cards-card-id-or-shortlink
"""
