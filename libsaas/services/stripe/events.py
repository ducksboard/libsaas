from libsaas.services import base
from libsaas import parsers, http

from . import resource


class EventsBaseResource(resource.StripeResource):

    path = 'events'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Event(EventsBaseResource):
    pass


class Events(EventsBaseResource):

    @base.apimethod
    def get(self, type=None, count=None, offset=None):
        """
        Fetch all of the objects.

        :var type: A string containing a specific event name, or group of
            events using * as a wildcard. The list will be filtered to
            include only events with a matching event property.
        :vartype type: str
        :var count: A limit on the number of objects to be returned.
            Count can range between 1 and 100 objects.
        :vartype count: int

        :var offset: An offset into your object array. The API will return
            the requested number of objects starting at that offset.
        :vartype offset: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
