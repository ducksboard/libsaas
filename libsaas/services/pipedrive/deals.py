from libsaas import http, parsers
from libsaas.services import base


class Products(base.RESTResource):

    path = 'products'

    @base.apimethod
    def get(self, start=None, limit=None):
        """
        Lists products attached to a deal.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def delete(self, product_attachment_id):
        """
        Deletes a product attachment from a deal, using the
        product_attachment_id.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())
        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json


class DealsResource(base.RESTResource):

    path = 'deals'


class Deals(DealsResource):

    @base.apimethod
    def get(self, filter_id=None, start=None, limit=None, sort_by=None,
            sort_mode=None, owned_by_you=None):
        """
        Returns all deals

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple deals as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())

        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json

    @base.apimethod
    def find(self, term):
        """
        Searches all deals by their title.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())
        url = '{0}/find'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def timeline(self, start_date, interval, amount, field_key, user_id=None,
                 pipeline_id=None, filter_id=None):
        """
        Returns open and won deals, grouped by defined interval of time set
        in a date-type dealField (field_key) - e.g. when month is the chosen
        interval, and 3 months are asked starting from  January 1st, 2012,
        deals are returned grouped into 3 groups - January, February and
        March - based on the value of the given field_key.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())
        url = '{0}/timeline'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class Deal(DealsResource):

    @base.apimethod
    def activities(self, start=None, limit=None, done=None, exclude=None):
        """
        Lists activities associated with a deal.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())
        url = '{0}/activities'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def followers(self):
        """
        Lists the followers of a deal.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        url = '{0}/followers'.format(self.get_url())
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def updates(self, start=None, limit=None):
        """
        Lists updates about a deal.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())
        url = '{0}/updates'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def participants(self, start=None, limit=None):
        """
        Lists participants associated with a deal.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())
        url = '{0}/participants'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def files(self, start=None, limit=None):
        """
        Lists files associated with a deal.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Deals
        """
        params = base.get_params(None, locals())
        url = '{0}/files'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.resource(Products)
    def products(self):
        """
        Returns the resource corresponding to the deal products
        """
        return Products(self)


class DealFieldsResource(base.RESTResource):

    path = 'dealFields'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class DealFields(DealFieldsResource):

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple activities as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-DealFields
        """
        params = base.get_params(None, locals())
        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json


class DealField(DealFieldsResource):
    pass
