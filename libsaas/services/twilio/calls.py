from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource, notifications, recordings


class CallsBase(resource.TwilioResource):

    path = 'Calls'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Call(CallsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(notifications.Notifications)
    def notifications(self):
        """
        Return a list of notifications generated for this call.
        """
        return notifications.Notifications(self)

    @base.resource(recordings.Recordings)
    def recordings(self):
        """
        Return a list of Recording resource representations,
        each representing a recording generated during the course
        of this phone call.
        """
        return recordings.Recordings(self)


class Calls(CallsBase):

    @base.apimethod
    def get(self, To=None, From=None, Status=None, StartTime=None,
            StartTimeGT=None, StartTimeLT=None, ParentCallSid=None,
            Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the calls made to or from an account.

        :var To: Only show calls to this phone number or Client identifier.
        :vartype To: str

        :var From: Only show calls from this phone number or Client identifier.
        :vartype From: str

        :var Status: Only show calls currently in this status.
            May be `queued`, `ringing`, `in-progress`, `completed`, `failed`,
            `busy` or `no-answer`.
        :vartype Status: str

        :var StartTime: Only show calls that started on this date,
            given as YYYY-MM-DD.
        :vartype StartTime: str

        :var StartTimeGT: Greater than inequality for StartTime,
            use it for calls that started at or after midnight on a date
            (generates StartTime>=YYYY-MM-DD).
        :vartype StartTimeGT: str

        :var StartTimeLT: Lower than inequality for StartTime,
            use it for calls that started at or before midnight on a date
            (generates StartTime<=YYYY-MM-DD).
        :vartype StartTimeGT: str

        :var ParentCallSid: Only show calls spawned by the call with this Sid.
        :vartype ParentCallSid: str

        :var Page: The current page number. Zero-indexed, so the first page
            is 0.
        :vartype Page: int

        :var PageSize: How many resources to return in each list page.
            The default is 50, and the maximum is 1000.
        :vartype PageSize: int

        :var AfterSid: The last Sid returned in the previous page, used to
            avoid listing duplicated resources if new ones are created while
            paging.
        :vartype AfterSid: str
        """
        params = resource.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()
