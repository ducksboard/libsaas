from libsaas.services import base

from .resources import Accounts, Account, Segments


class Management(base.HierarchicalResource):

    path = 'management'

    @base.resource(Accounts)
    def accounts(self):
        """
        Return the resource corresponding to all accounts
        """
        return Accounts(self)

    @base.resource(Account)
    def account(self, account_id):
        """
        Return the resource corresponding to a single account
        """
        return Account(self, account_id)

    @base.resource(Segments)
    def segments(self):
        """
        Return the resource corresponding to all segments
        """
        return Segments(self)
