from libsaas.services import base

from . import resource


class BalanceHistory(resource.ListResourceMixin, resource.StripeResource):

    path = 'balance/history'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
