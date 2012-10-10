from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource


class TranscriptionsBase(resource.TwilioResource):

    path = 'Transcriptions'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Transcription(TranscriptionsBase):

    pass


class Transcriptions(TranscriptionsBase):

    @base.apimethod
    def get(self, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the list of transcriptions for an account or call.

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


class RecordingsBase(resource.TwilioResource):

    path = 'Recordings'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Recording(RecordingsBase):

    @base.resource(Transcriptions)
    def transcriptions(self):
        """
        Return a set of Transcription resource representations
        for this recording.
        """
        return Transcriptions(self)


class Recordings(RecordingsBase):

    @base.apimethod
    def get(self, CallSid=None, DateCreated=None, DateCreatedGT=None,
            DateCreatedLT=None, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the list of transcriptions for an account or call.

        :var CallSid: Show only recordings made during the call given
            by this sid.
        :vartype CallSid: str

        :var DateCreated: Only show recordings created on this date,
            given as YYYY-MM-DD.
        :vartype DateCreated: str

        :var DateCreatedGT: Greater than inequality for DateCreated,
            use it for recordings created at or after midnight on a date
            (generates DateCreated>=YYYY-MM-DD).
        :vartype DateCreatedGT: str

        :var DateCreatedLT: Lower than inequality for DateCreated,
            use it for recordings created at or before midnight on a date
            (generates DateCreated<=YYYY-MM-DD).
        :vartype DateCreatedGT: str

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

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
