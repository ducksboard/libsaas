from libsaas import http, parsers
from libsaas.services import base


class CompeteResource(base.RESTResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Metric(CompeteResource):

    path = 'trended'

    def get_url(self):
        return '{0}/'.format(super(Metric, self).get_url())

    @base.apimethod
    def get(self, latest=None, start_date=None, end_date=None):
        """
        Fetch the object's data.

        :var latest: Returns the latest N months or days.
            If omitted, it returns data for the most recent 13 months
            for a monthly metric. For daily metrics, it returns data for
            the most recent 30 days.
        :vartype latest: int
        :var start_date: Return specific start date.
            If omitted, it returns data for the most recent 13 months
            for a monthly metric. For daily metrics, it returns data for
            the most recent 30 days.
        :vartype start_date: str
        :var end_date: Returns specific end date.
            If omitted, it returns data for the most recent 13 months
            for a monthly metric. For daily metrics, it returns data for
            the most recent 30 days.
        :vartype end_date: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class Site(CompeteResource):

    path = 'sites'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(Metric)
    def metric(self, metric_id):
        """
        Return the resource corresponding to a single metric for the site.
        """
        return Metric(self, metric_id)
