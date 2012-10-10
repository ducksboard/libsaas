from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource


class ApplicationsBase(resource.TwilioResource):

    path = 'Applications'


class Application(ApplicationsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Applications(ApplicationsBase):

    @base.apimethod
    def get(self, FriendlyName=None, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the Applications belonging to an account.

        :var FriendlyName: Only return the Account resources with friendly
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

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ConnectAppsBase(resource.TwilioResource):

    path = 'ConnectApps'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ConnectApp(ConnectAppsBase):

    pass


class ConnectApps(ConnectAppsBase):

    @base.apimethod
    def get(self, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the Connect Apps belonging to an account.

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


class AuthorizedConnectAppsBase(resource.TwilioResource):

    path = 'AuthorizedConnectApps'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class AuthorizedConnectApp(AuthorizedConnectAppsBase):

    pass


class AuthorizedConnectApps(AuthorizedConnectAppsBase):

    @base.apimethod
    def get(self, Page=None, PageSize=None, AfterSid=None):
        """
        Fetch the Authorized Connect Apps belonging to an account.

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
