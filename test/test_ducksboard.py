import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import ducksboard


class DucksboardTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = ducksboard.Ducksboard('apikey', 'pass')

    def serialize(self, data):
        return json.dumps(data)

    def expect(self, uri, method=None, params=None, subdomain=None):
        if not subdomain:
            domain = 'app.ducksboard.com/api'
        else:
            domain = '{0}.ducksboard.com/values'.format(subdomain)

        self.assertEqual(self.executor.request.uri,
                         'https://{0}/{1}'.format(domain, uri))
        if method:
            self.assertEqual(method, self.executor.request.method)
        if params:
            self.assertEqual(self.executor.request.params, params)

    def test_dashboard(self):
        self.service.dashboards().get()
        self.expect('dashboards/', 'GET')

        dashboard = {'name': 'x'}
        self.service.dashboards().create(dashboard)
        self.expect('dashboards/', 'POST', self.serialize(dashboard))

        self.service.dashboard('slug').update(dashboard)
        self.expect('dashboards/slug', 'PUT', self.serialize(dashboard))

        self.service.dashboard('slug').delete()
        self.expect('dashboards/slug', 'DELETE')

        self.service.dashboard('slug').accessed()
        self.expect('dashboards/slug/accessed', 'POST')

        self.service.dashboard('slug').widgets()
        self.expect('dashboards/slug/widgets/', 'GET')

        self.service.dashboard('slug').tokens().get()
        self.expect('dashboards/slug/tokens/', 'GET')

        self.service.dashboard('slug').token('token').get()
        self.expect('dashboards/slug/tokens/token', 'GET')

        token = {'password': 'p'}
        self.service.dashboard('slug').tokens().create(token)
        self.expect('dashboards/slug/tokens/', 'POST', self.serialize(token))

        self.service.dashboard('slug').token('token').delete()
        self.expect('dashboards/slug/tokens/token', 'DELETE')

    def test_widgets(self):
        self.service.widgets().get()
        self.expect('widgets/', 'GET')

        widget = {'widget': 'x'}
        self.service.widgets().create(widget)
        self.expect('widgets/', 'POST', self.serialize(widget))

        self.service.widget('id').update(widget)
        self.expect('widgets/id', 'PUT', self.serialize(widget))

        self.service.widget('id').delete()
        self.expect('widgets/id', 'DELETE')

        dashboard = {'dashboard': 'test'}
        self.service.widget('id').copy('test')
        self.expect('widgets/id/copy', 'POST', self.serialize(dashboard))

        positions = {"7": {"row": 1, "column": 1}}
        self.service.widgets().positions(positions)
        self.expect('widgets/positions', 'POST', self.serialize(positions))

    def test_accounts(self):
        self.service.accounts().get()
        self.expect('accounts/', 'GET')

        account = {'account': 'x'}
        self.service.accounts().create(account)
        self.expect('accounts/', 'POST', self.serialize(account))

        self.service.account('id').delete()
        self.expect('accounts/id', 'DELETE')

        self.service.account('id').get()
        self.expect('accounts/id', 'GET')

    def test_user(self):
        self.service.user().get()
        self.expect('user', 'GET')

        user = {'name': 'x'}
        self.service.user().update(user)
        self.expect('user', 'PUT', self.serialize(user))

        self.service.user().get_api_key()
        self.expect('user/api_key', 'GET')

        self.service.user().reset_api_key()
        self.expect('user/api_key', 'POST')

    def test_datasource(self):
        ds = self.service.data_source('label')

        value = {"value": 10}
        ds.push(value)
        self.expect('label', 'POST', self.serialize(value), 'push')

        ds.delete()
        self.expect('label', 'DELETE', subdomain='push')

        ds.last(5)
        self.expect('label/last', 'GET', {'count': 5}, subdomain='pull')

        ds.since(500)
        self.expect('label/since', 'GET', {'seconds': 500}, subdomain='pull')

        ds.timespan('daily', 'UTC')
        self.expect('label/timespan', 'GET',
                    {'timespan': 'daily', 'timezone': 'UTC'},
                    subdomain='pull')
