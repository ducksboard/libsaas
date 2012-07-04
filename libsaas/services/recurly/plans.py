from libsaas.services import base

from . import resource


class AddonsBase(resource.RecurlyResource):

    path = 'add_ons'


class Addons(AddonsBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Addon(AddonsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class PlansBase(resource.RecurlyResource):

    path = 'plans'


class Plans(PlansBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Plan(PlansBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(Addons)
    def addons(self):
        """
        Return the resource corresponding to all the add-ons for the plan.
        """
        return Addons(self)

    @base.resource(Addon)
    def addon(self, add_on_code):
        """
        Return the resource corresponding to a single plan's add-on.
        """
        return Addon(self, add_on_code)
