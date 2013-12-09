from libsaas import http, parsers
from libsaas.services import base

from .resource import (
    serialize_param, TrelloFieldMixin, TrelloFilterMixin,
    TrelloResource, TrelloCollection, TrelloReadonlyCollection)


class Actions(TrelloReadonlyCollection):
    path = 'actions'


class BoardBackgrounds(TrelloCollection):
    path = 'boardBackgrounds'


class BoardBackground(TrelloResource):
    path = 'boardBackgrounds'


class BoardStars(TrelloCollection):
    path = 'boardStars'

    @base.apimethod
    def get(self):
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json


class BoardStar(TrelloResource):
    path = 'boardStars'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class CustomBoardBackgrounds(TrelloCollection):
    path = 'customBoardBackgrounds'


class CustomBoardBackground(TrelloResource):
    path = 'customBoardBackgrounds'


class CustomStickers(TrelloCollection):
    path = 'customStickers'


class CustomSticker(TrelloResource):
    path = 'customStickers'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Boards(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'boards'


class Cards(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'cards'


class Notifications(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'notifications'


class Organizations(TrelloReadonlyCollection, TrelloFilterMixin):
    path = 'organizations'


class Sessions(TrelloReadonlyCollection):
    path = 'sessions'


class Tokens(TrelloReadonlyCollection):
    path = 'tokens'


class Member(TrelloResource, TrelloFieldMixin):
    path = 'members'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, **kwargs):
        """
        Fetch a single object.

        Upstream documentation:
        https://trello.com/docs/api/member/index.html
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

    @base.resource(BoardBackgrounds)
    def board_backgrounds(self):
        """
        Returns all board backgrounds
        """
        return BoardBackgrounds(self)

    @base.resource(BoardBackgrounds)
    def board_background(self, board_background_id):
        """
        Returns a single board background
        """
        return BoardBackground(self, board_background_id)

    @base.resource(BoardStars)
    def board_stars(self):
        """
        Returns all board stars
        """
        return BoardStars(self)

    @base.resource(BoardStar)
    def board_star(self, board_star_id):
        """
        Returns a single board star
        """
        return BoardStar(self, board_star_id)

    @base.resource(CustomBoardBackgrounds)
    def custom_board_backgrounds(self):
        """
        Returns all custom board backgrounds
        """
        return CustomBoardBackgrounds(self)

    @base.resource(CustomBoardBackground)
    def custom_board_background(self, board_background_id):
        """
        Returns a single custom board background
        """
        return CustomBoardBackground(self, board_background_id)

    @base.resource(CustomStickers)
    def custom_stickers(self):
        """
        Returns all custom stickers
        """
        return CustomStickers(self)

    @base.resource(CustomSticker)
    def custom_sticker(self, sticker_id):
        """
        Returns a single custom stickers
        """
        return CustomSticker(self, sticker_id)

    @base.resource(Notifications)
    def notifications(self):
        """
        Returns all notifications
        """
        return Notifications(self)

    @base.resource(Organizations)
    def organizations(self):
        """
        Returns all organizations
        """
        return Organizations(self)

    @base.resource(Boards)
    def boards(self):
        """
        Returns all boards
        """
        return Boards(self)

    @base.resource(Cards)
    def cards(self):
        """
        Returns all cards
        """
        return Cards(self)

    @base.resource(Sessions)
    def sessions(self):
        """
        Returns all sessions
        """
        return Sessions(self)

    @base.resource(Tokens)
    def tokens(self):
        """
        Returns all tokens
        """
        return Tokens(self)
