from libsaas import http, parsers, port
from libsaas.services import base
from . import resource


class Single(resource.PingdomGETResource):

    path = 'single'

    @base.apimethod
    def get(self, **params):
        params = base.get_params(None, params,
                                 translate_param=resource.translate_param)

        return http.Request('GET', self.get_url(), params), parsers.parse_json


port.method_func(Single, 'get').__doc__ = """
Performs a single test using a specified Pingdom probe against a specified
target. Please note that this method is meant to be used sparingly, not to
set up your own monitoring solution.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceSingle')
