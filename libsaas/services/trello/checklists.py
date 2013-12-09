from libsaas import http, parsers
from libsaas.services import base

from .resource import (
    serialize_param, TrelloFieldMixin, TrelloFilterMixin,
    TrelloResource, TrelloCollection,
    TrelloReadonlyResource, TrelloReadonlyCollection)


class Board(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'board'


class Cards(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'cards'


class CheckItems(TrelloCollection):
    path = 'checkItems'


class CheckItem(TrelloResource):
    path = 'checkItems'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Checklist(TrelloResource, TrelloFieldMixin):
    path = 'checklists'

    @base.apimethod
    def get(self, **kwargs):
        """
        Fetch a single object.

        Upstream documentation:
        https://trello.com/docs/api/checklist/index.html
        """
        params = base.get_params(None, kwargs, serialize_param=serialize_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.resource(Board)
    def board(self):
        """
        Returns a single board
        """
        return Board(self)

    @base.resource(Cards)
    def cards(self):
        """
        Returns all cards
        """
        return Cards(self)

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


class Checklists(TrelloCollection):
    path = 'checklists'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()
