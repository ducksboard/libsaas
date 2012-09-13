import unittest

from datetime import date

from libsaas import http, xml
from libsaas.executors import test_executor
from libsaas.services import recurly


class RecurlyTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(
            b'<?xml version="1.0" encoding="UTF-8"?><root/>', 200, {})
        self.service = recurly.Recurly('my-token')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://api.recurly.com/v2' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_accounts(self):
        self.service.accounts().get(per_page=3)
        self.expect('GET', '/accounts', {'state': 'active', 'per_page': 3})

        self.service.accounts().get(state='closed')
        self.expect('GET', '/accounts', {'state': 'closed'})

        self.service.account(3).get()
        self.expect('GET', '/accounts/3')

        self.service.account(3).adjustments().get()
        self.expect('GET', '/accounts/3/adjustments')

        self.service.account(3).adjustments().get(state='pending')
        self.expect('GET', '/accounts/3/adjustments', {'state': 'pending'})

        self.service.account(3).adjustments().get(type='credit')
        self.expect('GET', '/accounts/3/adjustments', {'type': 'credit'})

        self.service.account(3).invoices().get()
        self.expect('GET', '/accounts/3/invoices')

        self.service.account(3).invoices().get(per_page=23)
        self.expect('GET', '/accounts/3/invoices', {'per_page': 23})

        self.service.account(3).subscriptions().get()
        self.expect('GET', '/accounts/3/subscriptions')

        self.service.account(3).subscriptions().get(per_page=23)
        self.expect('GET', '/accounts/3/subscriptions', {'per_page': 23})

        self.service.account(3).billing_info().get()
        self.expect('GET', '/accounts/3/billing_info')

        self.service.account(3).redemption().get()
        self.expect('GET', '/accounts/3/redemption')

        self.service.accounts().create({'account': {'account_code': 'x'}})
        self.expect('POST', '/accounts',
                    xml.dict_to_xml({'account': {'account_code': 'x'}}))

        self.service.account(23).update({'account': {'username': 'x'}})
        self.expect('PUT', '/accounts/23',
                    xml.dict_to_xml({'account': {'username': 'x'}}))

        self.service.account(23).adjustments().create({
            'adjustment': {'x': 'x'}
        })
        self.expect('POST', '/accounts/23/adjustments',
                    xml.dict_to_xml({'adjustment': {'x': 'x'}}))

        self.service.account(23).invoices().create({
            'invoice': {'line_items': [{
                'adjustment': {'x': 'a'}}, {'adjustment': {'x': 'b'}
            }]
        }})
        self.expect('POST', '/accounts/23/invoices',
            xml.dict_to_xml({
                'invoice': {'line_items': [{
                    'adjustment': {'x': 'a'}}, {'adjustment': {'x': 'b'}}
                ]}
        }))

        self.service.account(23).billing_info().update({
            'billing_info': {'x': 'x'}
        })
        self.expect('PUT', '/accounts/23/billing_info',
                    xml.dict_to_xml({'billing_info': {'x': 'x'}}))

        self.service.account(23).billing_info().delete()
        self.expect('DELETE', '/accounts/23/billing_info')

        self.service.account(23).redemption().create({
            'redemption': {'coupon_code': 'x'}
        })
        self.expect('POST', '/accounts/23/redemption',
                    xml.dict_to_xml({'redemption': {'coupon_code': 'x'}}))

        self.service.account(23).redemption().delete()
        self.expect('DELETE', '/accounts/23/redemption')

        self.service.account(23).delete()
        self.expect('DELETE', '/accounts/23')

    def test_adjustments(self):
        self.service.adjustment('uuid').get()
        self.expect('GET', '/adjustments/uuid')

        self.service.adjustment('uuid').delete()
        self.expect('DELETE', '/adjustments/uuid')

    def test_coupons(self):
        self.service.coupons().get(per_page=3)
        self.expect('GET', '/coupons', {'per_page': 3})

        self.service.coupons().get(state='expired')
        self.expect('GET', '/coupons', {'state': 'expired'})

        self.service.coupon('discount').get()
        self.expect('GET', '/coupons/discount')

        self.service.coupons().create({'coupon': {'coupon_code': 'x'}})
        self.expect('POST', '/coupons',
                    xml.dict_to_xml({'coupon': {'coupon_code': 'x'}}))

        self.service.coupon('discount').delete()
        self.expect('DELETE', '/coupons/discount')

    def test_invoices(self):
        self.service.invoices().get(per_page=3)
        self.expect('GET', '/invoices', {'per_page': 3})

        self.service.invoices().get(state='open')
        self.expect('GET', '/invoices', {'state': 'open'})

        self.service.invoice('1980').get()
        self.expect('GET', '/invoices/1980')

        self.service.invoice('1980').mark_successful()
        self.expect('PUT', '/invoices/1980/mark_successful')

        self.service.invoice('1980').mark_failed()
        self.expect('PUT', '/invoices/1980/mark_failed')

    def test_plans(self):
        self.service.plans().get(per_page=3)
        self.expect('GET', '/plans', {'per_page': 3})

        self.service.plan('basic').get()
        self.expect('GET', '/plans/basic')

        self.service.plans().create({'plan': {'x': 'x'}})
        self.expect('POST', '/plans', xml.dict_to_xml({'plan': {'x': 'x'}}))

        self.service.plan('basic').update({'plan': {'x': 'x'}})
        self.expect('PUT', '/plans/basic',
                    xml.dict_to_xml({'plan': {'x': 'x'}}))

        self.service.plan('basic').delete()
        self.expect('DELETE', '/plans/basic')

        self.service.plan('basic').addons().get(per_page=3)
        self.expect('GET', '/plans/basic/add_ons', {'per_page': 3})

        self.service.plan('basic').addon('item').get()
        self.expect('GET', '/plans/basic/add_ons/item')

        self.service.plan('basic').addons().create({'add_on': {'x': 'x'}})
        self.expect('POST', '/plans/basic/add_ons',
                    xml.dict_to_xml({'add_on': {'x': 'x'}}))

        self.service.plan('basic').addon('item').update({'add_on': {'x': 'x'}})
        self.expect('PUT', '/plans/basic/add_ons/item',
                    xml.dict_to_xml({'add_on': {'x': 'x'}}))

        self.service.plan('basic').addon('item').delete()
        self.expect('DELETE', '/plans/basic/add_ons/item')

    def test_subscriptions(self):
        self.service.subscriptions().get()
        self.expect('GET', '/subscriptions', {'state': 'live'})

        self.service.subscriptions().get(state='future')
        self.expect('GET', '/subscriptions', {'state': 'future'})

        self.service.subscriptions().get(per_page=23)
        self.expect('GET', '/subscriptions', {'state': 'live', 'per_page': 23})

        self.service.subscriptions().create({'subscription': {'x': 'x'}})
        self.expect('POST', '/subscriptions',
                    xml.dict_to_xml({'subscription': {'x': 'x'}}))

        self.service.subscription('uuid').get()
        self.expect('GET', '/subscriptions/uuid')

        self.service.subscription('uuid').update({'subscription': {'x': 'x'}})
        self.expect('PUT', '/subscriptions/uuid',
                    xml.dict_to_xml({'subscription': {'x': 'x'}}))

        self.service.subscription('uuid').cancel()
        self.expect('PUT', '/subscriptions/uuid/cancel')

        self.service.subscription('uuid').reactivate()
        self.expect('PUT', '/subscriptions/uuid/reactivate')

        self.service.subscription('uuid').terminate()
        self.expect('PUT', '/subscriptions/uuid/terminate?refund=none')

        self.service.subscription('uuid').terminate(refund='partial')
        self.expect('PUT', '/subscriptions/uuid/terminate?refund=partial')

        today = '{0}'.format(date.today())
        self.service.subscription('uuid').postpone(today)
        self.expect('PUT', ('/subscriptions/uuid/postpone?'
                            'next_renewal_date={0}').format(today))

    def test_transactions(self):
        self.service.transactions().get()
        self.expect('GET', '/transactions')

        self.service.transactions().get(state='failed')
        self.expect('GET', '/transactions', {'state': 'failed'})

        self.service.transactions().get(per_page=23)
        self.expect('GET', '/transactions', {'per_page': 23})

        self.service.transactions().get(type='refund', per_page=23)
        self.expect('GET', '/transactions', {'type': 'refund', 'per_page': 23})

        self.service.transactions().create({'transaction': {'x': 'x'}})
        self.expect('POST', '/transactions',
                    xml.dict_to_xml({'transaction': {'x': 'x'}}))

        self.service.transaction('uuid').get()
        self.expect('GET', '/transactions/uuid')

        self.service.transaction('uuid').refund()
        self.expect('DELETE', '/transactions/uuid')

        self.service.transaction('uuid').refund(amount_in_cents=1000)
        self.expect('DELETE', '/transactions/uuid?amount_in_cents=1000')

    def test_count(self):
        self.executor.set_response(
            b'<?xml version="1.0" encoding="UTF-8"?><root/>', 200,
            {'x-records': '10'})
        res = self.service.accounts().count(state='active')
        self.expect('GET', '/accounts', {'state': 'active', 'per_page': 1})
        self.assertEqual(res, 10)

        # no X-Records header, the count should come default to 1
        self.executor.set_response(
            b'<?xml version="1.0" encoding="UTF-8"?><root/>', 200, {})
        res = self.service.accounts().count(state='active')
        self.assertEqual(res, 1)

        # no 2xx response, there should be an exception
        self.executor.set_response(b'boom', 500, {})
        self.assertRaises(http.HTTPError,
                          self.service.accounts().count)
