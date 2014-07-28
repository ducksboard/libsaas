from libsaas import http, parsers
from libsaas.services import base

from .resource import NewRelicResource


class AlertPolicies(NewRelicResource):

    path = 'alert_policies'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, name=None, type=None, ids=None, enabled=None, page=None):
        """
        List of the Alert Policies associated with your New Relic account.

        :var name: Filter by name.
        :vartype name: str

        :var type: Filter by policy types.
        :vartype type: str

        :var ids: Filter by ids.
        :vartype ids: str

        :var enabled: Select only enabled/disabled policies (default: both).
        :vartype enabled: bool

        :var page: Pagination index.
        :vartype page: int
        """
        params = base.get_params(None, locals())
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json


class AlertPolicy(NewRelicResource):

    path = 'alert_policies'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self):
        """
        Fetch a single Alert Policy.
        """
        url = '{0}.json'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json

    @base.apimethod
    def update(self, alert_policy):
        """
        Update certain parameters of an Alert Policy.

        :var alert_policy: Representation of the Alert Policy object.
        :vartype alert_policy: str
        """
        params = base.get_params(None, locals())
        url = '{0}.json'.format(self.get_url())
        request = http.Request('PUT', url, params)

        return request, parsers.parse_json
