from libsaas import http, xml

from libsaas.filters import auth
from libsaas.services import base

from . import plans as pl
from . import accounts as acc
from . import invoices as inv
from . import coupons as coup
from . import transactions as tx
from . import adjustments as ads
from . import subscriptions as subs


class Recurly(base.Resource):
    """
    """
    def __init__(self, api_key):
        """
        Create a Recurly service.

        :var api_key: The API key including.
        :vartype api_key: str
        """
        self.apiroot = 'https://api.recurly.com/v2'

        self.add_filter(auth.BasicAuth(api_key, ''))
        self.add_filter(self.use_xml)

    def get_url(self):
        return self.apiroot

    def use_xml(self, request):
        request.headers['Content-Type'] = 'application/xml'
        request.headers['Accept'] = 'application/xml'

        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = xml.dict_to_xml(request.params)

    @base.resource(pl.Plans)
    def plans(self):
        """
        Return the resource corresponding to all plans.
        """
        return pl.Plans(self)

    @base.resource(pl.Plan)
    def plan(self, plan_code):
        """
        Return the resource corresponding to a single plan.
        """
        return pl.Plan(self, plan_code)

    @base.resource(acc.Accounts)
    def accounts(self):
        """
        Return the resource corresponding to all accounts.
        """
        return acc.Accounts(self)

    @base.resource(acc.Account)
    def account(self, account_code):
        """
        Return the resource corresponding to a single account.
        """
        return acc.Account(self, account_code)

    @base.resource(ads.Adjustment)
    def adjustment(self, uuid):
        """
        Return the resource corresponding to a single adjustment.
        """
        return ads.Adjustment(self, uuid)

    @base.resource(coup.Coupons)
    def coupons(self):
        """
        Return the resource corresponding to all coupons.
        """
        return coup.Coupons(self)

    @base.resource(coup.Coupon)
    def coupon(self, coupon_code):
        """
        Return the resource corresponding to a single coupon.
        """
        return coup.Coupon(self, coupon_code)

    @base.resource(inv.Invoices)
    def invoices(self):
        """
        Return the resource corresponding to all invoices.
        """
        return inv.Invoices(self)

    @base.resource(inv.Invoice)
    def invoice(self, invoice_number):
        """
        Return the resource corresponding to a single invoice.
        """
        return inv.Invoice(self, invoice_number)

    @base.resource(subs.Subscriptions)
    def subscriptions(self):
        """
        Return the resource corresponding to all subscriptions.
        """
        return subs.Subscriptions(self)

    @base.resource(subs.Subscription)
    def subscription(self, uuid):
        """
        Return the resource corresponding to a single subscription.
        """
        return subs.Subscription(self, uuid)

    @base.resource(tx.Transactions)
    def transactions(self):
        """
        Return the resource corresponding to all transactions.
        """
        return tx.Transactions(self)

    @base.resource(tx.Transaction)
    def transaction(self, uuid):
        """
        Return the resource corresponding to a single transaction.
        """
        return tx.Transaction(self, uuid)
