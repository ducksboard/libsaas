from . import resource


class GadgetsBase(resource.UserVoiceResource):

    path = 'gadgets'

    def wrap_object(self, obj):
        return {'gadget': obj}


class Gadgets(GadgetsBase):
    pass


class Gadget(GadgetsBase):
    pass
