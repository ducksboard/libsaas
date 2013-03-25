from libsaas import http, parsers
from libsaas.services import base


class GoalsResource(base.RESTResource):

    path = 'goals'


class Goals(GoalsResource):
    pass


class Goal(GoalsResource):

    @base.apimethod
    def results(self, period_start=None, period_end=None):
        """
        Lists results of a specific goal.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Goals
        """
        params = base.get_params(None, locals())
        url = '{0}/results'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json
