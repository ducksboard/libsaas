import json

from libsaas import http
from libsaas.services import base

from .members import Member
from .actions import Action
from .cards import Card, Cards
from .lists import List, Lists
from .boards import Board, Boards
from .notifications import Notification
from .checklists import Checklist, Checklists
from .organizations import Organization, Organizations


class Trello(base.Resource):
    """
    """
    def __init__(self, key, token=None):
        """
        Create a Trello service.

        :var key: Your application key
        :vartype key: str
        :var token: The authorization token from the user (optional).
        :vartype token: str
        """
        self.apiroot = 'https://api.trello.com/1'
        self.key = key
        self.token = token
        self.add_filter(self.add_auth)
        self.add_filter(self.use_json)

    def get_url(self):
        return self.apiroot

    def add_auth(self, request):
        params = {'key': self.key}

        if self.token:
            params.update({'token': self.token})

        if request.method.upper() in http.URLENCODE_METHODS:
            request.params.update(params)
        else:
            request.params = json.dumps(request.params)
            request.uri += '?' + http.urlencode_any(params)

    def use_json(self, request):
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.headers['Content-Type'] = 'application/json'

    @base.resource(Action)
    def action(self, action_id):
        """
        Return the resource corresponding to a single action.
        """
        return Action(self, action_id)

    @base.resource(Boards)
    def boards(self):
        """
        Return the resource corresponding to all boards
        """
        return Boards(self)

    @base.resource(Board)
    def board(self, board_id):
        """
        Return the resource corresponding to a single board
        """
        return Board(self, board_id)

    @base.resource(Cards)
    def cards(self):
        """
        Return the resource corresponding to all cards
        """
        return Cards(self)

    @base.resource(Card)
    def card(self, card_id_or_shortlink):
        """
        Return the resource corresponding to a single card
        """
        return Card(self, card_id_or_shortlink)

    @base.resource(Checklists)
    def checklists(self):
        """
        Return the resource corresponding to all checklists
        """
        return Checklists(self)

    @base.resource(Checklist)
    def checklist(self, checklist_id):
        """
        Return the resource corresponding to a single checklist
        """
        return Checklist(self, checklist_id)

    @base.resource(Lists)
    def lists(self):
        """
        Return the resource corresponding to all lists
        """
        return Lists(self)

    @base.resource(List)
    def list(self, list_id):
        """
        Return the resource corresponding to a single list
        """
        return List(self, list_id)

    @base.resource(Member)
    def me(self):
        """
        Return the resource corresponding to the current member
        """
        return Member(self, 'me')

    @base.resource(Member)
    def member(self, member_id_or_username):
        """
        Return the resource corresponding to a single member
        """
        return Member(self, member_id_or_username)

    @base.resource(Notification)
    def notification(self, notification_id):
        """
        Return the resource corresponding to a single notification
        """
        return Notification(self, notification_id)

    @base.resource(Organizations)
    def organizations(self):
        """
        Return the resource corresponding to all organizations
        """
        return Organizations(self)

    @base.resource(Organization)
    def organization(self, organization_id_or_name):
        """
        Return the resource corresponding to a single organization
        """
        return Organization(self, organization_id_or_name)
