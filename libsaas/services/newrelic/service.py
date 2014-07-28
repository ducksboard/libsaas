import json

from libsaas import http, parsers
from libsaas.services import base

from . import (applications, application_hosts, application_instances,
               key_transactions, servers, alert_policies,
               notification_channels, users, plugins, components)


class NewRelic(base.Resource):
    """
    """
    def __init__(self, api_key):
        """
        Create a New Relic service.

        :var api_key: The API key.
        :vartipe api_key: str
        """
        self.apiroot = 'https://api.newrelic.com/v2'
        self.api_key = api_key

        self.add_filter(self.add_authorization)
        self.add_filter(self.use_json)

    def get_url(self):
        return self.apiroot

    def add_authorization(self, request):
        request.headers['x-api-key'] = self.api_key

    def use_json(self, request):
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = json.dumps(request.params)

    @base.resource(applications.Application)
    def application(self, application_id):
        """
        Return the resource corresponding to a single Application.
        """
        return applications.Application(self, application_id)

    @base.resource(applications.Applications)
    def applications(self):
        """
        Return the resource corresponding to all Applications.
        """
        return applications.Applications(self)

    @base.resource(application_hosts.ApplicationHost)
    def application_host(self, application_id, host_id):
        """
        Return the resource corresponding to a single host associated with an
        Application.
        """
        return application_hosts.ApplicationHost(self, application_id, host_id)

    @base.resource(application_hosts.ApplicationHosts)
    def application_hosts(self, application_id):
        """
        Return the resource corresponding to all hosts associated with an
        Application.
        """
        return application_hosts.ApplicationHosts(self, application_id)

    @base.resource(application_instances.ApplicationInstance)
    def application_instance(self, application_id, instance_id):
        """
        Return the resource corresponding to a single instance associated with
        an Application.
        """
        return application_instances.ApplicationInstance(self, application_id,
            instance_id)

    @base.resource(application_instances.ApplicationInstances)
    def application_instances(self, application_id):
        """
        Return the resource corresponding to all instances associated with an
        Application.
        """
        return application_instances.ApplicationInstances(self, application_id)

    @base.resource(key_transactions.KeyTransaction)
    def key_transaction(self, key_transaction_id):
        """
        Return the resource corresponding to a single Key transaction.
        """
        return key_transactions.KeyTransaction(self, key_transaction_id)

    @base.resource(key_transactions.KeyTransactions)
    def key_transactions(self):
        """
        Return the resource corresponding to all Key transactions.
        """
        return key_transactions.KeyTransactions(self)

    @base.resource(servers.Server)
    def server(self, server_id):
        """
        Return the resource corresponding to a single Server.
        """
        return servers.Server(self, server_id)

    @base.resource(servers.Servers)
    def servers(self):
        """
        Return the resource corresponding to all Servers.
        """
        return servers.Servers(self)

    @base.resource(alert_policies.AlertPolicy)
    def alert_policy(self, alert_policy_id):
        """
        Return the resource corresponding to a single Alert Policy.
        """
        return alert_policies.AlertPolicy(self, alert_policy_id)

    @base.resource(alert_policies.AlertPolicies)
    def alert_policies(self):
        """
        Return the resource corresponding to all Alert Policies.
        """
        return alert_policies.AlertPolicies(self)

    @base.resource(notification_channels.NotificationChannel)
    def notification_channel(self, notification_channel_id):
        """
        Return the resource corresponding to a single Notification Channel.
        """
        return notification_channels.NotificationChannel(self, notification_channel_id)

    @base.resource(notification_channels.NotificationChannels)
    def notification_channels(self):
        """
        Return the resource corresponding to all Notification Channels.
        """
        return notification_channels.NotificationChannels(self)

    @base.resource(users.User)
    def user(self, user_id):
        """
        Return the resource corresponding to a single User.
        """
        return users.User(self, user_id)

    @base.resource(users.Users)
    def users(self):
        """
        Return the resource corresponding to all Users.
        """
        return users.Users(self)

    @base.resource(plugins.Plugin)
    def plugin(self, plugin_id):
        """
        Return the resource corresponding to a single Plugin.
        """
        return plugins.Plugin(self, plugin_id)

    @base.resource(plugins.Plugins)
    def plugins(self):
        """
        Return the resource corresponding to all Plugins.
        """
        return plugins.Plugins(self)

    @base.resource(components.Component)
    def component(self, component_id):
        """
        Return the resource corresponding to a single plugin Component.
        """
        return components.Component(self, component_id)

    @base.resource(components.Components)
    def components(self):
        """
        Return the resource corresponding to all plugin Components.
        """
        return components.Components(self)


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
