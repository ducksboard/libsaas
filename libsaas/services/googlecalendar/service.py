import json

from libsaas import http
from libsaas.services import base

from .user import User
from . import calendar as c
from .resource import ColorsResource, FreeBusyResource


class GoogleCalendar(base.Resource):

    APIROOT = 'https://www.googleapis.com/calendar/v3'

    def __init__(self, access_token=None):
        """
        Create a Google Calendar service.

        :var access_token:
        :vartype access_token:
        """
        self.access_token = access_token

        self.add_filter(self.add_auth)
        self.add_filter(self.use_json)

    def add_auth(self, request):
        header = 'Bearer {0}'.format(self.access_token)
        request.headers['Authorization'] = header

    def use_json(self, request):
        if (request.method.upper() not in http.URLENCODE_METHODS
                and request.params):
            request.headers['Content-Type'] = 'application/json'
            request.params = json.dumps(request.params)

    def get_url(self):
        return self.APIROOT

    def set_access_token(self, access_token):
        self.access_token = access_token

    @base.resource(c.Calendars)
    def calendars(self):
        """
        Return the resource corresponding to all the calendars
        """
        return c.Calendars(self)

    @base.resource(c.Calendar)
    def calendar(self, calendar_id):
        """
        Return the resource corresponding to a single calendar
        """
        return c.Calendar(self, calendar_id)

    @base.resource(ColorsResource)
    def colors(self):
        """
        Return the resource corresponding to all the colors
        """
        return ColorsResource(self)

    @base.resource(FreeBusyResource)
    def freebusy(self):
        """
        Return the resource corresponding to all the free/busy info
        """
        return FreeBusyResource(self)

    @base.resource(User)
    def me(self):
        """
        Return the resource corresponding to the current user
        """
        return User(self)
