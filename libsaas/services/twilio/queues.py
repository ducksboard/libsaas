from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource


class MembersBase(resource.TwilioResource):

    path = 'Members'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Member(MembersBase):

    pass


class Members(MembersBase):

    @base.apimethod
    def get(self, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the list of members for a conference.

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


class QueuesBase(resource.TwilioResource):

    path = 'Queues'


class Queue(QueuesBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(Members)
    def members(self):
        """
        Return the list of members in this queue.
        """
        return Members(self)

    @base.resource(Member)
    def member(self, sid):
        """
        Return a member in this queue.
        """
        return Member(self, sid)


class Queues(QueuesBase):

    @base.apimethod
    def get(self, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the list of conferences of an account.

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
