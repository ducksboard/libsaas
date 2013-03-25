import json
import unittest

from libsaas import http, port
from libsaas.executors import test_executor
from libsaas.services import pipedrive
from libsaas.services.base import MethodNotSupported


class PipedriveTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = pipedrive.Pipedrive('my-api-token')

    def serialize(self, data):
        return json.dumps(data)

    def expect(self, method=None, uri=None, params=None):
        if method:
            self.assertEqual(method, self.executor.request.method)

        params = params or {}
        if method in http.URLENCODE_METHODS:
            params.update({'api_token': 'my-api-token'})
        else:
            uri += '?api_token=my-api-token'
            params = self.serialize(params)

        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://api.pipedrive.com/v1' + uri)

        self.assertEqual(self.executor.request.params, params)

    def test_activity_types(self):
        atype = {'name': 'test', 'color': 'FFFFFF'}

        self.service.activity_types().get()
        self.expect('GET', '/activityTypes')
        self.service.activity_types().create(atype)
        self.expect('POST', '/activityTypes', atype)
        self.service.activity_types().delete(ids='1,2,3')
        self.expect('DELETE', '/activityTypes', {'ids': '1,2,3'})

        self.service.activity_type('1').get()
        self.expect('GET', '/activityTypes/1')
        self.service.activity_type('1').update(atype)
        self.expect('PUT', '/activityTypes/1', atype)
        self.service.activity_type('1').delete()
        self.expect('DELETE', '/activityTypes/1')

    def test_activities(self):
        a = {'subject': 'test'}

        self.service.activities().get(user_id=1, start=10, limit=50)
        self.expect('GET', '/activities', {'user_id': 1, 'start': 10,
                                              'limit': 50})
        self.service.activities().create(a)
        self.expect('POST', '/activities', a)
        self.service.activities().delete(ids='1,2,3')
        self.expect('DELETE', '/activities', {'ids': '1,2,3'})

        self.service.activity('1').get()
        self.expect('GET', '/activities/1')
        self.service.activity('1').update(a)
        self.expect('PUT', '/activities/1', a)
        self.service.activity('1').delete()
        self.expect('DELETE', '/activities/1')

    def test_authorizations(self):
        self.service.authorizations().get('u@d.com', 'boo')
        self.expect('POST', '/authorizations',
                    {'email': 'u@d.com', 'password': 'boo'})

    def test_user_connections(self):
        self.service.user_connections().get()
        self.expect('GET', '/userConnections')

    def test_users(self):
        with port.assertRaises(MethodNotSupported):
            self.service.user(4).delete()
            self.service.user(4).update()

        paging = {'start': 100, 'limit': 50}
        u = {'name': 'Mr. Brown', 'email': 'b@d.com'}

        self.service.users().get()
        self.expect('GET', '/users')
        self.service.users().create(u)
        self.expect('POST', '/users', u)
        self.service.users().find('brown')
        self.expect('GET', '/users/find', {'term': 'brown'})

        self.service.user(1).get()
        self.expect('GET', '/users/1')
        self.service.user(1).followers()
        self.expect('GET', '/users/1/followers')
        self.service.user(1).activities(start=100, limit=50)
        self.expect('GET', '/users/1/activities', paging)
        self.service.user(1).updates(start=100, limit=50)
        self.expect('GET', '/users/1/updates', paging)
        self.service.user(1).merge(4)
        self.expect('POST', '/users/1/merge', {'merge_with_id': 4})

    def test_currencies(self):
        self.service.currencies().get('US')
        self.expect('GET', '/currencies', {'term': 'US'})

    def test_deal_fields(self):
        with port.assertRaises(MethodNotSupported):
            self.service.deal_field(4).update()

        field = {'name': 'test'}

        self.service.deal_fields().get()
        self.expect('GET', '/dealFields')
        self.service.deal_fields().create(field)
        self.expect('POST', '/dealFields', field)
        self.service.deal_fields().delete(ids='1,2,3')
        self.expect('DELETE', '/dealFields', {'ids': '1,2,3'})

        self.service.deal_field(1).get()
        self.expect('GET', '/dealFields/1')
        self.service.deal_field(1).delete()
        self.expect('DELETE', '/dealFields/1')

    def test_deals(self):
        paging = {'start': 100, 'limit': 50}
        d = {'title': 'My cool Brown'}

        self.service.deals().get(start=100, limit=50)
        self.expect('GET', '/deals', paging)
        self.service.deals().create(d)
        self.expect('POST', '/deals', d)
        self.service.deals().find('brown')
        self.expect('GET', '/deals/find', {'term': 'brown'})
        self.service.deals().delete(ids='1,2,3')
        self.expect('DELETE', '/deals', {'ids': '1,2,3'})
        self.service.deals().timeline('2013-01-01', 'day', 30, 'key')
        self.expect('GET', '/deals/timeline',
                    {'start_date': '2013-01-01', 'interval': 'day',
                     'amount': 30, 'field_key': 'key'})

        self.service.deal(1).get()
        self.expect('GET', '/deals/1')
        self.service.deal(1).followers()
        self.expect('GET', '/deals/1/followers')
        self.service.deal(1).participants(start=100, limit=50)
        self.expect('GET', '/deals/1/participants', paging)
        self.service.deal(1).updates(start=100, limit=50)
        self.expect('GET', '/deals/1/updates', paging)
        self.service.deal(1).files(start=100, limit=50)
        self.expect('GET', '/deals/1/files', paging)
        self.service.deal(1).products().get(start=100, limit=50)
        self.expect('GET', '/deals/1/products', paging)
        self.service.deal(1).products().delete(2)
        self.expect('DELETE', '/deals/1/products',
                    {'product_attachment_id': 2})
        p = {'product_id': 1, 'item_price': 100, 'amount': 2}
        self.service.deal(1).products().create(p)
        self.expect('POST', '/deals/1/products', p)

    def test_files(self):
        with port.assertRaises(MethodNotSupported):
            self.service.files().create()

        file = {'name': 'test'}
        paging = {'start': 100, 'limit': 50}

        self.service.files().get(start=100, limit=50)
        self.expect('GET', '/files', paging)
        self.service.file(1).get()
        self.expect('GET', '/files/1')
        self.service.file(1).delete()
        self.expect('DELETE', '/files/1')
        self.service.file(1).update(file)
        self.expect('PUT', '/files/1', file)

    def test_filter(self):
        with port.assertRaises(MethodNotSupported):
            self.service.condition_filters().create()

        self.service.condition_filters().get(type='deals')
        self.expect('GET', '/filters', {'type': 'deals'})
        self.service.condition_filters().delete('1,2,3')
        self.expect('DELETE', '/filters', {'ids': '1,2,3'})

        self.service.condition_filter(1).get()
        self.expect('GET', '/filters/1')
        self.service.condition_filter(1).delete()
        self.expect('DELETE', '/filters/1')

    def test_notes(self):
        note = {'content': '<h1>test</h1>'}
        paging = {'start': 100, 'limit': 50}

        self.service.notes().get(start=100, limit=50)
        self.expect('GET', '/notes', paging)
        self.service.notes().create(note)
        self.expect('POST', '/notes', note)

        self.service.note(1).get()
        self.expect('GET', '/notes/1')
        self.service.note(1).delete()
        self.expect('DELETE', '/notes/1')
        self.service.note(1).update(note)
        self.expect('PUT', '/notes/1', note)

    def test_organization_fields(self):
        with port.assertRaises(MethodNotSupported):
            self.service.organization_field(4).update()

        field = {'name': 'test'}

        self.service.organization_fields().get()
        self.expect('GET', '/organizationFields')
        self.service.organization_fields().create(field)
        self.expect('POST', '/organizationFields', field)
        self.service.organization_fields().delete(ids='1,2,3')
        self.expect('DELETE', '/organizationFields', {'ids': '1,2,3'})

        self.service.organization_field(1).get()
        self.expect('GET', '/organizationFields/1')
        self.service.organization_field(1).delete()
        self.expect('DELETE', '/organizationFields/1')

    def test_organizations(self):
        paging = {'start': 100, 'limit': 50}
        o = {'title': 'My cool Brown'}

        self.service.organizations().get(start=100, limit=50)
        self.expect('GET', '/organizations', paging)
        self.service.organizations().create(o)
        self.expect('POST', '/organizations', o)
        self.service.organizations().find('brown')
        self.expect('GET', '/organizations/find', {'term': 'brown'})
        self.service.organizations().delete(ids='1,2,3')
        self.expect('DELETE', '/organizations', {'ids': '1,2,3'})

        self.service.organization(1).get()
        self.expect('GET', '/organizations/1')
        self.service.organization(1).merge(4)
        self.expect('POST', '/organizations/1/merge', {'merge_with_id': 4})
        self.service.organization(1).update(o)
        self.expect('PUT', '/organizations/1', o)
        self.service.organization(1).followers()
        self.expect('GET', '/organizations/1/followers')
        self.service.organization(1).activities(start=100, limit=50)
        self.expect('GET', '/organizations/1/activities', paging)
        self.service.organization(1).updates(start=100, limit=50)
        self.expect('GET', '/organizations/1/updates', paging)
        self.service.organization(1).files(start=100, limit=50)
        self.expect('GET', '/organizations/1/files', paging)
        self.service.organization(1).persons(start=100, limit=50)
        self.expect('GET', '/organizations/1/persons', paging)
        self.service.organization(1).deals(start=100, limit=50)
        self.expect('GET', '/organizations/1/deals', paging)

    def test_person_fields(self):
        with port.assertRaises(MethodNotSupported):
            self.service.person_field(4).update()

        field = {'name': 'test'}

        self.service.person_fields().get()
        self.expect('GET', '/personFields')
        self.service.person_fields().create(field)
        self.expect('POST', '/personFields', field)
        self.service.person_fields().delete(ids='1,2,3')
        self.expect('DELETE', '/personFields', {'ids': '1,2,3'})

        self.service.person_field(1).get()
        self.expect('GET', '/personFields/1')
        self.service.person_field(1).delete()
        self.expect('DELETE', '/personFields/1')

    def test_persons(self):
        paging = {'start': 100, 'limit': 50}
        p = {'name': 'Mr Brown'}

        self.service.persons().get(start=100, limit=50)
        self.expect('GET', '/persons', paging)
        self.service.persons().create(p)
        self.expect('POST', '/persons', p)
        self.service.persons().find('brown')
        self.expect('GET', '/persons/find', {'term': 'brown'})
        self.service.persons().delete(ids='1,2,3')
        self.expect('DELETE', '/persons', {'ids': '1,2,3'})

        self.service.person(1).get()
        self.expect('GET', '/persons/1')
        self.service.person(1).merge(4)
        self.expect('POST', '/persons/1/merge', {'merge_with_id': 4})
        self.service.person(1).update(p)
        self.expect('PUT', '/persons/1', p)
        self.service.person(1).followers()
        self.expect('GET', '/persons/1/followers')
        self.service.person(1).products()
        self.expect('GET', '/persons/1/products')
        self.service.person(1).activities(start=100, limit=50)
        self.expect('GET', '/persons/1/activities', paging)
        self.service.person(1).updates(start=100, limit=50)
        self.expect('GET', '/persons/1/updates', paging)
        self.service.person(1).files(start=100, limit=50)
        self.expect('GET', '/persons/1/files', paging)
        self.service.person(1).deals(start=100, limit=50)
        self.expect('GET', '/persons/1/deals', paging)

    def test_stages(self):
        paging = {'start': 100, 'limit': 50}
        s = {'name': 'test', 'pipeline_id': 1}

        self.service.stages().get()
        self.expect('GET', '/stages')
        self.service.stages().create(s)
        self.expect('POST', '/stages', s)
        self.service.stages().delete(ids='1,2,3')
        self.expect('DELETE', '/stages', {'ids': '1,2,3'})

        self.service.stage(1).get()
        self.expect('GET', '/stages/1')
        self.service.stage(1).update(s)
        self.expect('PUT', '/stages/1', s)
        self.service.stage(1).deals(start=100, limit=50)
        self.expect('GET', '/stages/1/deals', paging)

    def test_pipelines(self):
        paging = {'start': 100, 'limit': 50}
        p = {'name': 'test'}

        self.service.pipelines().get()
        self.expect('GET', '/pipelines')
        self.service.pipelines().create(p)
        self.expect('POST', '/pipelines', p)

        self.service.pipeline(1).get()
        self.expect('GET', '/pipelines/1')
        self.service.pipeline(1).update(p)
        self.expect('PUT', '/pipelines/1', p)
        self.service.pipeline(1).deals(start=100, limit=50)
        self.expect('GET', '/pipelines/1/deals', paging)
        self.service.pipeline(1).conversion_rates('2012-01-01', '2012-02-02')
        self.expect('GET', '/pipelines/1/conversion_statistics',
                    {'start_date': '2012-01-01', 'end_date': '2012-02-02'})
        self.service.pipeline(1).movements('2012-01-01', '2012-02-02')
        self.expect('GET', '/pipelines/1/movement_statistics',
                    {'start_date': '2012-01-01', 'end_date': '2012-02-02'})

    def test_product_fields(self):
        with port.assertRaises(MethodNotSupported):
            self.service.product_field(4).update()

        field = {'name': 'test'}

        self.service.product_fields().get()
        self.expect('GET', '/productFields')
        self.service.product_fields().create(field)
        self.expect('POST', '/productFields', field)
        self.service.product_fields().delete(ids='1,2,3')
        self.expect('DELETE', '/productFields', {'ids': '1,2,3'})

        self.service.product_field(1).get()
        self.expect('GET', '/productFields/1')
        self.service.product_field(1).delete()
        self.expect('DELETE', '/productFields/1')

    def test_products(self):
        paging = {'start': 100, 'limit': 50}
        p = {'name': 'Blat'}

        self.service.products().get(start=100, limit=50)
        self.expect('GET', '/products', paging)
        self.service.products().create(p)
        self.expect('POST', '/products', p)
        self.service.products().find('brown')
        self.expect('GET', '/products/find', {'term': 'brown'})

        self.service.product(1).get()
        self.expect('GET', '/products/1')
        self.service.product(1).delete()
        self.expect('DELETE', '/products/1')
        self.service.product(1).update(p)
        self.expect('PUT', '/products/1', p)
        self.service.product(1).deals(start=100, limit=50)
        self.expect('GET', '/products/1/deals', paging)

    def test_search(self):
        self.service.search('brown')
        self.expect('GET', '/searchResults', {'term': 'brown'})

    def test_settings(self):
        self.service.settings()
        self.expect('GET', '/userSettings')

    def test_goals(self):
        g = {'goal_type': 'stage'}

        self.service.goals().get()
        self.expect('GET', '/goals')
        self.service.goals().create(g)
        self.expect('POST', '/goals', g)

        self.service.goal(1).get()
        self.expect('GET', '/goals/1')
        self.service.goal(1).delete()
        self.expect('DELETE', '/goals/1')
        self.service.goal(1).update(g)
        self.expect('PUT', '/goals/1', g)
        self.service.goal(1).results(period_start='2013-01-01',
                                     period_end='2013-02-02')
        self.expect('GET', '/goals/1/results',
                    {'period_start': '2013-01-01',
                     'period_end': '2013-02-02'})
