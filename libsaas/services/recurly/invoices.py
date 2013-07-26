from libsaas import http, parsers
from libsaas.services import base

from . import resource


def parse_passthrough(body, code, headers):
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)

    return body


class InvoicesBase(resource.RecurlyResource):

    path = 'invoices'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Invoices(InvoicesBase):

    @base.apimethod
    def get(self, state=None, cursor=None, per_page=None):
        """
        Fetch all your invoices.

        :var state: The state of invoices to return: "open", "collected",
            "failed", or "past_due".
        :vartype state: str
        """
        params = base.get_params(('state', 'cursor', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_xml

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Invoice(InvoicesBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get_pdf(self, language='en-US'):
        """
        Fetch a PDF blob for the invoice.

        :var language: The language for the invoice, defaults to "en-US'.
        :vartype language: str
        """
        self.require_item()

        headers = {'Accept': 'application/pdf', 'Accept-Language': language}
        request = http.Request('GET', self.get_url(), {}, headers)

        return request, parse_passthrough

    @base.apimethod
    def mark_successful(self):
        """
        Mark an invoice as paid successfully
        """
        self.require_item()

        url = '{0}/mark_successful'.format(self.get_url())
        request = http.Request('PUT', url)

        return request, parsers.parse_empty

    @base.apimethod
    def mark_failed(self):
        """
        Mark an invoice as failed collection
        """
        self.require_item()

        url = '{0}/mark_failed'.format(self.get_url())
        request = http.Request('PUT', url)

        return request, parsers.parse_empty


class AccountInvoices(InvoicesBase):

    pass
