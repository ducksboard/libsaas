import json

from libsaas import http
from libsaas.filters import auth
from libsaas.services import base

from . import resources, datasource


class Ducksboard(base.Resource):
    """
    """
    def __init__(self, apikey_or_username, password=None):
        """
        Create a Ducksboard service.

        :var apikey_or_username: Your apikey or your username if you
            want to get or reset your API key.
        :vartype apikey_or_username: str

        :var password: Only used with your username to get or reset your
            API key.
        :vartype password: str
        """
        self.apiroot = 'https://app.ducksboard.com/api'
        self.apikey_or_username = apikey_or_username

        self.add_filter(auth.BasicAuth(apikey_or_username, password))
        self.add_filter(self.use_json)

    def use_json(self, request):
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = json.dumps(request.params)

    def get_url(self):
        return self.apiroot

    @base.resource(resources.Dashboards)
    def dashboards(self):
        """
        Return the resource corresponding to all the dashboards.
        """
        return resources.Dashboards(self)

    @base.resource(resources.Dashboard)
    def dashboard(self, slug):
        """
        Return the resource corresponding to a single dashboard.
        """
        return resources.Dashboard(self, slug)

    @base.resource(resources.Widgets)
    def widgets(self):
        """
        Return the resource corresponding to all the widgets.
        """
        return resources.Widgets(self)

    @base.resource(resources.Widget)
    def widget(self, widget_id):
        """
        Return the resource corresponding to a single widget.
        """
        return resources.Widget(self, widget_id)

    @base.resource(resources.Accounts)
    def accounts(self):
        """
        Return the resource corresponding to all the accounts.
        """
        return resources.Accounts(self)

    @base.resource(resources.Account)
    def account(self, account_id):
        """
        Return the resource corresponding to a single account.
        """
        return resources.Account(self, account_id)

    @base.resource(resources.Account)
    def user(self):
        """
        Return the resource corresponding to your user.
        """
        return resources.User(self)

    @base.resource(datasource.Datasource)
    def data_source(self, label):
        """
        Return the resource corresponding to a datasource.
        Datasources can only be accesed using the API key
        """
        return datasource.Datasource(self.apikey_or_username, label)
