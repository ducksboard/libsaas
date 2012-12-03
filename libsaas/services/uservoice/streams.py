from libsaas import http, parsers
from libsaas.services import base


class Stream(base.HierarchicalResource):

    path = 'stream'

    @base.apimethod
    def public(self, date=None, filter=[], since=None):
        """
        Fetch all public events.

        :var date: Fetch only events from that day (EST). See upstream
            documentation for details.
        :vartype date: str

        :var filter: Specify which event types you want. See upstream
            documentation for allowed values.
        :var filter: list

        :var since: Fetch events from that moment onward. If set, the `date`
            parameter is ignored See upstream documentation for details.
        :vartype since: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'public')

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def private(self, date=None, filter=[], since=None):
        """
        Fetch all private events.

        :var date: Fetch only events from that day (EST). See upstream
            documentation for details.
        :vartype date: str

        :var filter: Specify which event types you want. See upstream
            documentation for allowed values.
        :var filter: list

        :var since: Fetch events from that moment onward. If set, the `date`
            parameter is ignored See upstream documentation for details.
        :vartype since: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'private')

        return http.Request('GET', url, params), parsers.parse_json
