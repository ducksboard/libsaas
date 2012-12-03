from . import resource

from libsaas import http, parsers
from libsaas.services import base


class FlagsBase(resource.UserVoiceResource):

    path = 'flags'

    def wrap_object(self, obj):
        return {'code': obj}

    @base.apimethod
    def create(self, flag):
        """
        Create a new flag.

        :var flag: The flag name. Refer to the upstream documentation for
            details.
        :vartype flag: str
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object(flag))

        return request, parsers.parse_json

    def update(self, obj):
        raise base.MethodNotSupported()


class SuggestionCommentFlags(FlagsBase):
    pass


class SuggestionFlags(FlagsBase):
    pass


class FaqFlags(FlagsBase):
    pass
