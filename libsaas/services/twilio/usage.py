from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource


class RecordsBase(resource.TwilioResource):

    path = 'Records'

    @base.apimethod
    def get(self, Category=None, StartDate=None, EndDate=None,
            Page=None, PageSize=None, AfterSid=None):
        """
        Fetch a list of usage records.

        :var Category: Only include usage records of this usage category.
        :vartype Category: str

        :var StartDate: Only include usage that has occurred on or after
            this date. Format is YYYY-MM-DD. All dates are in GMT.
            As a convenience, you can also specify offsets to today.
            For example, StartDate=-30days will make StartDate be 30 days
            before today.
        :vartype StartDate: str

        :var EndDate: Only include usage that has occurred on or before
            this date. Format is YYYY-MM-DD. All dates are in GMT.
            As a convenience, you can also specify offsets to today.
            For example, EndDate=+30days will make EndDate be 30 days
            from today.
        :vartype EndDate: str

        :var Page: The current page number. Zero-indexed, so the first page
            is 0.
        :vartype Page: int

        :var PageSize: How many resources to return in each list page.
            The default is 50, and the maximum is 1000.
        :vartype PageSize: int

        :var AfterSid: The last Sid returned in the previous page, used to
            avoid listing duplicated resources if new ones are created while
            paging.
        :vartype AfterSid: str
        """
        params = resource.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class RecordsDaily(RecordsBase):

    path = 'Daily'


class RecordsMonthly(RecordsBase):

    path = 'Monthly'


class RecordsYearly(RecordsBase):

    path = 'Yearly'


class RecordsAllTime(RecordsBase):

    path = 'AllTime'


class RecordsToday(RecordsBase):

    path = 'Today'


class RecordsYesterday(RecordsBase):

    path = 'Yesterday'


class RecordsThisMonth(RecordsBase):

    path = 'ThisMonth'


class RecordsLastMonth(RecordsBase):

    path = 'LastMonth'


class Records(RecordsBase):

    @base.resource(RecordsDaily)
    def daily(self):
        """
        Return multiple usage records for each usage category,
        each representing usage over a daily time-interval.
        """
        return RecordsDaily(self)

    @base.resource(RecordsMonthly)
    def monthly(self):
        """
        Return multiple usage records for each usage category,
        each representing usage over a monthly time-interval.
        """
        return RecordsMonthly(self)

    @base.resource(RecordsYearly)
    def yearly(self):
        """
        Return multiple usage records for each usage category,
        each representing usage over a yearly time-interval.
        """
        return RecordsYearly(self)

    @base.resource(RecordsAllTime)
    def all_time(self):
        """
        Return a single usage record for each usage category,
        each representing usage over the date-range specified.
        This is the same as the root .usage().records().
        """
        return RecordsAllTime(self)

    @base.resource(RecordsToday)
    def today(self):
        """
        Return a single usage record per usage category,
        for today's usage only.
        """
        return RecordsToday(self)

    @base.resource(RecordsYesterday)
    def yesterday(self):
        """
        Return a single usage record per usage category,
        for yesterday's usage only.
        """
        return RecordsYesterday(self)

    @base.resource(RecordsThisMonth)
    def this_month(self):
        """
        Return a single usage record per usage category,
        for this month's usage only.
        """
        return RecordsThisMonth(self)

    @base.resource(RecordsLastMonth)
    def last_month(self):
        """
        Return a single usage record per usage category,
        for last month's usage only.
        """
        return RecordsLastMonth(self)


class TriggersBase(resource.TwilioResource):

    path = 'Triggers'


class Trigger(TriggersBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Triggers(TriggersBase):

    @base.apimethod
    def get(self, Recurring=None, UsageCategory=None, TriggerBy=None,
            Page=None, PageSize=None, AfterSid=None):
        """
        Fetch a list of usage triggers resource representations.

        :var Recurring: Only show usage triggers that count over this interval.
            One of daily, monthly, or yearly. To retrieve non-recurring
            triggers, leave this empty or use alltime.
        :vartype Recurring: str

        :var UsageCategory: Only include usage triggers that watch this usage
            category.
        :vartype UsageCategory: str

        :var TriggerBy: Only show usage triggers that trigger by this field
            in the usage record. Must be one of: count, usage, or price.
        :vartype TriggerBy: str

        :var Page: The current page number. Zero-indexed, so the first page
            is 0.
        :vartype Page: int

        :var PageSize: How many resources to return in each list page.
            The default is 50, and the maximum is 1000.
        :vartype PageSize: int

        :var AfterSid: The last Sid returned in the previous page, used to
            avoid listing duplicated resources if new ones are created while
            paging.
        :vartype AfterSid: str
        """
        params = resource.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Usage(resource.TwilioResource):

    path = 'Usage'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(Records)
    def records(self):
        """
        Return a list of usage records.
        """
        return Records(self)

    @base.resource(Triggers)
    def triggers(self):
        """
        Return a list of usage triggers set on this account.
        """
        return Triggers(self)

    @base.resource(Trigger)
    def trigger(self, sid):
        """
        Return an usage trigger set on this account.
        """
        return Trigger(self, sid)
