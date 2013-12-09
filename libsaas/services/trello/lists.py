from libsaas import http, parsers, port
from libsaas.services import base

from .resource import (
    serialize_param, TrelloFieldMixin, TrelloFilterMixin,
    TrelloResource, TrelloCollection,
    TrelloReadonlyResource, TrelloReadonlyCollection)


class Actions(TrelloReadonlyCollection):
    path = 'actions'


class Board(TrelloReadonlyResource, TrelloFieldMixin):
    path = 'board'


class Cards(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'cards'


class List(TrelloResource, TrelloFieldMixin):
    path = 'lists'

    @base.apimethod
    def get(self, **kwargs):
        """
        Fetch a single object.

        Upstream documentation:
        https://trello.com/docs/api/list/index.html
        """
        params = base.get_params(None, kwargs, serialize_param=serialize_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def archive_all_cards(self):
        """
        Archive all list cards.
        """
        url = '{0}/archiveAllCards'.format(self.get_url())
        request = http.Request('POST', url)
        return request, parsers.parse_json

    @base.resource(Actions)
    def actions(self):
        """
        Returns all actions
        """
        return Actions(self)

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


class Lists(TrelloCollection):
    path = 'lists'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


port.method_func(List, 'get').__doc__ = """
Fetch a single object.

Upstream documentation:
https://trello.com/docs/api/list/index.html#get-1-lists-idlist
"""
