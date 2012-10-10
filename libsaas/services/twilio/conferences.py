from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource


class ParticipantsBase(resource.TwilioResource):

    path = 'Participants'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Participant(ParticipantsBase):

    pass


class Participants(ParticipantsBase):

    @base.apimethod
    def get(self, Muted=None, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the participants of a conference.

        :var Muted: Only show participants that are muted or unmuted.
            Either `True` or `False`.
        :vartype Muted: bool

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

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ConferencesBase(resource.TwilioResource):

    path = 'Conferences'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Conference(ConferencesBase):

    @base.resource(Participants)
    def participants(self):
        """
        Return the list of participants in this conference.
        """
        return Participants(self)

    @base.resource(Participant)
    def participant(self, sid):
        """
        Return a participant in this conference.
        """
        return Participant(self, sid)


class Conferences(ConferencesBase):

    @base.apimethod
    def get(self, Status=None, FriendlyName=None,
            DateCreated=None, DateCreatedGT=None, DateCreatedLT=None,
            DateUpdated=None, DateUpdatedGT=None, DateUpdatedLT=None,
            Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the calls made to or from an account.

        :var Status: Only show conferences currently in with this status.
            May be `init`, `in-progress`, or `completed`.
        :vartype Status: str

        :var FriendlyName: List conferences who's FriendlyName is the exact
            match of this string.
        :vartype FriendlyName: str

        :var DateCreated: Only show conferences that started on this date,
            given as YYYY-MM-DD.
        :vartype DateCreated: str

        :var DateCreatedGT: Greater than inequality for DateCreated,
            use it for conferences that started at or after midnight on a date
            (generates DateCreated>=YYYY-MM-DD).
        :vartype DateCreatedGT: str

        :var DateCreatedLT: Lower than inequality for DateCreated,
            use it for conferences that started at or before midnight on a date
            (generates DateCreated<=YYYY-MM-DD).
        :vartype DateCreatedGT: str

        :var DateUpdated: Only show conferences that were last updated on
            this date, given as YYYY-MM-DD.
        :vartype DateUpdated: str

        :var DateUpdatedGT: Greater than inequality for DateUpdated,
            use it for conferences that were last updated at or after midnight
            on a date (generates DateUpdated>=YYYY-MM-DD).
        :vartype DateUpdatedGT: str

        :var DateUpdatedLT: Lower than inequality for DateUpdated,
            use it for conferences that were last updated at or before midnight
            on a date (generates DateUpdated<=YYYY-MM-DD).
        :vartype DateUpdatedGT: str

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
