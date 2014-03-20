from libsaas.services import base
from libsaas import parsers, http, port


class User(base.Resource):

    def __init__(self, parent, object_id=None):
        self.parent = parent
        self.object_id = object_id

    def get_url(self, method):
        return '{0}/{1}'.format(self.parent.get_url(), method)

    def _post(self, method, data):
        data['userId'] = self.object_id

        request = http.Request('POST', self.get_url(method), data)
        return request, parsers.parse_json

    @base.apimethod
    def identify(self, traits=None, context=None, timestamp=None):
        """
        Identify an user.

        :var traits: A dictionary of traits you know about the user.
        :vartype traits: dict

        :var context: A dictionary of provider specific options.
        :vartype context: dict

        :var timestamp: An ISO 8601 date string representing
        when the identify took place.
        :vartype timestamp: str
        """
        params = base.get_params(None, locals())
        return self._post('identify', params)

    @base.apimethod
    def track(self, event, properties=None, context=None, timestamp=None):
        """
        Track an event.

        :var event: The name of the event you're tracking.
        :vartype event: str

        :var properties: A dictionary of properties for the event.
        :vartype properties: dict

        :var context: A dictionary of provider specific options.
        :vartype context: dict

        :var timestamp: An ISO 8601 date string representing
        when the event took place.
        :vartype timestamp: str
        """
        params = base.get_params(None, locals())
        return self._post('track', params)
