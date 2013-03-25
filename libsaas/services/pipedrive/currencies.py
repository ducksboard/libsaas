from libsaas import http, parsers
from libsaas.services import base


class Currencies(base.HierarchicalResource):

    path = 'currencies'

    @base.apimethod
    def get(self, term=None):
        """
        Returns all supported currencies which should be used when saving
        monetary values with other objects. The 'code' parameter of the
        returning objects is the currency code according to ISO 4217.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Currencies
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json
