import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import newrelic


class NewRelicTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = newrelic.NewRelic('my_api_key')

    def expect(self, method=None, uri=None, params=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                'https://api.newrelic.com/v2' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)

        headers = {'x-api-key': 'my_api_key'}
        self.assertEqual(self.executor.request.headers, headers)

    def test_applications(self):
        params = {
            'name': 'test,',
            'ids': '999999,',
            'language': 'python',
            'page': 2
        }
        self.service.applications().get(**params)
        self.expect('GET', '/applications.json', params)

        id = 999999
        self.service.application(id).get()
        self.expect('GET', '/applications/{0}.json'.format(id))

        params = {
            'application': {'application': {'name': 'foo'}}
        }
        self.service.application(id).update(**params)
        self.expect('PUT', '/applications/{0}.json'.format(id),
            json.dumps(params))

        self.service.application(id).delete()
        self.expect('DELETE', '/applications/{0}.json'.format(id))

        params = {
            'name': 'ActiveRecord/all',
            'page': 2
        }
        self.service.application(id).metric_names(**params)
        self.expect('GET', '/applications/{0}/metrics.json'.format(id), params)

        params = {
            'names': 'ActiveRecord/all',
            'values': 'average_response_time',
            'from_datetime': '2014-07-20T10:03:00+00:00',
            'to_datetime': '2014-07-28T10:03:00+00:00'
        }
        self.service.application(id).metric_data(**params)
        params['from'] = params.pop('from_datetime')
        params['to'] = params.pop('to_datetime')
        self.expect('GET', '/applications/{0}/metrics/data.json'.format(id),
            params)

    def test_application_hosts(self):
        app_id = 999999
        params = {
            'hostname': 'foo',
            'ids': '888888,',
            'page': 2
        }
        self.service.application_hosts(app_id).get(**params)
        self.expect('GET', '/applications/{0}/hosts.json'.format(app_id),
            params)

        host_id = 888888
        self.service.application_host(app_id, host_id).get()
        self.expect('GET', '/applications/{0}/hosts/{1}.json'.format(app_id,
            host_id))

        params = {
            'name': 'ActiveRecord/all',
            'page': 2
        }
        self.service.application_host(app_id, host_id).metric_names(**params)
        self.expect('GET', '/applications/{0}/hosts/{1}/metrics.json'.format(
            app_id, host_id), params)

        params = {
            'names': 'ActiveRecord/all',
            'values': 'average_response_time',
            'from_datetime': '2014-07-20T10:03:00+00:00',
            'to_datetime': '2014-07-28T10:03:00+00:00'
        }
        self.service.application_host(app_id, host_id).metric_data(**params)
        params['from'] = params.pop('from_datetime')
        params['to'] = params.pop('to_datetime')
        self.expect('GET',
            '/applications/{0}/hosts/{1}/metrics/data.json'.format(app_id,
                host_id), params)

    def test_applications_instances(self):
        app_id = 999999
        params = {
            'hostname': 'foo',
            'ids': '888888,',
            'page': 2
        }
        self.service.application_instances(app_id).get(**params)
        self.expect('GET', '/applications/{0}/instances.json'.format(app_id),
            params)

        instance_id = 888888
        self.service.application_instance(app_id, instance_id).get()
        self.expect('GET', '/applications/{0}/instances/{1}.json'.format(
            app_id, instance_id))

        params = {
            'name': 'ActiveRecord/all',
            'page': 2
        }
        self.service.application_instance(app_id, instance_id).metric_names(
            **params)
        self.expect('GET',
            '/applications/{0}/instances/{1}/metrics.json'.format(
                app_id, instance_id), params)

        params = {
            'names': 'ActiveRecord/all',
            'values': 'average_response_time',
            'from_datetime': '2014-07-20T10:03:00+00:00',
            'to_datetime': '2014-07-28T10:03:00+00:00'
        }
        self.service.application_instance(app_id, instance_id).metric_data(
            **params)
        params['from'] = params.pop('from_datetime')
        params['to'] = params.pop('to_datetime')
        self.expect('GET',
            '/applications/{0}/instances/{1}/metrics/data.json'.format(app_id,
                instance_id), params)

    def test_key_transactions(self):
        params = {
            'name': 'test,',
            'ids': '999999,',
            'page': 2
        }
        self.service.key_transactions().get(**params)
        self.expect('GET', '/key_transactions.json', params)

        id = 9999999
        self.service.key_transaction(id).get()
        self.expect('GET', '/key_transactions/{0}.json'.format(id))

    def test_servers(self):
        params = {
            'name': 'test,',
            'ids': '999999,',
            'page': 2
        }
        self.service.servers().get(**params)
        self.expect('GET', '/servers.json', params)

        id = 999999
        self.service.server(id).get()
        self.expect('GET', '/servers/{0}.json'.format(id))

        params = {
            'server': {'server': {'name': 'foo'}}
        }
        self.service.server(id).update(**params)
        self.expect('PUT', '/servers/{0}.json'.format(id), json.dumps(params))

        self.service.server(id).delete()
        self.expect('DELETE', '/servers/{0}.json'.format(id))

        params = {
            'name': 'ActiveRecord/all',
            'page': 2
        }
        self.service.server(id).metric_names(**params)
        self.expect('GET', '/servers/{0}/metrics.json'.format(id), params)

        params = {
            'names': 'ActiveRecord/all',
            'values': 'average_response_time',
            'from_datetime': '2014-07-20T10:03:00+00:00',
            'to_datetime': '2014-07-28T10:03:00+00:00'
        }
        self.service.server(id).metric_data(**params)
        params['from'] = params.pop('from_datetime')
        params['to'] = params.pop('to_datetime')
        self.expect('GET', '/servers/{0}/metrics/data.json'.format(id), params)

    def test_alert_policies(self):
        params = {
            'name': 'test,',
            'type': 'server',
            'ids': '999999,',
            'page': 2
        }
        self.service.alert_policies().get(**params)
        self.expect('GET', '/alert_policies.json', params)

        id = 999999
        self.service.alert_policy(id).get()
        self.expect('GET', '/alert_policies/{0}.json'.format(id))

        params = {
            'alert_policy': {'alert_policy': {'name': 'foo'}}
        }
        self.service.alert_policy(id).update(**params)
        self.expect('PUT', '/alert_policies/{0}.json'.format(id),
            json.dumps(params))

    def test_notification_channels(self):
        params = {
            'type': 'server',
            'ids': '999999,',
            'page': 2
        }
        self.service.notification_channels().get(**params)
        self.expect('GET', '/notification_channels.json', params)

        id = 999999
        self.service.notification_channel(id).get()
        self.expect('GET', '/notification_channels/{0}.json'.format(id))

    def test_users(self):
        params = {
            'ids': '999999,',
            'email': 'test@ducksboard.com',
            'page': 2
        }
        self.service.users().get(**params)
        self.expect('GET', '/users.json', params)

        id = 999999
        self.service.user(id).get()
        self.expect('GET', '/users/{0}.json'.format(id))

    def test_plugins(self):
        params = {
            'guids': '888888,',
            'ids': '999999,',
            'page': 2
        }
        self.service.plugins().get(**params)
        self.expect('GET', '/plugins.json', params)

        id = 999999
        self.service.plugin(id).get()
        self.expect('GET', '/plugins/{0}.json'.format(id))

    def test_components(self):
        params = {
            'name': 'test,',
            'ids': '999999,',
            'plugin_id': 888888,
            'page': 2
        }
        self.service.components().get(**params)
        self.expect('GET', '/components.json', params)

        id = 999999
        self.service.component(id).get()
        self.expect('GET', '/components/{0}.json'.format(id))

        params = {
            'name': 'ActiveRecord/all',
            'page': 2
        }
        self.service.component(id).metric_names(**params)
        self.expect('GET', '/components/{0}/metrics.json'.format(id), params)

        params = {
            'names': 'ActiveRecord/all',
            'values': 'average_response_time',
            'from_datetime': '2014-07-20T10:03:00+00:00',
            'to_datetime': '2014-07-28T10:03:00+00:00'
        }
        self.service.component(id).metric_data(**params)
        params['from'] = params.pop('from_datetime')
        params['to'] = params.pop('to_datetime')
        self.expect('GET', '/components/{0}/metrics/data.json'.format(id),
            params)


class InsightsTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.insert_key = 'insert_key'
        self.query_key = 'query_key'
        self.account_id = 'account_id'
        self.service = newrelic.Insights(self.account_id, self.query_key,
                                         self.insert_key)

    def serialize(self, data):
        return json.dumps(data)

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if self.executor.request.method.upper() == 'POST':
            self.assertEqual(self.executor.request.headers['X-Insert-Key'],
                             self.insert_key)
        else:
            self.assertEqual(self.executor.request.headers['X-Query-Key'],
                             self.query_key)

        if uri:
            tmpl = 'https://insights-{0}.newrelic.com/v1/accounts/{1}/{2}'
            sufix = 'api' if uri == 'query' else 'collector'
            url = tmpl.format(sufix, self.account_id, uri)
            self.assertEqual(self.executor.request.uri, url)
        if params:
            self.assertEqual(self.executor.request.params, params)

    def test_insert(self):
        events = [{'eventType': 'test', 'amount': 10}]
        self.service.insert(events)
        self.expect('POST', 'events', self.serialize(events))

    def test_sql(self):
        query = 'select * from TestEvent'
        self.service.query(query)
        self.expect('GET', 'query', {'nrql': query})
