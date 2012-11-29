from libsaas.services import base
from libsaas import parsers, http

from . import resource


class LineItems(resource.StripeResource):

    path = 'lines'

    @base.apimethod
    def get(self, customer=None, count=None, offset=None):
        """
        Fetch all of the objects.

        :var customer: In the case of upcoming invoices, the customer of the
            upcoming invoice is required. In other cases it is ignored.
        :vartype customer: str
        :var count: A limit on the number of objects to be returned.
            Count can range between 1 and 100 objects.
        :vartype count: int

        :var offset: An offset into your object array. The API will return
            the requested number of objects starting at that offset.
        :vartype offset: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class InvoicesBaseResource(resource.StripeResource):

    path = 'invoices'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Invoice(InvoicesBaseResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(LineItems)
    def lines(self):
        """
        Return the resource corresponding to all invoice's lines.
        """
        return LineItems(self)

    @base.apimethod
    def pay(self):
        """
        Paying an invoice
        """
        self.require_item()
        url = '{0}/{1}'.format(self.get_url(), 'pay')
        request = http.Request('POST', url, {})

        return request, parsers.parse_json


class Invoices(InvoicesBaseResource):

    @base.apimethod
    def get(self, customer=None, count=None, offset=None):
        """
        Fetch all of the objects.

        :var customer: The identifier of the customer whose invoices to return.
            If none is provided, all invoices will be returned.
        :vartype customer: str
        :var count: A limit on the number of objects to be returned.
            Count can range between 1 and 100 objects.
        :vartype count: int

        :var offset: An offset into your object array. The API will return
            the requested number of objects starting at that offset.
        :vartype offset: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def upcoming(self, customer):
        """
        Fetch a customer's upcoming invoice.

        :var customer: The identifier of the customer whose invoices to return.
            If none is provided, all invoices will be returned.
        :vartype customer: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'upcoming')
        request = http.Request('GET', url, params)

        return request, parsers.parse_json


class InvoiceItemBaseResource(resource.StripeResource):

    path = 'invoiceitems'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class InvoiceItem(InvoiceItemBaseResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class InvoiceItems(InvoiceItemBaseResource):

    @base.apimethod
    def get(self, customer=None, count=None, offset=None):
        """
        Fetch all of the objects.

        :var customer: The identifier of the customer whose invoice items to return.
            If none is provided, all invoice items will be returned.
        :vartype customer: str
        :var count: A limit on the number of objects to be returned.
            Count can range between 1 and 100 objects.
        :vartype count: int

        :var offset: An offset into your object array. The API will return
            the requested number of objects starting at that offset.
        :vartype offset: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
