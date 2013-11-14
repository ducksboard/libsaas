import unittest

from libsaas.executors import test_executor
from libsaas.services import flurry


class FlurryTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = flurry.Flurry('my-api-access-code')

    def expect(self, uri, params={}):
        self.assertEqual('GET', self.executor.request.method)

        self.assertEqual(self.executor.request.uri,
                         'http://api.flurry.com' + uri)

        params.update({'apiAccessCode': 'my-api-access-code'})

        if params:
            self.assertEqual(self.executor.request.params, params)

    def test_applications(self):
        self.service.applications().get()
        self.expect('/appInfo/getAllApplications')

    def test_application(self):
        self.service.application('my-api-key').get()
        self.expect('/appInfo/getApplication', {
            'apiKey': 'my-api-key'
        })

        (self.service.application('my-api-key')
                     .events().get('start_date', 'end_date'))
        self.expect('/eventMetrics/Summary', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date'
        })

        (self.service.application('my-api-key')
                     .event('event_name').get('start_date', 'end_date'))
        self.expect('/eventMetrics/Event', {
            'apiKey': 'my-api-key',
            'eventName': 'event_name',
            'startDate': 'start_date',
            'endDate': 'end_date'
        })

        (self.service.application('my-api-key').metrics()
                     .active_users('start_date', 'end_date'))
        self.expect('/appMetrics/ActiveUsers', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date'
        })
        (self.service.application('my-api-key').metrics()
                     .active_users_by_week('start_date', 'end_date'))
        self.expect('/appMetrics/ActiveUsersByWeek', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date'
        })
        (self.service.application('my-api-key').metrics()
                     .active_users_by_month('start_date', 'end_date'))
        self.expect('/appMetrics/ActiveUsersByMonth', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date'
        })
        (self.service.application('my-api-key').metrics()
                     .new_users('start_date', 'end_date', group_by='WEEKS'))
        self.expect('/appMetrics/NewUsers', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date',
            'groupBy': 'WEEKS'
        })
        (self.service.application('my-api-key').metrics()
                     .median_session_length('start_date', 'end_date'))
        self.expect('/appMetrics/MedianSessionLength', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date'
        })
        (self.service.application('my-api-key').metrics()
                     .avg_session_length('start_date', 'end_date'))
        self.expect('/appMetrics/AvgSessionLength', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date',
        })
        (self.service.application('my-api-key').metrics()
                     .sessions('start_date', 'end_date'))
        self.expect('/appMetrics/Sessions', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date'
        })
        (self.service.application('my-api-key').metrics()
                     .page_views('start_date', 'end_date', version_name='v1'))
        self.expect('/appMetrics/PageViews', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date',
            'versionName': 'v1'
        })
        (self.service.application('my-api-key').metrics()
                     .avg_page_views_per_session('start_date', 'end_date'))
        self.expect('/appMetrics/AvgPageViewsPerSession', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date'
        })
        (self.service.application('my-api-key').metrics()
                     .retained_users('start_date', 'end_date', 'US'))
        self.expect('/appMetrics/RetainedUsers', {
            'apiKey': 'my-api-key',
            'startDate': 'start_date',
            'endDate': 'end_date',
            'country': 'US'
        })
