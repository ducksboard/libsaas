from libsaas import http, parsers
from libsaas.services import base

from . import resource


class CouponsBase(resource.RecurlyResource):

    path = 'coupons'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Coupons(CouponsBase):

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, state=None, cursor=None, per_page=None):
        """
        Fetch all your coupons.

        :var state: The state of coupons to return: "redeemable", "expired"
            or "maxed_out".
        :vartype state: str
        """
        params = base.get_params(('state', 'cursor', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_xml


class Coupon(CouponsBase):

    pass


class CouponRedemption(CouponsBase):

    path = 'redemption'

    @base.apimethod
    def delete(self):
        """
        Delete this resource.
        """
        request = http.Request('DELETE', self.get_url())
        return request, parsers.parse_empty
