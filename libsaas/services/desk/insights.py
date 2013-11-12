from libsaas import http, parsers
from libsaas.services import base


class Insights(base.HierarchicalResource):

    path = 'insights'

    @base.apimethod
    def meta(self):
        """
        Retrieve Insights meta data for the authenticated site.

        Upstream documentation: http://dev.desk.com/API/insights/#meta-show
        """
        url = '{0}/{1}'.format(self.get_url(), 'meta')

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def report(self, resolution=None, min_date=None, max_date=None,
               dimension1_name=None, dimension1_values=None,
               dimension2_name=None, dimension2_values=None, metrics=None,
               sort_by=None, sort_order=None, dimension1_per_page=None,
               dimension1_page=None):
        """
        Create a report.

        Upstream documentation: http://dev.desk.com/API/insights/#report-create
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'reports')

        return http.Request('POST', url, params), parsers.parse_json
