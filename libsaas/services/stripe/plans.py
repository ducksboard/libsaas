from libsaas.services import base

from . import resource


class PlansBaseResource(resource.StripeResource):

    path = 'plans'


class Plan(PlansBaseResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Plans(resource.ListResourceMixin, PlansBaseResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
