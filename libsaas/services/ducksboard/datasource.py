import json

from libsaas import http, parsers, port

from libsaas.filters import auth
from libsaas.services import base


class Datasource(base.Resource):
    """
    """
    def __init__(self, apikey, label):
        """
        Get a datasource resource.

        :var apikey: Your API key.
        :vartype apikey: str

        :var label: data source label
        :vartype label: str
        """
        self.url_tmpl = 'https://{0}.ducksboard.com/values/{1}'
        self.label = label

        self.add_filter(auth.BasicAuth(apikey, None))
        self.add_filter(self.use_json)

    def use_json(self, request):
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = json.dumps(request.params)

    def get_url(self, api):
        return self.url_tmpl.format(api, port.to_u(self.label))

    def get_pull_url(self):
        return self.get_url('pull')

    def get_push_url(self):
        return self.get_url('push')

    @base.apimethod
    def push(self, obj):
        """
        Send a value or a list of values. Each value can have a timestamp
        associated with it. Timestamps should be UNIX timestamps expressed
        as numbers. If no timestamp is specified, the value is assumed to be
        timestamped with the current time.

        :var obj: a Python object representing the value to push to the
            data source.
            See http://dev.ducksboard.com/apidoc/push-api/#post-values-label
        """
        request = http.Request('POST', self.get_push_url(), obj)
        return request, parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Delete all data for a given data source.
        """
        request = http.Request('DELETE', self.get_push_url(), None)
        return request, parsers.parse_empty

    @base.apimethod
    def last(self, count=None):
        """
        Get the last count values for a given data source, ordered by their
        timestamp, newest data first. This resource can be used for all data
        sources.

        :var count: The amount of data returned. It might be less than the
            count parameter. The default value for count is 3 and the maximum
            is 100.
        :vartype count: int
        """
        url = '{0}/{1}'.format(self.get_pull_url(), 'last')
        params = base.get_params(('count',), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def since(self, seconds=None):
        """
        Get the values from up to seconds ago for a given data source,
        ordered by their timestamp, newest data first.
        This resource can be used for all data sources.

        :var seconds: The first value returned might actually be from later
            than seconds ago. The default value for seconds is 3600 and the
            maximum is 7776000.
        :vartype seconds: int
        """
        url = '{0}/{1}'.format(self.get_pull_url(), 'since')
        params = base.get_params(('seconds',), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def timespan(self, timespan=None, timezone=None):
        """
        Get the last value for a series of periods for a given data source.
        The number of values returned depends on the timespan parameter.
        If a certain period is empty, meaning that no values from inside of
        it are found, the value of the previous period is substituted, or
        null if no previous values were found.
        See {0}

        :var timespan: The allowed values for timespan are daily, weekly
            and monthly, with the default of monthly.
        :vartype timespan: str

        :var timezone: The limits of periods are actually dependent on the
            timezone parameter, as depending on which timezone you want to
            see the data in, the last value of each period might be different.
            The default for timezone is UTC.
        :vartype timezone: str
        """
        url = '{0}/{1}'.format(self.get_pull_url(), 'timespan')
        params = base.get_params(('timespan', 'timezone'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    timespan.__doc__ = timespan.__doc__.format(
        'http://dev.ducksboard.com/apidoc/pull-api-http/#get-values-label-'
        'timespan-timespan-timespan-timezone-timezone')
