from libsaas import http, parsers

from libsaas.services import base
from .base import YouTubeBaseResource


def translate_param(val):
    return val.replace('_', '-')


class Analytics(YouTubeBaseResource):
    """
    The YouTube Analytics API currently provides a single method that lets
    you retrieve Analytics reports for a YouTube channel.

    https://developers.google.com/youtube/analytics/v1/available_reports.html
    identifies the different reports that you can retrieve. For each report,
    it lists the dimensions that are used to aggregate data,
    available metrics, and supported filtering options.
    """

    APIROOT = 'https://www.googleapis.com/youtube/analytics/v1/reports'

    @base.apimethod
    def get(self, ids, metrics, start_date, end_date, dimensions=None,
           filters=None, max_results=None, start_index=None, sort=None):
        """
        Retrieve YouTube Analytics data

        :var ids: Identifies the YouTube channel or content owner for which
            you are retrieving YouTube Analytics data. To request data for
            a YouTube user, set the ids parameter value to channel==USER_ID.
            To request data for a YouTube CMS content owner, set the ids
            parameter value to contentOwner==OWNER_NAME
        :vartype ids: str

        :var metrics: A comma-separated list of YouTube Analytics metrics,
            such as views or likes,dislikes. See {reports} for a list of the
            reports that you can retrieve and the metrics available in each
            report, and see{metrics} for definitions of those metrics.
        :vartype metrics: str

        :var start_date: The start date for fetching YouTube Analytics data.
            The value should be in YYYY-MM-DD format.
        :vartype start_date: str

        :var end_date: The start date for fetching YouTube Analytics data.
            The value should be in YYYY-MM-DD format.
        :vartype end_date: str

        :var dimensions: A comma-separated list of YouTube Analytics
            dimensions, such as video or ageGroup,gender. See {reports}
            for a list of the reports that you can retrieve and the
            dimensions used for those reports. Also see {dimensions} for
            definitions of those dimensions.
        :vartype dimensions: str

        :var filters: A list of filters that should be applied when retrieving
            YouTube Analytics data. The {reports} identifies the dimensions
            that can be used to filter each report, and {dimensions} defines
            those dimensions. If a request uses multiple filters, join them
            together with a semicolon (;), and the returned result table will
            satisfy both filters. For example, a filters parameter value of
            video==dMH0bHeiRNg;country==IT restricts the result set to include
            data for the given video in Italy.
        :vartype filters: str

        :var max_results: The maximum number of rows to include in the response
        :vartype max_results: str

        :var start_index: The 1-based index of the first entity to retrieve.
            Use this parameter as a pagination mechanism along with the
            max-results parameter.
        :vartype start_index: int

        :var sort: A comma-separated list of dimensions or metrics that
            determine the sort order for YouTube Analytics data. By default
            the sort order is ascending. The '-' prefix causes descending
            sort order
        :vartype sort: str
        """
        params = base.get_params(None, locals(),
                                 translate_param=translate_param)

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json

    get.__doc__ = get.__doc__.format(
        reports='https://developers.google.com/youtube/analytics'
        '/v1/available_reports.html',
        metrics='https://developers.google.com/youtube/analytics'
        '/v1/dimsmets/mets.html',
        dimensions='https://developers.google.com/youtube/analytics'
        '/v1/dimsmets/dims')

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
