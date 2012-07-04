from libsaas import http, parsers
from libsaas.services import base

from . import resource


class AdjustmentsBase(resource.RecurlyResource):

    path = 'adjustments'


class AccountAdjustments(AdjustmentsBase):

    @base.apimethod
    def get(self, type=None, state=None, cursor=None, per_page=None):
        """
        Fetch credits and charges for an account.

        :var type: The type of adjustments: 'charge' or 'credit'.
        :vartype type: str

        :var state: The state of the adjustments to return: 'pending'
            or 'invoiced'.
        :vartype state: str
        """
        params = base.get_params(('type', 'state', 'cursor', 'per_page'),
                                 locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_xml

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Adjustment(AdjustmentsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()
