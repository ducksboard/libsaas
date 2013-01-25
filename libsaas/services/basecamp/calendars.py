from libsaas import http, parsers
from libsaas.services import base

from .resource import BasecampResource
from .comments import Comments
from . import accesses as acc


class CalendarEventResource(BasecampResource):
    path = 'calendar_events'


class CalendarEvents(CalendarEventResource):

    @base.apimethod
    def past(self):
        url = '{0}/past'.format(self.get_url())
        request = http.Request('GET', url, {})

        return request, parsers.parse_json


class CalendarEvent(CalendarEventResource):

    @base.resource(Comments)
    def comments(self):
        """
        Return the resource corresponding to all comments.
        """
        return Comments(self)


class CalendarResource(BasecampResource):
    path = 'calendars'


class Calendars(CalendarResource):
    pass


class Calendar(CalendarResource):

    @base.resource(acc.Accesses)
    def accesses(self):
        """
        Return the resource corresponding to all calendar accesses.
        """
        return acc.Accesses(self)

    @base.resource(acc.Access)
    def access(self, access_id):
        """
        Return the resource corresponding to a single access.
        """
        return acc.Access(self, access_id)

    @base.resource(CalendarEvents)
    def calendar_events(self):
        """
        Return the resource corresponding to all calendar events.
        """
        return CalendarEvents(self)

    @base.resource(CalendarEvent)
    def calendar_event(self, calendar_event_id):
        """
        Return the resource corresponding to a single calendar event.
        """
        return CalendarEvent(self, calendar_event_id)
