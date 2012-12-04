from libsaas import http, parsers, port
from libsaas.services import base
from . import resource


class Summary(base.HierarchicalResource):

    path = 'summary'

    def require_item(self):
        if self.object_id is None:
            raise base.MethodNotSupported()

    def get_url(self, summary):
        self.require_item()
        return '{0}/{1}.{2}/{3}'.format(self.parent.get_url(), self.path,
                                        summary, self.object_id)

    @base.apimethod
    def average(self, from_=None, to=None, probes=None, includeuptime=None,
                bycountry=None, byprobe=None):
        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)
        url = self.get_url('average')
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def hoursofday(self, from_=None, to=None, probes=None, uselocaltime=None):
        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)
        url = self.get_url('hoursofday')
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def outage(self, from_=None, to=None, order=None):
        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)
        url = self.get_url('outage')
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def performance(self, from_=None, to=None, resolution=None,
                    includeuptime=None, probes=None, order=None):
        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)
        url = self.get_url('performance')
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def probes(self, from_=None, to=None):
        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)
        url = self.get_url('probes')
        return http.Request('GET', url, params), parsers.parse_json


port.method_func(Summary, 'average').__doc__ = """
Get the average time / uptime value for a specified check and time period.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceSummary.average')

port.method_func(Summary, 'hoursofday').__doc__ = """
Returns the average response time for each hour of the day (0-23) for a
specific check over a selected time period.
I.e. it shows you what an average day looks like during that time period.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceSummary.hoursofday')

port.method_func(Summary, 'outage').__doc__ = """
Get a list of status changes for a specified check and time period.
If order is speficied to descending, the list is ordered by newest
first. (Default is ordered by oldest first.)

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceSummary.outage')

port.method_func(Summary, 'performance').__doc__ = """
For a given interval in time, return a list of sub intervals with the
given resolution. Useful for generating graphs. A sub interval may be a
week, a day or an hour depending on the choosen resolution.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceSummary.performance')

port.method_func(Summary, 'probes').__doc__ = """
Get a list of probes that performed tests for a specified check during a
specified period.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceSummary.probes')
