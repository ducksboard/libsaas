from libsaas import http, parsers, port
from libsaas.services import base
from . import resource


class Analysis(resource.PingdomGETResource):

    path = 'analysis'

    @base.apimethod
    def get(self, from_=None, to=None, limit=None, offset=None):
        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def get_raw_analysis(self, analysisid):
        """
        Get Raw Analysis Results

        :var analysisid: The specified error analysis id
        :vartype analysisid: str
        """
        url = '{0}/{1}'.format(self.get_url(), analysisid)

        request = http.Request('GET', url)
        return request, parsers.parse_json


port.method_func(Analysis, 'get').__doc__ = """
Returns a list of the latest root cause analysis results for a specified check.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceAnalysis')
