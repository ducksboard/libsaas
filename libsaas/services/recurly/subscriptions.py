from libsaas import http, parsers
from libsaas.services import base

from . import resource


class SubscriptionsBase(resource.RecurlyResource):

    path = 'subscriptions'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Subscriptions(SubscriptionsBase):

    @base.apimethod
    def get(self, state='live', cursor=None, per_page=None):
        """
        Fetch all your subscription.

        :var state: The state of subscriptions to return:
            "active", "canceled", "expired", "future", "in_trial", "live",
            or "past_due". A subscription will belong to more than one state.
        :vartype state: str
        """
        params = base.get_params(('cursor', 'per_page'), locals())
        params['state'] = state
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_xml

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Subscription(SubscriptionsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def cancel(self):
        """
        Cancel a subscription, remaining it as active until next billing cycle.
        """
        self.require_item()

        url = '{0}/cancel'.format(self.get_url())
        request = http.Request('PUT', url)
        request.use_xml = False

        return request, parsers.parse_empty

    @base.apimethod
    def reactivate(self):
        """
        Reactivating a canceled subscription.
        """
        self.require_item()

        url = '{0}/reactivate'.format(self.get_url())
        request = http.Request('PUT', url)

        return request, parsers.parse_empty

    @base.apimethod
    def terminate(self, refund=None):
        """
        Terminate a subsciription, removing any stored billing information.

        :var refund: The type of the refund to perform: 'full' or 'partial'
            Defaults to 'none'.
        :vartype refund: str
        """
        self.require_item()

        url = '{0}/terminate'.format(self.get_url())
        params = {
            'refund': refund if refund else 'none'
        }
        url = url + '?' + http.urlencode_any(params)

        request = http.Request('PUT', url)

        return request, parsers.parse_empty

    @base.apimethod
    def postpone(self, next_renewal_date):
        """
        Postpone a subscription

        :var next_renewal_date: The next renewal date that will be applied
        :vartype next_renewal_date: str
        """
        self.require_item()

        url = '{0}/postpone'.format(self.get_url())
        params = {'next_renewal_date': next_renewal_date}
        url = url + '?' + http.urlencode_any(params)

        request = http.Request('PUT', url)

        return request, parsers.parse_empty


class AccountSubscriptions(SubscriptionsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()
