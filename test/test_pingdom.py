import unittest

from libsaas.executors import test_executor
from libsaas.services import base, pingdom


class PingdomTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = pingdom.Pingdom('username', 'password', 'key')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method is not None:
            self.assertEqual(method, self.executor.request.method)
        if uri is not None:
            self.assertEqual(self.executor.request.uri,
                             'https://api.pingdom.com/api/2.0' + uri)
        if params is not None:
            self.assertEqual(self.executor.request.params, params)
        if headers is not None:
            self.assertEqual(self.executor.request.headers, headers)

    def test_actions(self):
        paging = {'limit': 100, 'offset': 50}
        self.service.actions().get()
        self.expect('GET', '/actions')

        self.service.actions().get(limit=100, offset=50)
        self.expect('GET', '/actions', paging)

        with self.assertRaises(base.MethodNotSupported):
            self.service.actions().create()
            self.service.actions().update()
            self.service.actions().delete()

    def test_analysis(self):
        paging = {'limit': 100, 'offset': 50}
        self.service.analysis(4).get()
        self.expect('GET', '/analysis/4')

        self.service.analysis(4).get(limit=100, offset=50)
        self.expect('GET', '/analysis/4', paging)

        self.service.analysis(4).get_raw_analysis(10)
        self.expect('GET', '/analysis/4/10')

        self.service.check(4).analysis().get(limit=100, offset=50)
        self.expect('GET', '/analysis/4', paging)

        self.service.check(4).analysis().get_raw_analysis(10)
        self.expect('GET', '/analysis/4/10')

        with self.assertRaises(base.MethodNotSupported):
            self.service.analysis(4).create()
            self.service.analysis(4).update()
            self.service.analysis(4).delete()

    def test_contacts(self):
        obj = {'name': 'Super cool contact'}
        paging = {'limit': 100, 'offset': 50}

        self.service.contacts().get(offset=50, limit=100)
        self.expect('GET', '/contacts', paging)

        self.service.contact(4).update(obj)
        self.expect('PUT', '/contacts/4', obj)

        self.service.contact(4).delete()
        self.expect('DELETE', '/contacts/4')

        self.service.contacts().create(obj)
        self.expect('POST', '/contacts', obj)

        pause = {'paused': True, 'contactids': '1,2'}
        self.service.contacts().update(pause)
        self.expect('PUT', '/contacts', pause)

        delcontacts = {'delcontactids': '1,2'}
        self.service.contacts().update(delcontacts)
        self.expect('PUT', '/contacts', delcontacts)

        with self.assertRaises(base.MethodNotSupported):
            self.service.contact(4).get()

    def test_credits(self):
        self.service.credits().get()
        self.expect('GET', '/credits')

        with self.assertRaises(base.MethodNotSupported):
            self.service.credits().create()
            self.service.credits().update()
            self.service.credits().delete()

    def test_probes(self):
        paging = {'limit': 100, 'offset': 50}
        self.service.probes().get()
        self.expect('GET', '/probes')

        self.service.probes().get(limit=100, offset=50)
        self.expect('GET', '/probes', paging)

        with self.assertRaises(base.MethodNotSupported):
            self.service.probes().create()
            self.service.probes().update()
            self.service.probes().delete()

    def test_reference(self):
        self.service.reference().get()
        self.expect('GET', '/reference')

        with self.assertRaises(base.MethodNotSupported):
            self.service.reference().create()
            self.service.reference().update()
            self.service.reference().delete()

    def test_reports_email(self):
        obj = {'name': 'Super cool report'}

        self.service.reports_email().get()
        self.expect('GET', '/reports.email')

        self.service.report_email(4).update(obj)
        self.expect('PUT', '/reports.email/4', obj)

        self.service.report_email(4).delete()
        self.expect('DELETE', '/reports.email/4')

        self.service.reports_email().create(obj)
        self.expect('POST', '/reports.email', obj)

        with self.assertRaises(base.MethodNotSupported):
            self.service.report_email(4).get()

    def test_reports_public(self):
        obj = {'name': 'Super cool report'}

        self.service.reports_public().get()
        self.expect('GET', '/reports.public')

        self.service.report_public(4).update(obj)
        self.expect('PUT', '/reports.public/4', obj)

        self.service.report_public(4).delete()
        self.expect('DELETE', '/reports.public/4')

        self.service.reports_public().create(obj)
        self.expect('POST', '/reports.public', obj)

        with self.assertRaises(base.MethodNotSupported):
            self.service.report_public(4).get()

    def test_reports_shared(self):
        obj = {'name': 'Super cool report'}

        self.service.reports_shared().get()
        self.expect('GET', '/reports.shared')

        self.service.report_shared(4).update(obj)
        self.expect('PUT', '/reports.shared/4', obj)

        self.service.report_shared(4).delete()
        self.expect('DELETE', '/reports.shared/4')

        self.service.reports_shared().create(obj)
        self.expect('POST', '/reports.shared', obj)

        with self.assertRaises(base.MethodNotSupported):
            self.service.report_shared(4).get()

    def test_results(self):
        paging = {'limit': 100, 'offset': 50}
        self.service.results(4).get()
        self.expect('GET', '/results/4')

        self.service.results(4).get(limit=100, offset=50)
        self.expect('GET', '/results/4', paging)

        self.service.check(4).results().get(limit=100, offset=50)
        self.expect('GET', '/results/4', paging)

        with self.assertRaises(base.MethodNotSupported):
            self.service.results(4).create()
            self.service.results(4).update()
            self.service.results(4).delete()

    def test_servertime(self):
        self.service.servertime().get()
        self.expect('GET', '/servertime')

        with self.assertRaises(base.MethodNotSupported):
            self.service.servertime().create()
            self.service.servertime().update()
            self.service.servertime().delete()

    def test_settings(self):
        self.service.settings().get()
        self.expect('GET', '/settings')

        obj = {'phone': '112231234'}
        self.service.settings().update(obj)
        self.expect('PUT', '/settings', obj)

        with self.assertRaises(base.MethodNotSupported):
            self.service.settings().create()
            self.service.settings().delete()

    def test_summary(self):
        params = {'from': 1}
        self.service.summary(4).average(from_=1)
        self.expect('GET', '/summary.average/4', params)

        self.service.check(4).summary().average(from_=1)
        self.expect('GET', '/summary.average/4', params)

        self.service.summary(4).outage(from_=1)
        self.expect('GET', '/summary.outage/4', params)

        self.service.check(4).summary().outage(from_=1)
        self.expect('GET', '/summary.outage/4', params)

        self.service.summary(4).hoursofday(from_=1)
        self.expect('GET', '/summary.hoursofday/4', params)

        self.service.check(4).summary().hoursofday(from_=1)
        self.expect('GET', '/summary.hoursofday/4', params)

        self.service.summary(4).performance(from_=1)
        self.expect('GET', '/summary.performance/4', params)

        self.service.check(4).summary().performance(from_=1)
        self.expect('GET', '/summary.performance/4', params)

        self.service.summary(4).probes(from_=1)
        self.expect('GET', '/summary.probes/4', params)

        self.service.check(4).summary().probes(from_=1)
        self.expect('GET', '/summary.probes/4', params)

    def test_single(self):
        p = {'host': 'ducksboard.com', 'probeid': 17, 'type': 'http'}
        self.service.single().get(**p)
        self.expect('GET', '/single', p)

        with self.assertRaises(base.MethodNotSupported):
            self.service.single().create()
            self.service.single().update()
            self.service.single().delete()

    def test_traceroute(self):
        p = {'host': 'ducksboard.com', 'probeid': 17}
        self.service.traceroute().get(**p)
        self.expect('GET', '/traceroute', p)

        with self.assertRaises(base.MethodNotSupported):
            self.service.traceroute().create()
            self.service.traceroute().update()
            self.service.traceroute().delete()
