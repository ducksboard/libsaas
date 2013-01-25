from libsaas import http, parsers
from libsaas.services import base

from .resource import BasecampResource


class AccessResource(BasecampResource):
    path = 'accesses'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Accesses(AccessResource):

    @base.apimethod
    def grant(self, obj):
        """
        Create a new resource.

        :var obj: a Python object representing the resource to be created,
            usually in the same format as returned from `get`. Refer to the
            upstream documentation for details.
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_empty


class Access(AccessResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def revoke(self):
        """
        Delete this resource.
        """
        self.require_item()
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_empty
