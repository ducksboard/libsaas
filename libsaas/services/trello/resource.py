from libsaas import http, parsers
from libsaas.services import base


def serialize_param(val):
    if isinstance(val, bool):
        return 'true' if val else 'false'
    elif isinstance(val, list):
        return ','.join(val)

    return val


class TrelloFieldMixin(object):

    @base.apimethod
    def field(self, field):
        """
        Returns a single resource field.

        :var field: a valid resource's field.
        :vartype field: str
        """
        url = '{0}/{1}'.format(self.get_url(), field)
        request = http.Request('GET', url)
        return request, parsers.parse_json

class TrelloFilterMixin(object):

    @base.apimethod
    def filter(self, filter_id):
        """
        Fetch a collection filtered.

        :var filter: a valid resource's filter.
        :vartype filter: str
        """
        self.require_collection()
        url = '{0}/{1}'.format(self.get_url(), filter_id)
        request = http.Request('GET', url)

        return request, parsers.parse_json


class TrelloResource(base.RESTResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, fields=None):
        """
        Fetch a single object.

        :var fields: all or comma-separated list of fields.
        :vartype fields: list
        """
        params = base.get_params(
            None, locals(), serialize_param=serialize_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class TrelloReadonlyResource(TrelloResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class TrelloCollection(base.RESTResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, **kwargs):
        """
        Fetch a collection.

        Upstream documentation: https://trello.com/docs/api/
        """
        params = base.get_params(None, kwargs, serialize_param=serialize_param)
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class TrelloReadonlyCollection(TrelloCollection):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()
