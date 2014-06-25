from libsaas.services import base
from libsaas import parsers, http

from . import resource


class SubscriptionsResource(resource.StripeResource):

    path = 'subscriptions'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self):
        """
        Fetch the object's data.
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json


class SubscriptionResource(SubscriptionsResource):

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

    @base.resource(SubscriptionsResource)
    def subscriptions(self):
        """
        Return the resource corresponding to the customer's subscriptions.
        """
        return SubscriptionsResource(self)

    @base.resource(SubscriptionResource)
    def subscription(self, subscription_id):
        """
        Return the resource corresponding to a single customer's subscription.

        :var subscription_id: The subscription's id.
        :vartype subscription_id: str
        """
        return SubscriptionResource(self, subscription_id)


    @base.resource(DiscountResource)
    def discount(self):
        """
        Return the resource corresponding to a single discount.
        """
        return DiscountResource(self)


class Customers(CustomersBaseResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, total_count=False, count=None, offset=None):
        """
        Fetch all of the objects.

        :var total_count: Include the total count of all customers.
        :vartype total_count: bool

        :var count: A limit on the number of objects to be returned.
            Count can range between 1 and 100 objects.
        :vartype count: int

        :var offset: An offset into your object array. The API will return
            the requested number of objects starting at that offset.
        :vartype offset: int
        """
        params = {'count': count, 'offset': offset}
        if total_count:
            params.update({'include[]': 'total_count'})
        params = base.get_params(None, params)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
