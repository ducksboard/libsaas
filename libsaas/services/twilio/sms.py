from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource


class MessagesBase(resource.TwilioResource):

    path = 'Messages'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Message(MessagesBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Messages(MessagesBase):

    @base.apimethod
    def get(self, To=None, From=None, DateSent=None, DateSentGT=None,
            DateSentLT=None, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the list of SMS messages associated with an account.

        :var To: Only show SMS messages to this phone number.
        :vartype To: str

        :var From: Only show SMS messages from this phone number.
        :vartype From: str

        :var DateSent: Only show SMS messages on this date,
            given as YYYY-MM-DD.
        :vartype DateSent: str

        :var DateSentGT: Greater than inequality for DateSent,
            use it for message sent at or after midnight on a date
            (generates DateSent>=YYYY-MM-DD).
        :vartype DateSentGT: str

        :var DateSentLT: Lower than inequality for DateSent,
            use it for messages sent at or before midnight on a date
            (generates DateSent<=YYYY-MM-DD).
        :vartype DateSentGT: str

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


class ShortCodesBase(resource.TwilioResource):

    path = 'ShortCodes'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ShortCode(ShortCodesBase):

    pass


class ShortCodes(ShortCodesBase):

    @base.apimethod
    def get(self, ShortCode=None, FriendlyName=None,
            Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the list of short codes for an account.

        :var ShortCode: Only show the ShortCode resources that match
            this pattern. You can specify partial numbers and use `*`
            as a wildcard for any digit.
        :vartype ShortCode: str

        :var FriendlyName: Only show the ShortCode resources with friendly
            names that exactly match this name.
        :vartype FriendlyName: str

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


class SMS(resource.TwilioResource):

    path = 'SMS'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(Message)
    def message(self, sid):
        """
        Return a SMS message associated with this account.
        """
        return Message(self, sid)

    @base.resource(Messages)
    def messages(self):
        """
        Return a list of SMS messages associated with this account.
        """
        return Messages(self)

    @base.resource(ShortCode)
    def short_code(self, sid):
        """
        Return a ShortCode resource representation,
        representing a short code within this account.
        """
        return ShortCode(self, sid)

    @base.resource(ShortCodes)
    def short_codes(self):
        """
        Return a list of ShortCode resource representations,
        each representing a short code within this account.
        """
        return ShortCodes(self)
