import base64
import calendar
import hashlib
import json
import time

from libsaas import http, port
from libsaas.services import base

from . import resources


class InsufficientSettings(Exception):
    """
    The settings of the service are not sufficient to make the request.
    """



class Mixpanel(base.Resource):
    """
    """
    USE_EXPIRE = True

    def __init__(self, token, api_key=None, api_secret=None):
        """
        Create a Mixpanel service.

        :var token: The token used for tracking events.
        :vartype token: str

        :var api_key: Optional API key. If you leave this as None, you won't be
            able to export data through this service object.
        :vartype api_key: str or None

        :var api_secret: Optional API secret. If you leave this as None, you won't be
            able to export data through this service object.
        :vartype api_secret: str or None
        """
        self.token = token
        self.api_key = api_key
        self.api_secret = api_secret

        self.add_filter(self.sign_request)
        self.add_filter(self.update_uri)

    def sign_request(self, request):
        if getattr(request, 'nosign', False):
            return

        if not self.api_key or not self.api_secret:
            raise InsufficientSettings('api_key and api_secret are required '
                                       'for this method')

        request.params['api_key'] = self.api_key

        if self.USE_EXPIRE:
            request.params['expire'] = calendar.timegm(time.gmtime()) + 600

        to_hash = ''.join('{0}={1}'.format(key, request.params[key]) for key in
                          sorted(request.params.keys()))

        md5 = hashlib.md5()
        md5.update(to_hash.encode('utf-8'))
        md5.update(self.api_secret.encode('utf-8'))

        request.params['sig'] = md5.hexdigest()

    def update_uri(self, request):
        if request.uri.startswith('http'):
            return

        request.uri = 'http://mixpanel.com/api/2.0/' + request.uri

    @base.apimethod
    def track(self, event, properties=None, ip=False, test=False):
        if properties is None:
            properties = {}
        properties['token'] = self.token

        properites = dict((port.to_u(key), port.to_u(value))for
                          key, value in properties.items())

        params = base.get_params(('ip', 'test'), locals(),
                                 resources.serialize_param)

        data = {'event': port.to_u(event), 'properties': properties}
        params['data'] = base64.b64encode(json.dumps(data).encode('utf-8'))

        request = http.Request('GET', 'http://api.mixpanel.com/track/', params)
        request.nosign = True

        return request, resources.parse_boolean

    @base.apimethod
    def export(self, from_date, to_date, event, where=None, bucket=None):
        params = base.get_params(('from_date', 'to_date',
                                  'event', 'where', 'bucket'),
                                 locals(), resources.serialize_param)

        uri = 'http://data.mixpanel.com/api/2.0/export/'
        request = http.Request('GET', uri, params)

        return request, resources.parse_export

    @base.resource(resources.Events)
    def events(self):
        return resources.Events(self)

    @base.resource(resources.Properties)
    def properties(self):
        return resources.Properties(self)

    @base.resource(resources.Funnels)
    def funnels(self):
        return resources.Funnels(self)

    @base.resource(resources.Segmentation)
    def segmentation(self):
        return resources.Segmentation(self)

    @base.resource(resources.Retention)
    def retention(self):
        return resources.Retention(self)
