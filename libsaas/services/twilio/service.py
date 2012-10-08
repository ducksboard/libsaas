from libsaas.filters import auth
from libsaas.services import base

from . import accounts


def use_json(request):
    """
    Add a .json extension to the request URI to get a JSON response.
    """
    request.uri = '{0}.json'.format(request.uri)


class Twilio(base.Resource):

    def __init__(self, account_sid, auth_token):
        """
        Create a Twilio service.

        :var account_sid: The users's account SID
        :vartype account_sid: str

        :var auth_token: THe account's API token
        :vartype auth_token: str
        """
        self.apiroot = 'https://api.twilio.com/2010-04-01'
        self.add_filter(auth.BasicAuth(account_sid, auth_token))
        self.add_filter(use_json)

    def get_url(self):
        return self.apiroot

    @base.resource(accounts.Account)
    def account(self, sid):
        """
        Return the representation of an Account or SubAccount.
        """
        return accounts.Account(self, sid)

    @base.resource(accounts.Accounts)
    def accounts(self):
        """
        Return the set of Accounts resources belonging to the Account
        used to make the API request.
        This list includes that account, along with any subaccounts belonging to it.

        You can use the Accounts list resource to create subaccounts and
        retrieve the subaccounts that exist under your main account.
        """
        return accounts.Accounts(self)
