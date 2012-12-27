from libsaas import http, parsers
from libsaas.services import base


class GoogleCalendarResource(base.RESTResource):

    @base.apimethod
    def patch(self, obj):
        """
        Update this resource's metadata.

        :var obj: a Python object representing the updated resource.
            Refer to the upstream documentation for details.
        """
        self.require_item()
        request = http.Request('PATCH', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json


class ReadonlyResource(base.RESTResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def patch(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ColorsResource(ReadonlyResource):
    path = 'colors'


class FreeBusyResource(ReadonlyResource):
    path = 'freeBusy'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def query(self, obj):
        """
        Return free/busy info for a set of calendars.

        :var obj: a Python object representing the query.
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json
