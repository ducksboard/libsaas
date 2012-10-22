from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource
from libsaas.services.twilio import (
    applications, calls, conferences, notifications, numbers, queues,
    recordings, sms, usage)


class AccountsBase(resource.TwilioResource):

    path = 'Accounts'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Account(AccountsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(numbers.AvailablePhoneNumbers)
    def available_phone_numbers(self):
        """
        Return an AvailablePhoneNumbers resource that allows querying
        local and toll-free available for this account.
        """
        return numbers.AvailablePhoneNumbers(self)

    @base.resource(numbers.OutgoingCallerId)
    def outgoing_caller_id(self, sid):
        """
        Return an OutgoingCallerId resource representation,
        representing a Caller ID number valid for this account.
        """
        return numbers.OutgoingCallerId(self, sid)

    @base.resource(numbers.OutgoingCallerIds)
    def outgoing_caller_ids(self):
        """
        Return a list of OutgoingCallerId resource representations,
        each representing a Caller ID number valid for this account.
        """
        return numbers.OutgoingCallerIds(self)

    @base.resource(numbers.IncomingPhoneNumber)
    def incoming_phone_number(self, sid):
        """
        Return an IncomingPhoneNumber resource representation,
        representing a phone number given to this account.
        """
        return numbers.IncomingPhoneNumber(self, sid)

    @base.resource(numbers.IncomingPhoneNumbers)
    def incoming_phone_numbers(self):
        """
        Return a list of IncomingPhoneNumber resource representations,
        each representing a phone number given to this account.
        """
        return numbers.IncomingPhoneNumbers(self)

    @base.resource(applications.ConnectApp)
    def connect_app(self, sid):
        """
        Return a Connect App resource representations,
        representing a Connect App in this account.
        """
        return applications.ConnectApp(self, sid)

    @base.resource(applications.ConnectApps)
    def connect_apps(self):
        """
        Return a list of Connect App resource representations,
        each representing a Connect App in this account.
        """
        return applications.ConnectApps(self)

    @base.resource(applications.AuthorizedConnectApp)
    def authorized_connect_app(self, sid):
        """
        Return a Connect App resource representation,
        representing a Connect App you've authorized to access this account.
        """
        return applications.AuthorizedConnectApp(self, sid)

    @base.resource(applications.AuthorizedConnectApps)
    def authorized_connect_apps(self):
        """
        Return a list of Connect App resource representations,
        each representing a Connect App you've authorized to access
        this account.
        """
        return applications.AuthorizedConnectApps(self)

    @base.resource(applications.Application)
    def application(self, sid):
        """
        Return a Application resource representation,
        representing an application within this account.
        """
        return applications.Application(self, sid)

    @base.resource(applications.Applications)
    def applications(self):
        """
        Return a list of Application resource representations,
        each representing an application within this account.
        """
        return applications.Applications(self)

    @base.resource(calls.Call)
    def call(self, sid):
        """
        Return a phone call made to and from this account.
        """
        return calls.Call(self, sid)

    @base.resource(calls.Calls)
    def calls(self):
        """
        Return a list of phone calls made to and from this account.
        """
        return calls.Calls(self)

    @base.resource(conferences.Conference)
    def conference(self, sid):
        """
        Return a conference within this account.
        """
        return conferences.Conference(self, sid)

    @base.resource(conferences.Conferences)
    def conferences(self):
        """
        Return a list of conferences within this account.
        """
        return conferences.Conferences(self)

    @base.resource(queues.Queue)
    def queue(self, sid):
        """
        Return a queue within this account.
        """
        return queues.Queue(self, sid)

    @base.resource(queues.Queues)
    def queues(self):
        """
        Return a list of queues within this account.
        """
        return queues.Queues(self)

    @base.resource(sms.SMS)
    def sms(self):
        """
        Return a SMS resource to query messages and short codes resources.
        """
        return sms.SMS(self)

    @base.resource(recordings.Transcription)
    def transcription(self, sid):
        """
        Return a Transcription resource representation for call
        made to of from this account.
        """
        return recordings.Transcription(self, sid)

    @base.resource(recordings.Transcriptions)
    def transcriptions(self):
        """
        Return a set of Transcription resource representations
        for this account.
        """
        return recordings.Transcriptions(self)

    @base.resource(recordings.Recording)
    def recording(self, sid):
        """
        Return a Recording resource representation,
        representing a recording generated during the course
        of a phone call made to or from this account.
        """
        return recordings.Recording(self, sid)

    @base.resource(recordings.Recordings)
    def recordings(self):
        """
        Return a list of Recording resource representations,
        each representing a recording generated during the course
        of a phone call made to or from this account.
        """
        return recordings.Recordings(self)

    @base.resource(notifications.Notification)
    def notification(self, sid):
        """
        Return a notification generated for this account.
        """
        return notifications.Notification(self, sid)

    @base.resource(notifications.Notifications)
    def notifications(self):
        """
        Return a list of notifications generated for this account.
        """
        return notifications.Notifications(self)

    @base.resource(usage.Usage)
    def usage(self):
        """
        Return a usage resource to query records and triggers resources.
        """
        return usage.Usage(self)


class Accounts(AccountsBase):

    @base.apimethod
    def get(self, FriendlyName=None, Status=None,
            Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the (sub)accounts belonging to this account.

        :var FriendlyName: Only return the Account resources with friendly
            names that exactly match this name.
        :vartype FriendlyName: str

        :var Status: Only return Account resources with the given status.
            Can be `closed`, `suspended` or `active`.
        :vartype Status: str

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
