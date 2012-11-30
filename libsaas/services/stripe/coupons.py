from libsaas.services import base

from . import resource


class CouponsBaseResource(resource.StripeResource):

    path = 'coupons'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Coupon(CouponsBaseResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Coupons(resource.ListResourceMixin, CouponsBaseResource):

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
