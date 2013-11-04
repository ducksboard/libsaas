from libsaas import http, parsers
from libsaas.services import base

from . import resource, cases


class CustomersBase(resource.DeskResource):

    path = 'customers'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Customers(CustomersBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, embed=None, fields=None, per_page=None, page=None):
        """
        Retrieve a paginated list of all customers

        Upstream documentation: http://dev.desk.com/API/customers#list
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def search(self, first_name=None, last_name=None, full_name=None,
               email=None, phone=None, twitter=None, external_id=None,
               since_created_at=None, max_created_at=None, since_updated_at=None,
               max_updated_at=None, since_id=None, max_id=None, per_page=None,
               page=None, **custom_fields):
        """
        Search customers based on a combination of parameters with pagination.

        Upstream documentation: http://dev.desk.com/API/customers#search
        """
        store = locals()
        store.update(store.pop('custom_fields'))

        params = base.get_params(None, store)
        url = '{0}/{1}'.format(self.get_url(), 'search')
        return http.Request('GET', url, params), parsers.parse_json


class Customer(CustomersBase):

    @base.resource(cases.Cases)
    def cases(self):
        return cases.Cases(self)
