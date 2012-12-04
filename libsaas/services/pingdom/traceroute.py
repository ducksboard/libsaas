from libsaas import http, parsers, port
from libsaas.services import base
from . import resource


class Traceroute(resource.PingdomGETResource):

    path = 'traceroute'

    @base.apimethod
    def get(self, host=None, probeid=None):
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json


port.method_func(Traceroute, 'get').__doc__ = """
Perform a traceroute to a specified target from a specified Pingdom probe.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceTraceroute')
