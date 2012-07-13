from libsaas import http, parsers
from libsaas.services import base


class DucksboardResource(base.RESTResource):

    def get_url(self):
        if self.object_id is None:
            return '{0}/{1}/'.format(self.parent.get_url(), self.path)

        return '{0}/{1}/{2}'.format(self.parent.get_url(), self.path,
                                    self.object_id)


class TokenBase(DucksboardResource):

    path = 'tokens'


class Tokens(TokenBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Token(TokenBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class DashboardBase(DucksboardResource):

    path = 'dashboards'


class Dashboards(DashboardBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Dashboard(DashboardBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def accessed(self):
        """
        Update the access time of a dashboard. The last accessed dashboard
        is the one that gets displayed by default when accessing the
        application.
        """

        url = '{0}/{1}'.format(self.get_url(), 'accessed')

        request = http.Request('POST', url, None)
        return request, parsers.parse_json

    @base.resource(Tokens)
    def tokens(self):
        return Tokens(self)

    @base.resource(Token)
    def token(self, token):
        return Token(self, token)

    @base.apimethod
    def widgets(self):
        """
        Get a collection of widgets from a dashboard.
        """
        url = '{0}/{1}/'.format(self.get_url(), 'widgets')

        return http.Request('GET', url), parsers.parse_json


class WidgetBase(DucksboardResource):

    path = 'widgets'


class Widgets(WidgetBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def positions(self, positions):
        """
        Update the positions of multiple widgets at once.

        :var positions: The object keys are widget IDs. the values should
            include a row and column field. Both of them default to 1 if
            not present.
        :vartype positions: dict
        """

        url = '{0}{1}'.format(self.get_url(), 'positions')

        request = http.Request('POST', url, positions)
        return request, parsers.parse_json


class Widget(WidgetBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def copy(self, dashboard_slug):
        """
        Copy a widget to another dashboard, specified by a slug.
        A new widget is created, with the same parameters as the copied one.
        The position is chosen automatically if not specified.

        :var dashboard_slug: dashboard slug destination
        :vartype dashboard_slug: str
        """

        url = '{0}/{1}'.format(self.get_url(), 'copy')

        request = http.Request('POST', url, {'dashboard': dashboard_slug})
        return request, parsers.parse_json


class AccountBase(DucksboardResource):

    path = 'accounts'


class Accounts(AccountBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Account(AccountBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class User(base.RESTResource):

    path = 'user'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def require_item(self):
        pass

    @base.apimethod
    def get_api_key(self):
        """
        Get your API key. This endpoint uses HTTP Basic authentication with
        your Ducksboard username and password.
        """
        url = '{0}/{1}'.format(self.get_url(), 'api_key')

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def reset_api_key(self):
        """
        Reset your API key. This endpoint uses HTTP Basic authentication with
        your Ducksboard username and password.
        """
        url = '{0}/{1}'.format(self.get_url(), 'api_key')

        return http.Request('POST', url, None), parsers.parse_json
