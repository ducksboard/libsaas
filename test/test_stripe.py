import unittest

from libsaas.services import stripe
from libsaas.executors import test_executor
from libsaas.services.base import MethodNotSupported


class StripeTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = stripe.Stripe('my-api-key')

    def expect(self, method=None, uri=None, params={}, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://api.stripe.com/v1' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)

        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_account(self):
        with self.assertRaises(MethodNotSupported):
            self.service.account().create()
            self.service.account().update()
            self.service.account().delete()

        self.service.account().get()
        self.expect('GET', '/account', {})

    def test_plans(self):
        with self.assertRaises(MethodNotSupported):
            self.service.plans().update()
            self.service.plans().delete()

        self.service.plans().get()
        self.expect('GET', '/plans', {})
        self.service.plans().get(count=23)
        self.expect('GET', '/plans', {'count': 23})

        self.service.plans().create({'key':'value'})
        self.expect('POST', '/plans', {'key': 'value'})

        with self.assertRaises(MethodNotSupported):
            self.service.plan('123').create()

        self.service.plan('123').get()
        self.expect('GET', '/plans/123', {})

        self.service.plan('123').update({'key':'value'})
        self.expect('POST', '/plans/123', {'key': 'value'})

        self.service.plan('123').delete()
        self.expect('DELETE', '/plans/123', {})

    def test_charges(self):
        with self.assertRaises(MethodNotSupported):
            self.service.charges().update()
            self.service.charges().delete()

        self.service.charges().get()
        self.expect('GET', '/charges', {})
        self.service.charges().get(customer='123', count=23)
        self.expect('GET', '/charges', {'count': 23, 'customer': '123'})

        self.service.charges().create({'key':'value'})
        self.expect('POST', '/charges', {'key': 'value'})

        with self.assertRaises(MethodNotSupported):
            self.service.charge('123').create()
            self.service.charge('123').update()
            self.service.charge('123').delete()

        self.service.charge('123').get()
        self.expect('GET', '/charges/123', {})

        self.service.charge('123').dispute({})
        self.expect('POST', '/charges/123/dispute', {})

        self.service.charge('123').refund()
        self.expect('POST', '/charges/123/refund', {})
        self.service.charge('123').refund(amount=23)
        self.expect('POST', '/charges/123/refund', {'amount': 23})

    def test_customers(self):
        with self.assertRaises(MethodNotSupported):
            self.service.customers().update()
            self.service.customers().delete()

        self.service.customers().get()
        self.expect('GET', '/customers', {})
        self.service.customers().get(count=23, offset=1)
        self.expect('GET', '/customers', {'count': 23, 'offset': 1})

        self.service.customers().create({'key':'value'})
        self.expect('POST', '/customers', {'key': 'value'})

        with self.assertRaises(MethodNotSupported):
            self.service.customer('123').create()
            self.service.customer('123').subscription().create()
            self.service.customer('123').discount().get()
            self.service.customer('123').discount().create()
            self.service.customer('123').discount().update()

        self.service.customer('123').get()
        self.expect('GET', '/customers/123', {})

        self.service.customer('123').update({'key':'value'})
        self.expect('POST', '/customers/123', {'key': 'value'})

        self.service.customer('123').delete()
        self.expect('DELETE', '/customers/123', {})

        self.service.customer('123').subscription().get()
        self.expect('GET', '/customers/123/subscription', {})

        self.service.customer('123').subscription().update({'key': 'value'})
        self.expect('POST', '/customers/123/subscription', {'key': 'value'})

        self.service.customer('123').subscription().delete()
        self.expect('DELETE', '/customers/123/subscription', {})

        self.service.customer('123').discount().delete()
        self.expect('DELETE', '/customers/123/discount', {})

    def test_tokens(self):
        with self.assertRaises(MethodNotSupported):
            self.service.tokens().get()
            self.service.tokens().update()
            self.service.tokens().delete()

        self.service.tokens().create({'key':'value'})
        self.expect('POST', '/tokens', {'key': 'value'})

        with self.assertRaises(MethodNotSupported):
            self.service.token('123').create()
            self.service.token('123').update()
            self.service.token('123').delete()

        self.service.token('123').get()
        self.expect('GET', '/tokens/123', {})

    def test_invoices(self):
        with self.assertRaises(MethodNotSupported):
            self.service.invoices().update()
            self.service.invoices().delete()

        self.service.invoices().get()
        self.expect('GET', '/invoices', {})
        self.service.invoices().get(customer=23)
        self.expect('GET', '/invoices', {'customer': 23})

        self.service.invoices().upcoming('123')
        self.expect('GET', '/invoices/upcoming', {'customer': '123'})

        self.service.invoices().create({'key':'value'})
        self.expect('POST', '/invoices', {'key': 'value'})

        with self.assertRaises(MethodNotSupported):
            self.service.invoice('123').create()
            self.service.invoice('123').delete()

        self.service.invoice('123').get()
        self.expect('GET', '/invoices/123', {})

        self.service.invoice('123').update({'key':'value'})
        self.expect('POST', '/invoices/123', {'key': 'value'})

        self.service.invoice('123').pay()
        self.expect('POST', '/invoices/123/pay', {})

        with self.assertRaises(MethodNotSupported):
            self.service.invoice('123').lines().create()
            self.service.invoice('123').lines().update()
            self.service.invoice('123').lines().delete()

        self.service.invoice('123').lines().get()
        self.expect('GET', '/invoices/123/lines', {})
        self.service.invoice('123').lines().get(offset=1)
        self.expect('GET', '/invoices/123/lines', {'offset': 1})

    def test_events(self):
        with self.assertRaises(MethodNotSupported):
            self.service.events().create()
            self.service.events().update()
            self.service.events().delete()

        self.service.events().get()
        self.expect('GET', '/events', {})
        self.service.events().get(type='type')
        self.expect('GET', '/events', {'type': 'type'})

        with self.assertRaises(MethodNotSupported):
            self.service.event('123').create()
            self.service.event('123').update()
            self.service.event('123').delete()

        self.service.event('123').get()
        self.expect('GET', '/events/123', {})

    def test_coupons(self):
        with self.assertRaises(MethodNotSupported):
            self.service.coupons().update()
            self.service.coupons().delete()

        self.service.coupons().get()
        self.expect('GET', '/coupons', {})
        self.service.coupons().get(count=23)
        self.expect('GET', '/coupons', {'count': 23})

        self.service.coupons().create({'key':'value'})
        self.expect('POST', '/coupons', {'key': 'value'})

        with self.assertRaises(MethodNotSupported):
            self.service.coupon('123').create()
            self.service.coupon('123').update()

        self.service.coupon('123').get()
        self.expect('GET', '/coupons/123', {})

        self.service.coupon('123').delete()
        self.expect('DELETE', '/coupons/123', {})

    def test_invoiceitems(self):
        with self.assertRaises(MethodNotSupported):
            self.service.invoiceitems().update()
            self.service.invoiceitems().delete()

        self.service.invoiceitems().get()
        self.expect('GET', '/invoiceitems', {})
        self.service.invoiceitems().get(count=23)
        self.expect('GET', '/invoiceitems', {'count': 23})

        self.service.invoiceitems().create({'key':'value'})
        self.expect('POST', '/invoiceitems', {'key': 'value'})

        with self.assertRaises(MethodNotSupported):
            self.service.invoiceitem('123').create()
            self.service.invoiceitem('123').update()

        self.service.invoiceitem('123').get()
        self.expect('GET', '/invoiceitems/123', {})

        self.service.invoiceitem('123').delete()
        self.expect('DELETE', '/invoiceitems/123', {})

