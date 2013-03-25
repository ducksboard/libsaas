from libsaas import http, parsers
from libsaas.services import base


class ProductsResource(base.RESTResource):

    path = 'products'


class Products(ProductsResource):

    @base.apimethod
    def get(self, start=None, limit=None):
        """
        Returns all products

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Products
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def find(self, term, currency=None, start=None, limit=None):
        """
        Returns data about the products that were found.
        If currency was set in request, prices in that currency are
        served back.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Products
        """
        params = base.get_params(None, locals())
        url = '{0}/find'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class Product(ProductsResource):

    @base.apimethod
    def deals(self, start=None, limit=None):
        """
        Returns data about a deals that have a product attached to.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Products
        """
        params = base.get_params(None, locals())
        url = '{0}/deals'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class ProductFieldsResource(base.RESTResource):

    path = 'productFields'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ProductFields(ProductFieldsResource):

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple activities as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-ProductFields
        """
        params = base.get_params(None, locals())

        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json


class ProductField(ProductFieldsResource):
    pass
