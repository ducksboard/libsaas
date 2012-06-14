from libsaas import http, parsers
from libsaas.services import base

from . import resource
from . import invoices as inv
from . import coupons as coup
from . import transactions as tx
from . import adjustments as ads
from . import subscriptions as subs


class BillingInfo(resource.RecurlyResource):

    path = 'billing_info'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        """
        # skip require_item checking because we are using the account's one
        request = http.Request('PUT', self.get_url(), obj)
        return request, parsers.parse_xml

    @base.apimethod
    def delete(self):
        """
        Delete this resource.
        """
        request = http.Request('DELETE', self.get_url())
        return request, parsers.parse_empty


class AccountBase(resource.RecurlyResource):

    path = 'accounts'


class Accounts(AccountBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, state='active', cursor=None, per_page=None):
        """
        Fetch accounts for your site.

        :var state: The state of the accounts to return: 'active', 'closed',
            'past_due'. Defaults to 'active'.
        :vartype state: str
        """
        params = base.get_params(('cursor', 'per_page'), locals())
        params['state'] = state
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_xml


class Account(AccountBase):

    @base.resource(BillingInfo)
    def billing_info(self):
        """
        Return the resource corresponding to the account's
        current billing information.
        """
        return BillingInfo(self)

    @base.resource(coup.CouponRedemption)
    def redemption(self):
        """
        Return the resource corresponding to the
        coupon redeemed by the account.
        """
        return coup.CouponRedemption(self)

    @base.resource(subs.AccountSubscriptions)
    def subscriptions(self):
        """
        Return the resource corresponding to all subscriptions for the account.
        """
        return subs.AccountSubscriptions(self)

    @base.resource(ads.AccountAdjustments)
    def adjustments(self):
        """
        Return the resource corresponding to all charges
        and credits issued for the account.
        """
        return ads.AccountAdjustments(self)

    @base.resource(inv.AccountInvoices)
    def invoices(self):
        """
        Return the resource corresponding to all invoices for the account.
        """
        return inv.AccountInvoices(self)

    @base.resource(tx.AccountTransactions)
    def transactions(self):
        """
        Return the resource corresponding to all transactions for the account.
        """
        return tx.AccountTransactions(self)
