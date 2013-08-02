import base64
import calendar
import hashlib
import hmac
import json
import time

from libsaas import parsers, http, port
from libsaas.services import base

from . import resources


class Mozscape(base.Resource):

    EXPIRES = 300
    timesource = time.gmtime

    def __init__(self, access_id, secret_key):
        """
        Create a Mozscape service.

        :var access_id: Your Mozscape AccessID.
        :vartype access_id: str

        :var secret_key: Your Mozscape Secret Key.
        :vartype secret_key: str
        """
        self.apiroot = 'https://lsapi.seomoz.com/linkscape'

        self.access_id = access_id
        self.secret_key = secret_key

        self.add_filter(self.add_api_root)
        self.add_filter(self.sign_request)

    def add_api_root(self, request):
        request.uri = self.apiroot + request.uri

    def sign_request(self, request):
        if getattr(request, 'nosign', False):
            return

        expires = str(calendar.timegm(self.timesource()) + self.EXPIRES)
        to_sign = port.to_b(self.access_id + '\n' + expires)
        signature = hmac.new(port.to_b(self.secret_key), to_sign, hashlib.sha1).digest()

        request.params['AccessID'] = self.access_id
        request.params['Expires'] = expires
        request.params['Signature'] = port.to_u(base64.b64encode(signature))

    @base.apimethod
    def urlmetrics(self, urls, cols):
        """
        Fetch URL metrics for one or more URLs.

        :var urls: The URLs you're interested in.
        :vartype urls: str or list of str

        :var cols: The sum of column constants for metrics you want to have
            fetched, taken from `libsaas.services.mozscape.constants`.
        """
        if isinstance(urls, list):
            return self.list_urlmetrics(urls, str(cols))

        uri = '/url-metrics/{0}/'.format(http.quote_any(urls))
        request = http.Request('GET', uri, {'Cols': str(cols)})

        return request, parsers.parse_json

    def list_urlmetrics(self, urls, cols):
        # For url-metrics the URLs are passed as POST body, but the remaining
        # parameters should still be in the URL. Work around this by manually
        # generating the signature and then replacing the body.
        request = http.Request('POST', '')
        self.sign_request(request)
        request.nosign = True

        request.params['Cols'] = cols
        uri = '/url-metrics/?' + http.urlencode_any(request.params)
        request.uri = uri
        request.params = json.dumps(urls)

        return request, parsers.parse_json

    @base.resource(resources.Metadata)
    def metadata(self):
        """
        Return the resource responsible for Mozscape Index metadata.
        """
        return resources.Metadata(self)
