from libsaas import http, parsers
from libsaas.services import base


def translate_param(val):
    return val.replace('_', '-')


class Reporting(base.HierarchicalResource):

    path = 'data'

    def get_url(self, api_endpoint):
        return '{0}/{1}/{2}'.format(self.parent.get_url(), self.path,
                                    api_endpoint)

    @base.apimethod
    def core(self, ids, start_date, end_date, metrics, dimensions=None,
            sort=None, filters=None, segment=None, start_index=None,
            max_results=None, fields=None, prettyPrint=None, userIp=None,
            quotaUser=None, access_token=None, key=None):
        """
        Query the Core Reporting API for Google Analytics report data.

        :var ids: The unique table ID of the form ga:XXXX, where XXXX is the
            Analytics view (profile) ID for which the query will retrieve the
            data.
        :vartype ids: str

        :var start-date: The first date of the date range for which you are
            requesting the data.
        :vartype start-date: str

        :var end-date: The first last of the date range for which you are
            requesting the data.
        :vartype end-date: str

        :var metrics: A list of comma-separated metrics, such as
            ga:visits,ga:bounces.
        :vartype metrics: str

        :var dimensions: A list of comma-separated dimensions for your
            Analytics data, such as ga:browser,ga:city.
        :vartype dimensions: str

        :var sort A list of comma-separated dimensions and metrics indicating
            the sorting order and sorting direction for the returned data.
        :vartype sort: str

        :var filters: Dimension or metric filters that restrict the data
            returned for your request.
        :vartype filters: str

        :var segment: Segments the data returned for your request.
        :vartype segment: str

        :var start-index: The first row of data to retrieve, starting at 1.
            Use this parameter as a pagination mechanism along with the
            max-results parameter.
        :vartype start-index: int

        :var max-results: The maximum number of rows to include in the response
        :vartype max-results: int

        :var fields: Selector specifying a subset of fields to include in the
            response.

        :var prettyPrint: Returns response with indentations and line breaks.
            Default false.
        :vartype prettyPrint: bool

        :var userIp: Specifies IP address of the end user for whom the API call
            is being made. Used to cap usage per IP.
        :vartype userIp: str

        :var quotaUser: Alternative to userIp in cases when the user's IP
            address is unknown.
        :vartype quotaUser: str

        :var access_token: One possible way to provide an OAuth 2.0 token.
        :vartype access_token: str

        :var key: Used for OAuth 1.0a authorization to specify your application
            to get quota. For example: key=AldefliuhSFADSfasdfasdfASdf.
        :vartype key: str
        """
        params = base.get_params(None, locals(),
                                 translate_param=translate_param)
        request = http.Request('GET', self.get_url('ga'), params)

        return request, parsers.parse_json

    @base.apimethod
    def realtime(self, ids, metrics, dimensions=None, sort=None, filters=None,
                 max_results=None, fields=None, prettyPrint=None, userIp=None,
                 quotaUser=None, access_token=None, key=None ):
        """
        Returns real-time data for a view (profile)

        :var ids: The unique table ID of the form ga:XXXX, where XXXX is the
            Analytics view (profile) ID for which the query will retrieve the
            data.
        :vartype ids: str

        :var metrics: A list of comma-separated metrics, such as
            ga:visits,ga:bounces.
        :vartype metrics: str

        :var dimensions: A list of comma-separated dimensions for your
            Analytics data, such as ga:browser,ga:city.
        :vartype dimensions: str

        :var sort A list of comma-separated dimensions and metrics indicating
            the sorting order and sorting direction for the returned data.
        :vartype sort: str

        :var filters: Dimension or metric filters that restrict the data
            returned for your request.
        :vartype filters: str

        :var max-results: The maximum number of rows to include in the response
        :vartype max-results: int

        :var fields: Selector specifying a subset of fields to include in the
            response.

        :var prettyPrint: Returns response with indentations and line breaks.
            Default false.
        :vartype prettyPrint: bool

        :var userIp: Specifies IP address of the end user for whom the API call
            is being made. Used to cap usage per IP.
        :vartype userIp: str

        :var quotaUser: Alternative to userIp in cases when the user's IP
            address is unknown.
        :vartype quotaUser: str

        """
        params = base.get_params(None, locals(),
                                 translate_param=translate_param)
        request = http.Request('GET', self.get_url('realtime'), params)

        return request, parsers.parse_json
