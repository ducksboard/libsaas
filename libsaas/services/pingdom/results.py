from libsaas import http, parsers, port
from libsaas.services import base
from . import resource


class Results(resource.PingdomGETResource):

    path = 'results'

    @base.apimethod
    def get(self, from_=None, to=None, limit=None, offset=None, probes=None,
            status=None, includeanalysis=None, maxresponse=None,
            minresponse=None):
        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)

        return http.Request('GET', self.get_url(), params), parsers.parse_json

port.method_func(Results, 'get').__doc__ = """
Return a list of raw test results for a specified check

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceResults')
