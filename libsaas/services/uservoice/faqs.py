from libsaas.services import base

from . import resource, flags


class Faq(resource.UserVoiceResource):

    path = 'faqs'

    def create(self, obj):
        raise base.MethodNotSupported()

    def get(self):
        raise base.MethodNotSupported()

    @base.resource(flags.FaqFlags)
    def flags(self):
        """
        Return the resource corresponding to all the flags of this FAQ.
        """
        return flags.FaqFlags(self)
