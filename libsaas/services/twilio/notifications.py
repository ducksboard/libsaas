from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource


class NotificationsBase(resource.TwilioResource):

    path = 'Notifications'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Notification(NotificationsBase):

    pass


class Notifications(NotificationsBase):

    @base.apimethod
    def get(self, Log=None, MessageDate=None, MessageDateGT=None,
            MessageDateLT=None, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch notifications for an account or call.

        :var Log: Only show notifications for this log, using the integer
            log values.
        :vartype Log: int

        :var MessageDate: Only show notifications for this date, given
            as YYYY-MM-DD.
        :vartype MessageDate: str

        :var MessageDateGT: Greater than inequality for MessageDate,
            use it for messages logged at or after midnight on a date
            (generates MessageDate>=YYYY-MM-DD).
        :vartype MessageDateGT: str

        :var MessageDateLT: Lower than inequality for MessageDate,
            use it for messages logged at or before midnight on a date
            (generates MessageDate<=YYYY-MM-DD).
        :vartype MessageDateGT: str

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
