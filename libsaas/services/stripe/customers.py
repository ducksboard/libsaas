from libsaas.services import base
from libsaas import parsers, http

from . import resource


class SubscriptionResource(resource.StripeResource):

    path = 'subscription'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self):
        """
        Fetch the object's data.
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json

    @base.apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        """
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Delete this resource.
        """
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_empty


class DiscountResource(resource.StripeResource):

    path = 'discount'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def delete(self):
        """
        Delete this resource.
        """
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_empty


class CustomersBaseResource(resource.StripeResource):

    path = 'customers'


class Customer(CustomersBaseResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(SubscriptionResource)
    def subscription(self):
        """
        Return the resource corresponding to the customer's subscription.
        """
        return SubscriptionResource(self)

    @base.resource(DiscountResource)
    def discount(self):
        """
        Return the resource corresponding to a single discount.
        """
        return DiscountResource(self)


class Customers(resource.ListResourceMixin, CustomersBaseResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
