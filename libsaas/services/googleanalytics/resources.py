from libsaas import http, parsers
from libsaas.services import base


def translate_param(val):
    return val.replace('_', '-')


class QuotaResource(base.RESTResource):

    @base.apimethod
    def get(self, userIp=None, quotaUser=None):
        """
        Get resource

        :var userIp: Specifies IP address of the end user for whom the API call
            is being made. Used to cap usage per IP.
        :vartype userIp: str

        :var quotaUser: Alternative to userIp in cases when the user's IP
            address is unknown.
        :vartype quotaUser: str
        """
        params = base.get_params(None, locals(),
                                 translate_param=translate_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class PaginatedQuotaResource(QuotaResource):

    @base.apimethod
    def get(self, max_results=None, start_index=None, userIp=None,
            quotaUser=None):
        """
        List resource

        :var max-results: The maximum number of rows to include in the response
        :vartype max-results: int

        :var start-index: The first row of data to retrieve, starting at 1.
            Use this parameter as a pagination mechanism along with the
            max-results parameter.
        :vartype start-index: int

        :var userIp: Specifies IP address of the end user for whom the API call
            is being made. Used to cap usage per IP.
        :vartype userIp: str

        :var quotaUser: Alternative to userIp in cases when the user's IP
            address is unknown.
        :vartype quotaUser: str
        """
        params = base.get_params(None, locals(),
                                 translate_param=translate_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class GoalBase(QuotaResource):

    path = 'goals'


class Goal(GoalBase):
    pass


class Goals(GoalBase, PaginatedQuotaResource):
    pass


class ViewBase(QuotaResource):

    path = 'profiles'


class Views(ViewBase, PaginatedQuotaResource):
    pass


class View(ViewBase):

    @base.resource(Goals)
    def goals(self):
        """
        Return the resource corresponding to all goals
        """
        return Goals(self)

    @base.resource(Goal)
    def goal(self, goal_id):
        """
        Return the resource corresponding to a single goal
        """
        return Goal(self, goal_id)


class WebPropertyBase(QuotaResource):

    path = 'webproperties'


class WebProperties(WebPropertyBase, PaginatedQuotaResource):
    pass


class WebProperty(WebPropertyBase):

    @base.resource(Views)
    def views(self):
        """
        Return the resource corresponding to all views
        """
        return Views(self)

    @base.resource(View)
    def view(self, profile_id):
        """
        Return the resource corresponding to a single view
        """
        return View(self, profile_id)


class AccountBase(QuotaResource):

    path = 'accounts'


class Accounts(AccountBase, PaginatedQuotaResource):
    pass


class Account(AccountBase):

    @base.resource(WebProperties)
    def webproperties(self):
        """
        Return the resource corresponding to all web properties
        """
        return WebProperties(self)

    @base.resource(WebProperty)
    def webproperty(self, webproperty_id):
        """
        Return the resource corresponding to a single property
        """
        return WebProperty(self, webproperty_id)


class Segments(PaginatedQuotaResource):

    path = 'segments'
