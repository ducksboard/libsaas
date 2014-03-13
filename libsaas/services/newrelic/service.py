import json

from libsaas import http, parsers
from libsaas.services import base


class Insights(base.Resource):
    """
    """
    version = 'beta_api'

    def __init__(self, account_id, query_key=None, insert_key=None):
        """
        Create a New Relic Insights service.

        :var account_id: The account id
        :vartype account_id: str

        :var query_key: The query key.
        :vartype query_key: str

        :var insert_key: The insert key.
        :vartype insert_key: str
        """
        tmpl = 'https://insights.newrelic.com/{0}/accounts/{1}'
        self.apiroot = tmpl.format(self.version, account_id)

        self.query_key = query_key
        self.insert_key = insert_key

        self.add_filter(self.add_authorization)
        self.add_filter(self.use_json)

    def use_json(self, request):
        request.headers['Content-Type'] = 'application/json'
        request.headers['Accept'] = 'application/json'

        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = json.dumps(request.params)

    def add_authorization(self, request):
        if request.method.upper() == 'POST':
            request.headers['X-Insert-Key'] = self.insert_key
        else:
            request.headers['X-Query-Key'] = self.query_key

    def get_url(self):
        return self.apiroot

    @base.apimethod
    def query(self, nrql):
        """
        NRQL query

        :var nqrl: The nrql query
        :vartype nqrl: str

        Upstream documentation: http://docs.newrelic.com/docs/rubicon/using-nrql
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'query')

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def insert(self, events):
        """
        Submit event or events to rubicon

        :var events: Event data
        :vartype event: dict

        Upstream documentation: http://docs.newrelic.com/docs/rubicon/inserting-events
        """
        url = '{0}/{1}'.format(self.get_url(), 'events')

        return http.Request('POST', url, events), parsers.parse_json
