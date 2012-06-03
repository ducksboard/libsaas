import json

from libsaas import http, parsers, port
from libsaas.services import base


def parse_boolean(body, code, headers):
    # Mixpanel's track endpoint responds with '1' for True and '0' for False
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)

    if body == b'1':
        return True
    elif body == b'0':
        return False

    raise http.HTTPError(body, code, headers)


def parse_export(body, code, headers):
    # the export endpoint returns lines of JSON values
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)

    # JSON mandates the use of UTF-8, so assume each line is decodable
    return [json.loads(line.decode('utf-8')) for line in body.splitlines()]


def serialize_param(val):
    if isinstance(val, bool):
        return '1' if val else '0'
    if isinstance(val, list):
        return json.dumps([port.to_u(v) for v in val])
    return val


class Events(base.Resource):

    @base.apimethod
    def get(self, event, type, unit, interval):
        """
        Fetch event data.
        """
        params = base.get_params(('event', 'type', 'unit', 'interval'),
                                 locals(), serialize_param)
        request = http.Request('GET', 'events/', params)

        return request, parsers.parse_json

    @base.apimethod
    def top(self, type, limit=None):
        """
        Fetch the top events for today.
        """
        params = base.get_params(('type', 'limit'), locals(), serialize_param)
        request = http.Request('GET', 'events/top/', params)

        return request, parsers.parse_json

    @base.apimethod
    def names(self, type, limit=None):
        """
        Fetch the most common events over the last 31 days.
        """
        params = base.get_params(('type', 'limit'), locals(), serialize_param)
        request = http.Request('GET', 'events/names/', params)

        return request, parsers.parse_json


class Properties(base.Resource):

    @base.apimethod
    def get(self, event, name, type, unit, interval,
                   values=None, limit=None):
        """
        Fetch data of a single event.
        """
        params = base.get_params(('event', 'name', 'type',
                                  'unit', 'interval', 'values', 'limit'),
                                 locals(), serialize_param)
        request = http.Request('GET', 'events/properties/', params)

        return request, parsers.parse_json

    @base.apimethod
    def top(self, event, limit=None):
        """
        Fetch top property names for an event.
        """
        params = base.get_params(('event', 'limit'), locals(), serialize_param)

        request = http.Request('GET', 'events/properties/top/', params)

        return request, parsers.parse_json

    @base.apimethod
    def values(self, event, name, limit=None, bucket=None):
        """
        Fetch top values for a property.
        """
        params = base.get_params(('event', 'name', 'limit', 'bucket'),
                                 locals(), serialize_param)

        request = http.Request('GET', 'events/properties/values/', params)

        return request, parsers.parse_json


class Funnels(base.Resource):

    @base.apimethod
    def get(self, funnel_id, from_date=None, to_date=None, length=None,
            interval=None, unit=None, on=None, where=None, limit=None):
        """
        Fetch data for a funnel.
        """
        params = base.get_params(
            ('funnel_id', 'from_date', 'to_date', 'length', 'interval',
             'unit', 'on', 'where', 'limit'), locals(), serialize_param)

        request = http.Request('GET', 'funnels/', params)

        return request, parsers.parse_json

    @base.apimethod
    def list(self):
        """
        Fetch the list of all funnels.
        """
        request = http.Request('GET', 'funnels/list/')

        return request, parsers.parse_json


class Segmentation(base.Resource):

    @base.apimethod
    def get(self, event, from_date, to_date, on=None, unit=None, where=None,
            limit=None, type=None):
        """
        Fetch segmented and filtered data for an event.
        """
        params = base.get_params(('event', 'from_date', 'to_date', 'on',
                                 'unit', 'where', 'limit', 'type'),
                                 locals(), serialize_param)

        request = http.Request('GET', 'segmentation/', params)

        return request, parsers.parse_json

    @base.apimethod
    def numeric(self, event, from_date, to_date, on, buckets, unit=None,
                where=None, type=None):
        """
        Fetch segmented and filtered data for an event, sorted into numeric
        buckets.
        """
        params = base.get_params(('event', 'from_date', 'to_date', 'on',
                                 'buckets', 'unit', 'where', 'type'),
                                 locals(), serialize_param)

        request = http.Request('GET', 'segmentation/numeric/', params)

        return request, parsers.parse_json

    @base.apimethod
    def sum(self, event, from_date, to_date, on, unit=None, where=None):
        """
        Fetch the sum of an expression for an event per time unit.
        """
        params = base.get_params(('event', 'from_date', 'to_date', 'on',
                                  'unit', 'where'), locals(), serialize_param)

        request = http.Request('GET', 'segmentation/sum/', params)

        return request, parsers.parse_json

    @base.apimethod
    def average(self, event, from_date, to_date, on, unit=None, where=None):
        """
        Fetch the average of an expression for an event per time unit.
        """
        params = base.get_params(('event', 'from_date', 'to_date', 'on',
                                  'unit', 'where'), locals(), serialize_param)

        request = http.Request('GET', 'segmentation/average/', params)

        return request, parsers.parse_json


class Retention(base.Resource):

    @base.apimethod
    def get(self, from_date, to_date, retention_type=None, born_event=None,
            event=None, born_Where=None, where=None, interval=None,
            interval_count=None, unit=None, on=None, limit=None):
        """
        Fetch cohort analysis.
        """
        params = base.get_params(('from_date', 'to_date', 'retention_type',
                                  'born_event', 'event', 'born_where', 'where',
                                  'interval', 'interval_count', 'unit',
                                  'on', 'limit'), locals(), serialize_param)

        request = http.Request('GET', 'retention/', params)

        return request, parsers.parse_json
