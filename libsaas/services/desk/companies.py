from libsaas import http, parsers
from libsaas.services import base

from . import resource, cases, customers


class CompaniesBase(resource.DeskResource):

    path = 'companies'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Companies(CompaniesBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, embed=None, fields=None, per_page=None, page=None):
        """
        Retrieve a paginated list of all companies

        Upstream documentation: http://dev.desk.com/API/companies/#list
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def search(self, q, per_page=None, page=None,
               sort_field=None, sort_direction=None):
        """
        Search companies based on a search parameter with pagination.

        Upstream documentation: http://dev.desk.com/API/companies/#search
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'search')
        return http.Request('GET', url, params), parsers.parse_json


class Company(CompaniesBase):

    @base.resource(cases.Cases)
    def cases(self):
        return cases.Cases(self)

    @base.resource(customers.Customers)
    def customers(self):
        return customers.Customers(self)
