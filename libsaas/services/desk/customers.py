from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Emails(resource.DeskResource):

    path = 'emails'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Phones(resource.DeskResource):

    path = 'phones'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class CustomersBase(resource.DeskResource):

    path = 'customers'


class Customers(CustomersBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, email=None, phone=None, twitter=None, external_id=None,
            since_created_at=None, max_created_at=None, since_updated_at=None,
            max_updated_at=None, since_id=None, max_id=None, count=None,
            page=None, **custom_fields):
        """
        Search customers based on a combination of parameters with pagination.

        Upstream documentation: http://dev.desk.com/docs/api/customers
        """
        store = locals()
        store.update(store.pop('custom_fields'))

        params = base.get_params(None, store)

        return http.Request('GET', self.get_url(), params), parsers.parse_json


class Customer(CustomersBase):

    @base.resource(Emails)
    def emails(self):
        """
        Return the resource corresponding to customer emails
        """
        return Emails(self)

    @base.resource(Emails)
    def email(self, email_id):
        """
        Return the resource corresponding to a customer email
        """
        return Emails(self, email_id)

    @base.resource(Phones)
    def phones(self):
        """
        Return the resource corresponding to customer phones
        """
        return Phones(self)

    @base.resource(Phones)
    def phone(self, phone_id):
        """
        Return the resource corresponding to a customer phone
        """
        return Phones(self, phone_id)
