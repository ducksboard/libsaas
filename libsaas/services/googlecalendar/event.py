from libsaas import http, parsers
from libsaas.services import base

from .resource import GoogleCalendarResource


class EventResource(GoogleCalendarResource):
    path = 'events'


class Events(EventResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def patch(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, alwaysIncludeEmail=None, iCalUID=None,
            maxAttendees=None, maxResults=None, orderBy=None, pageToken=None,
            q=None, showDeleted=None, showHiddenInvitations=None,
            singleEvents=None, timeMax=None, timeMin=None, timeZone=None,
            updateMin=None):
        """
        Fetch all events on the calendar.

        :var alwaysIncludeEmail: Whether to always include a value in the
            "email" field for the organizer, creator and attendees, even
            if no real email is available. The default is False.
        :vartype alwaysIncludeEmail: str
        :var iCalUID: Specifies iCalendar UID of events to be included.
        :vartype iCalUID: str
        :var maxAttendees: The maximum number of attendees to include
            in the response. If none is indicated, only the participant
            is returned.
        :vartype maxAttendees: int
        :var maxResults: Maximum number of events returned.
        :vartype maxResults: int
        :var orderBy: The order of the events returned in the result.
            The default is an unspecified, stable order.
        :vartype orderBy: str
        :var pageToken:	Token specifying which result page to return.
        :vartype pageToken: str
        :var q: Free text search terms to find events that match these terms.
        :vartype q: str
        :var showDeleted: Whether to include deleted events.
            The default is False.
        :vartype showDeleted: str
        :var showHiddenInvitations: Whether to include hidden invitations.
            The default is False.
        :vartype showHiddenInvitations: str
        :var singleEvents: Whether to expand recurring events into instances
            and only return single one-off events and instances of recurring
            events, but not the underlying recurring events themselves.
            The default is False.
        :vartype singleEvents: str
        . :var timeMax:	Upper bound for an event's start time to filter by.
            The default is not to filter by start time.
        :vartype timeMax: str
        :var timeMin: Lower bound for an event's end time to filter by.
            The default is not to filter by end time.
        :vartype timeMin: str
        :var timeZone: Time zone used in the response.
            The default is the time zone of the calendar.
        :vartype timeZone: str
        :var updatedMin: Lower bound for an event's last modification timestamp
            to filter by. Optional. The default is not to filter by last modification time.
        :vartype updateMin: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def create(self, obj, sendNotifications=None):
        """
        Create a new resource.

        :var obj: a Python object representing the resource to be created,
            usually in the same format as returned from `get`. Refer to the
            upstream documentation for details.
        :var sendNotifications: Whether to send notifications.
            The default is False.
        :vartype sendNotifications: str
        """
        self.require_collection()

        params = base.get_params(('sendNotifications', ), locals())
        url = self.get_url()
        if params:
            url += '?' + http.urlencode_any(params)

        request = http.Request('POST', url, self.wrap_object(obj))

        return request, parsers.parse_empty

    @base.apimethod
    def importing(self, obj):
        """
        Import an event.

        :var obj: a Python object representing the imported event.
        """
        self.require_collection()
        url = '{0}/import'.format(self.get_url())
        request = http.Request('POST', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def quick_add(self, text, sendNotifications=None):
        """
        Import an event.

        :var text: The text describing the event to be created.
        :vartype text: str
        :var sendNotifications: Whether to send notifications.
            The default is False.
        :vartype sendNotifications: str
        """
        self.require_collection()
        params = base.get_params(None, locals())
        url = '{0}/quickAdd'.format(self.get_url())
        url += '?' + http.urlencode_any(params)
        request = http.Request('POST', url)

        return request, parsers.parse_json


class Event(EventResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, alwaysIncludeEmail=None, maxAttendees=None, timeZone=None):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.

        :var alwaysIncludeEmail:	Whether to always include a value in the
            "email" field for the organizer, creator and attendees, even
            if no real email is available. The default is False.
        :vartype alwaysIncludeEmail: str
        :var maxAttendees: The maximum number of attendees to include
            in the response. If none is indicated, only the participant
            is returned.
        :vartype maxAttendees: int
        :var timeZone: Time zone used in the response.
            The default is the time zone of the calendar.
        :vartype timeZone: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def update(self, obj, alwaysIncludeEmail=None, sendNotifications=None):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        :var alwaysIncludeEmail: Whether to always include a value in the
            "email" field for the organizer, creator and attendees, even
            if no real email is available. The default is False.
        :vartype alwaysIncludeEmail: str
        :var sendNotifications: Whether to send notifications.
            The default is False.
        :vartype sendNotifications: str
        """
        self.require_item()

        params = base.get_params(
                ('alwaysIncludeEmail', 'sendNotifications'), locals())
        url = self.get_url()
        if params:
            url += '?' + http.urlencode_any(params)

        request = http.Request('PUT', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def patch(self, obj, alwaysIncludeEmail=None, sendNotifications=None):
        """
        Patch this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        :var alwaysIncludeEmail: Whether to always include a value in the
            "email" field for the organizer, creator and attendees, even
            if no real email is available. The default is False.
        :vartype alwaysIncludeEmail: str
        :var sendNotifications: Whether to send notifications.
            The default is False.
        :vartype sendNotifications: str
        """
        self.require_item()

        params = base.get_params(
                ('alwaysIncludeEmail', 'sendNotifications'), locals())
        url = self.get_url()
        if params:
            url += '?' + http.urlencode_any(params)

        request = http.Request('PATCH', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete(self, sendNotifications=None):
        """
        Delete this resource.

        :var sendNotifications: Whether to send notifications.
            The default is False.
        :vartype sendNotifications: str
        """
        self.require_item()

        params = base.get_params(None, locals())
        url = self.get_url()
        if params:
            url += '?' + http.urlencode_any(params)

        request = http.Request('DELETE', url)

        return request, parsers.parse_empty

    @base.apimethod
    def move(self, destination, sendNotifications=None):
        """
        Move an event to another calendar.

        :var destination: Calendar identifier of the target calendar
            where the event is to be moved to.
        :vartype destination: str
        :var sendNotifications: Whether to send notifications.
            The default is False.
        :vartype sendNotifications: str
        """
        self.require_item()
        params = base.get_params(None, locals())
        url = '{0}/move'.format(self.get_url())
        url += '?' + http.urlencode_any(params)
        request = http.Request('POST', url)

        return request, parsers.parse_json

    @base.apimethod
    def instances(self, alwaysIncludeEmail=None, maxAttendees=None,
            maxResults=None, originalStart=None, pageToken=None,
            showDeleted=None, timeZone=None):
        """
        Fetch all instances of the recurring event.

        :var alwaysIncludeEmail: Whether to always include a value in the
            "email" field for the organizer, creator and attendees, even
            if no real email is available. The default is False.
        :vartype alwaysIncludeEmail: str
        :var maxAttendees: The maximum number of attendees to include
            in the response. If none is indicated, only the participant
            is returned.
        :vartype maxAttendees: int
        :var maxResults: Maximum number of instances returned.
        :vartype maxResults: int
        :var originalStart: The original start time of the instance
            in the result.
        :vartype originalStart: str
        :var pageToken:	Token specifying which result page to return.
        :vartype pageToken: str
        :var showDeleted: Whether to include deleted instances.
            The default is False.
        :vartype showDeleted: str
        :var timeZone: Time zone used in the response.
            The default is the time zone of the calendar.
        :vartype timeZone: str
        """
        params = base.get_params(None, locals())
        url = '{0}/instances'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

