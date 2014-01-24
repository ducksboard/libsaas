from libsaas import http, parsers, port
from libsaas.services import base


class CartoDB(base.Resource):
    """
    """
    def __init__(self, subdomain, api_key):
        """
        Create a CartoDB service.

        :var subdomain: The account-specific part of the CartoDB domain, for
            instance use `mycompany` if your CartpDB domain is
            `mycompany.cartodb.com`.
        :vartype subdomain: str

        :var api_key: The API key.
        :vartype api_key: str
        """
        tmpl = '{0}.cartodb.com/api'
        self.apiroot = http.quote_any(tmpl.format(port.to_u(subdomain)))
        self.apiroot = 'https://' + self.apiroot

        self.api_key = api_key
        self.add_filter(self.add_api_key)

    def get_url(self, version='v2'):
        return '{0}/{1}'.format(self.apiroot, version)

    def add_api_key(self, request):
        request.params.update({'api_key': self.api_key})

    @base.apimethod
    def sql(self, q):
        """
        SQL request to the CartoDB account

        :var q: The sql query
        :vartype q: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'sql')

        return http.Request('POST', url, params), parsers.parse_json

    @base.apimethod
    def viz(self, type=None):
        """
        Get the list of visualizations (undocumented endpoint)

        :var type: The visualization type
        :vartype q: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url('v1'), 'viz')

        return http.Request('GET', url, params), parsers.parse_json
