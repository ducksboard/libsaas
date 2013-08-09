import json

from libsaas import http
from libsaas.services import base

from . import reporting


class GoogleAnalytics(base.Resource):

    APIROOT = 'https://www.googleapis.com/analytics/v3'

    def __init__(self, access_token=None):
        """
        Create a Google Analytics service.

        :var access_token:
        :vartype access_token:
        """
        self.access_token = access_token

        self.add_filter(self.add_auth)
        self.add_filter(self.use_json)

    def add_auth(self, request):
        header = 'Bearer {0}'.format(self.access_token)
        request.headers['Authorization'] = header

    def use_json(self, request):
        if (request.method.upper() not in http.URLENCODE_METHODS
                and request.params):
            request.headers['Content-Type'] = 'application/json'
            request.params = json.dumps(request.params)

    def get_url(self):
        return self.APIROOT

    def set_access_token(self, access_token):
        self.access_token = access_token

    @base.resource(reporting.Reporting)
    def reporting(self):
        """
        Return the resource corresponding to the reporting API
        """
        return reporting.Reporting(self)
