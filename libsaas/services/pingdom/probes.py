from libsaas import http, parsers, port
from libsaas.services import base
from . import resource


class Probes(resource.PingdomGETResource):

    path = 'probes'

    @base.apimethod
    def get(self, limit=None, offset=None, onlyactive=None,
            includedeleted=None):
        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)

        return http.Request('GET', self.get_url(), params), parsers.parse_json


port.method_func(Probes, 'get').__doc__ = """
Returns a list of all Pingdom probe servers.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceProbes')
