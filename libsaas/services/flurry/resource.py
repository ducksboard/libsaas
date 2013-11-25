from libsaas.services import base
from libsaas import http, parsers


def to_camelcase(val):
    words = val.split('_')
    words = [words[0].lower()] + [x.capitalize() for x in words[1:]]
    return ''.join(words)


class Metrics(base.HierarchicalResource):
    path = 'appMetrics'

    def get_url(self):
        grandparent = self.parent.parent
        return '{0}/{1}'.format(grandparent.get_url(), self.path)

    def _get(self, metric_name, start_date, end_date,
             country=None, version_name=None, group_by=None):
        params = base.get_params(None, locals(),
                                 translate_param=to_camelcase)
        params.pop('metricName')

        url = '{0}/{1}'.format(self.get_url(), metric_name)

        request = http.Request('GET', url, params)
        return request, parsers.parse_json

    @base.apimethod
    def active_users(self, *args, **kwargs):
        """
        Returns the total number of unique users who accessed
        the application per day.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('ActiveUsers', *args, **kwargs)

    @base.apimethod
    def active_users_by_week(self, *args, **kwargs):
        """
        Returns the total number of unique users who accessed
        the application per week

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('ActiveUsersByWeek', *args, **kwargs)

    @base.apimethod
    def active_users_by_month(self, *args, **kwargs):
        """
        Returns the total number of unique users who accessed
        the application per month.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('ActiveUsersByMonth', *args, **kwargs)

    @base.apimethod
    def new_users(self, *args, **kwargs):
        """
        Returns the total number of unique users who used the
        application for the first time per day.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('NewUsers', *args, **kwargs)

    @base.apimethod
    def median_session_length(self, *args, **kwargs):
        """
        Returns the median length of a user session per day.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('MedianSessionLength', *args, **kwargs)

    @base.apimethod
    def avg_session_length(self, *args, **kwargs):
        """
        Returns the average length of a user session per day.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('AvgSessionLength', *args, **kwargs)

    @base.apimethod
    def sessions(self, *args, **kwargs):
        """
        Returns the total number of times users accessed
        the application per day.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('Sessions', *args, **kwargs)

    @base.apimethod
    def retained_users(self, *args, **kwargs):
        """
        Returns the total number of users who remain active users of
        the application per day.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('RetainedUsers', *args, **kwargs)

    @base.apimethod
    def page_views(self, *args, **kwargs):
        """
        Returns the total number of page views per day.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('PageViews', *args, **kwargs)

    @base.apimethod
    def avg_page_views_per_session(self, *args, **kwargs):
        """
        Returns the average page views per session for each day.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var country: optional parameter indicating user's country.
        :vartype country: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str

        :var group_by: group data by DAYS, WEEKS or MONTHS.
            By default, it will group data by days.
        :vartype group_by: str
        """
        return self._get('AvgPageViewsPerSession', *args, **kwargs)


class EventResource(base.HierarchicalResource):
    def __init__(self, parent, object_id=None):
        self.parent = parent
        self.object_id = object_id

    def get_url(self):
        grandparent = self.parent.parent
        return '{0}/eventMetrics/{1}'.format(grandparent.get_url(), self.path)

    @base.apimethod
    def get(self, start_date, end_date, version_name=None):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.

        :var start_date: the first date to look metrics for.
        :vartype start_date: str

        :var end_date: the last date to look metrics for.
        :vartype end_date: str

        :var version_name: optional parameter indicating application's version.
        :vartype version_name: str
        """
        params = base.get_params(None, locals(),
                                 translate_param=to_camelcase)
        if self.object_id:
            params['eventName'] = self.object_id

        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class Events(EventResource):
    path = 'Summary'


class Event(EventResource):
    path = 'Event'


class ApplicationResource(base.HierarchicalResource):

    @base.apimethod
    def get(self):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json


class Application(ApplicationResource):
    path = 'appInfo/getApplication'

    def __init__(self, parent, application_api_key):
        super(Application, self).__init__(parent)

        self.application_api_key = application_api_key
        self.add_filter(self.add_authorization)

    def add_authorization(self, request):
        request.params['apiKey'] = self.application_api_key

    @base.resource(Metrics)
    def metrics(self):
        """
        Returns the resource corresponding to all metrics.
        """
        return Metrics(self)

    @base.resource(Events)
    def events(self):
        """
        Return the resource corresponding to all events.
        """
        return Events(self)

    @base.resource(Event)
    def event(self, event_name):
        """
        Returns the resource corresponding to a single event.
        """
        return Event(self, event_name)


class Applications(ApplicationResource):
    path = 'appInfo/getAllApplications'
