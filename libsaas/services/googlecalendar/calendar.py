from libsaas import http, parsers
from libsaas.services import base

from .resource import GoogleCalendarResource
from .acl import Acls, Acl
from . import event as e


class CalendarResource(GoogleCalendarResource):
    path = 'calendars'


class Calendars(CalendarResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def patch(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Calendar(CalendarResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def clear(self):
        """
        Clear this calendar.
        """
        self.require_item()
        url = '{0}/clear'.format(self.get_url())
        request = http.Request('POST', url)

        return request, parsers.parse_empty

    @base.resource(Acls)
    def rules(self):
        """
        Return the resource corresponding to all the rules
        """
        return Acls(self)

    @base.resource(Acl)
    def rule(self, rule_id):
        """
        Return the resource corresponding to a single rule
        """
        return Acl(self, rule_id)

    @base.resource(e.Events)
    def events(self):
        """
        Return the resource corresponding to all the events
        """
        return e.Events(self)

    @base.resource(e.Event)
    def event(self, event_id):
        """
        Return the resource corresponding to a single event
        """
        return e.Event(self, event_id)


class CalendarListResource(GoogleCalendarResource):
    path = 'calendarList'


class CalendarLists(CalendarListResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def patch(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class CalendarList(CalendarListResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()
