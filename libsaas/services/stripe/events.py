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
    def get(self, type=None, limit=None, ending_before=None,
            starting_after=None):
        """
        Fetch all of the objects.

        :var type: A string containing a specific event name, or group of
            events using * as a wildcard. The list will be filtered to
            include only events with a matching event property.
        :vartype type: str

        :var limit: A limit on the number of objects to be returned.
            Count can range between 1 and 100 objects.
        :vartype count: int

        :var ending_before: A cursor (object ID) for use in pagination. Fetched
            objetcs will be newer than the given object.
        :vartype ending_before: str

        :var starting_after: A cursor (object ID) for use in pagination.
            Fetched objetcs will be older than the given object.
        :vartype starting_after: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
