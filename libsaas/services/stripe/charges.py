from libsaas.services import base
from libsaas import parsers, http

from . import resource


class ChargesBaseResource(resource.StripeResource):

    path = 'charges'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Charge(ChargesBaseResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def dispute(self, obj):
        """
        Update a dispute

        :var obj: a Python object representing the updated dispute.
        """
        self.require_item()
        url = '{0}/{1}'.format(self.get_url(), 'dispute')
        request = http.Request('POST', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def refund(self, amount=None):
        """
        Refunding a charge

        :var amount: A positive integer in cents representing how much
            of this charge to refund. Can only refund up to the unrefunded
            amount remaining of the charge. Default is entire charge.
        :vartype amount: int
        """
        params = {}
        if amount:
            params.update({'amount': amount})
        url = '{0}/{1}'.format(self.get_url(), 'refund')
        request = http.Request('POST', url, params)

        return request, parsers.parse_json


class Charges(ChargesBaseResource):

    @base.apimethod
    def get(self, customer=None, count=None, offset=None):
        """
        Fetch all of the objects.

        :var customer: Only return charges for the customer specified by
            this customer ID.
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

