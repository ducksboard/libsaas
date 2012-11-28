from libsaas.services import base

from . import resource


class Actions(resource.PaginatedDeskResource):

    path = 'actions'


class Action(resource.DeskResource):

    path = 'actions'


class Macros(resource.PaginatedDeskResource):

    path = 'macros'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Macro(base.RESTResource):

    path = 'macros'

    @base.resource(Actions)
    def actions(self):
        """
        Return the resource corresponding to macro actions
        """
        return Actions(self)

    @base.resource(Actions)
    def action(self, action_id):
        """
        Return the resource corresponding to single macro action
        """
        return Action(self, action_id)
