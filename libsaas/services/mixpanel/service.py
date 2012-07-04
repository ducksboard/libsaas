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

    def __init__(self, token=None, api_key=None, api_secret=None):
        """
        Create a Mixpanel service.

        :var token: Optional token used for tracking events. If you leave this
            as None, you won't be able to track events through this service
            object.
        :vartype token: str or None

        :var api_key: Optional API key. If you leave this as None, you won't be
            able to export data through this service object.
        :vartype api_key: str or None

        :var api_secret: Optional API secret. If you leave this as None, you
            won't be able to export data through this service object.
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

        to_hash = ''.join('{0}={1}'.format(key, port.to_u(request.params[key]))
                          for key in sorted(request.params.keys()))

        md5 = hashlib.md5()
        md5.update(port.to_b(to_hash))
        md5.update(port.to_b(self.api_secret))

        request.params['sig'] = md5.hexdigest()

    def update_uri(self, request):
        if request.uri.startswith('http'):
            return

        request.uri = 'http://mixpanel.com/api/2.0/' + request.uri

    @base.apimethod
    def track(self, event, properties=None, ip=False, test=False):
        """
        Track an event.

        Upstream documentation: {0}

        :var event: The name of the event.
        :vartype event: str

        :var properties: The event's properties, your access token will be
            inserted into it automatically.
        :vartype properties: dict

        :var ip: Should Mixpanel automatically use the incoming request IP.
        :vartype ip: bool

        :var test: Use a high priority rate limited queue for testing.
        :vartype test: bool

        :return: A boolean that tells if the event has been logged.
        """
        if not self.token:
            raise InsufficientSettings('token is required for this method')

        if properties is None:
            properties = {}
        properties['token'] = self.token

        properties = dict((port.to_u(key), port.to_u(value))for
                          key, value in properties.items())

        params = base.get_params(('ip', 'test'), locals(),
                                 resources.serialize_param)

        data = {'event': port.to_u(event), 'properties': properties}
        params['data'] = base64.b64encode(port.to_b(json.dumps(data)))

        request = http.Request('GET', 'http://api.mixpanel.com/track/', params)
        request.nosign = True

        return request, resources.parse_boolean

    track.__doc__ = track.__doc__.format(
        'https://mixpanel.com/docs/api-documentation/'
        'http-specification-insert-data')

    @base.apimethod
    def export(self, from_date, to_date, event=None, where=None, bucket=None):
        """
        Export raw data from your account.

        Upstream documentation: {0}

        :var from_date: Query start date, in yyyy-mm-dd format.
        :vartype from_date: str

        :var to_date: Query finish date, in yyyy-mm-dd format.
        :vartype to_date: str

        :var event: Optional list of events to export.
        :vartype event: list of str

        :var where: A filter expression.
        :vartype where: str

        :var bucket: Data bucket to query.
        :vartype bucket: str
        """
        params = base.get_params(('from_date', 'to_date',
                                  'event', 'where', 'bucket'),
                                 locals(), resources.serialize_param)

        uri = 'http://data.mixpanel.com/api/2.0/export/'
        request = http.Request('GET', uri, params)

        return request, resources.parse_export

    export.__doc__ = export.__doc__.format(
        'https://mixpanel.com/docs/api-documentation/'
        'exporting-raw-data-you-inserted-into-mixpanel#export')

    @base.resource(resources.Events)
    def events(self):
        """
        Return the resource corresponding to events.
        """
        return resources.Events(self)

    @base.resource(resources.Properties)
    def properties(self):
        """
        Return the resource corresponding to events properties.
        """
        return resources.Properties(self)

    @base.resource(resources.Funnels)
    def funnels(self):
        """
        Return the resource corresponding to funnels.
        """
        return resources.Funnels(self)

    @base.resource(resources.Segmentation)
    def segmentation(self):
        """
        Return the resource corresponding to segmentation.
        """
        return resources.Segmentation(self)

    @base.resource(resources.Retention)
    def retention(self):
        """
        Return the resource corresponding to retention (cohort analysis).
        """
        return resources.Retention(self)


def add_docstrings():
    # the upstream URLs follow a fixed pattern, so add them programatically

    def extra_doc(resource_name, method_name):
        base = 'https://mixpanel.com/docs/api-documentation/data-export-api'
        method_name = 'default' if method_name == 'get' else method_name
        doc_name = ('event-properties' if resource_name == 'properties'
                    else resource_name)

        tmpl = '\nUpstream documentation: {0}#{1}-{2}'
        return tmpl.format(base, doc_name, method_name)

    # walk the list of resources
    for resource_name in Mixpanel.list_resources():
        # get the resource class
        resource = getattr(Mixpanel, resource_name).produces[0]
        # walks its list of methods
        for method_name in resource.list_methods():
            # update the method's docstring
            function = port.method_func(resource, method_name)
            extra = extra_doc(resource_name, method_name)
            function.__doc__ += extra


add_docstrings()
