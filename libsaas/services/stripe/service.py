from libsaas.filters import auth
from libsaas.services import base

from .accounts import Account
from .plans import Plans, Plan
from .tokens import Tokens, Token
from .events import Events, Event
from .charges import Charges, Charge
from .coupons import Coupons, Coupon
from .customers import Customers, Customer
from .invoices import Invoices, Invoice, InvoiceItems, InvoiceItem


class Stripe(base.Resource):
    """
    """
    def __init__(self, api_key):
        """
        Create a Stripe service.

        :var api_key: The API key.
        :vartype api_key: str
        """
        self.apiroot = 'https://api.stripe.com/v1'

        self.add_filter(auth.BasicAuth(api_key, ''))

    def get_url(self):
        return self.apiroot

    @base.resource(Account)
    def account(self):
        """
        Return the resource corresponding to the logged account.
        """
        return Account(self)

    @base.resource(Plans)
    def plans(self):
        """
        Return the resource corresponding to all plans.
        """
        return Plans(self)

    @base.resource(Plan)
    def plan(self, id):
        """
        Return the resource corresponding to a single plan.
        """
        return Plan(self, id)

    @base.resource(Charges)
    def charges(self):
        """
        Return the resource corresponding to all charges.
        """
        return Charges(self)

    @base.resource(Charge)
    def charge(self, id):
        """
        Return the resource corresponding to a single charge.
        """
        return Charge(self, id)

    @base.resource(Customers)
    def customers(self):
        """
        Return the resource corresponding to all customers.
        """
        return Customers(self)

    @base.resource(Customer)
    def customer(self, id):
        """
        Return the resource corresponding to a single customer.
        """
        return Customer(self, id)

    @base.resource(Tokens)
    def tokens(self):
        """
        Return the resource corresponding to all tokens.
        """
        return Tokens(self)

    @base.resource(Token)
    def token(self, id):
        """
        Return the resource corresponding to a single token.
        """
        return Token(self, id)

    @base.resource(Invoices)
    def invoices(self):
        """
        Return the resource corresponding to all invoices.
        """
        return Invoices(self)

    @base.resource(Invoice)
    def invoice(self, id):
        """
        Return the resource corresponding to a single invoice.
        """
        return Invoice(self, id)

    @base.resource(Events)
    def events(self):
        """
        Return the resource corresponding to all events.
        """
        return Events(self)

    @base.resource(Event)
    def event(self, id):
        """
        Return the resource corresponding to a single event.
        """
        return Event(self, id)

    @base.resource(Coupons)
    def coupons(self):
        """
        Return the resource corresponding to all coupons.
        """
        return Coupons(self)

    @base.resource(Coupon)
    def coupon(self, id):
        """
        Return the resource corresponding to a single coupon.
        """
        return Coupon(self, id)

    @base.resource(InvoiceItems)
    def invoiceitems(self):
        """
        Return the resource corresponding to all invoiceitems.
        """
        return InvoiceItems(self)

    @base.resource(InvoiceItem)
    def invoiceitem(self, id):
        """
        Return the resource corresponding to a single invoiceitem.
        """
        return InvoiceItem(self, id)
