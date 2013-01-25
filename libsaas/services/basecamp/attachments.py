from libsaas import http, parsers
from libsaas.services import base

from .resource import BasecampResource

class AttachmentResource(BasecampResource):
    path = 'attachments'

    @base.apimethod
    def get(self, page=None):
        """
        Fetch all resources.

        :var page: the page that will be return.
            If not indicated, first one is returned.
        :vartype page: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class Attachments(AttachmentResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class GlobalAttachments(AttachmentResource):
    pass
