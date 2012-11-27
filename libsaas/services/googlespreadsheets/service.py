from libsaas import http, xml
from libsaas.services import base

from . import resource


class GoogleSpreadsheets(base.Resource):

    APIROOT = 'https://spreadsheets.google.com/feeds'

    def __init__(self, access_token=None):
        """
        Create a Google Spreadsheets service.

        :var access_token:
        :vartype access_token:
        """
        self.access_token = access_token

        self.add_filter(self.add_auth)
        self.add_filter(self.set_format)

    def add_auth(self, request):
        header = 'Bearer {0}'.format(self.access_token)
        request.headers['Authorization'] = header

    def get_url(self):
        return self.APIROOT

    def set_format(self, request):
        if request.method.upper() in http.URLENCODE_METHODS:
            request.params['alt'] = 'json'
        else:
            request.headers['Content-Type'] = 'application/atom+xml'
            request.params = xml.dict_to_xml(request.params)

    def set_access_token(self, access_token):
        self.access_token = access_token

    @base.resource(resource.Spreadsheets)
    def spreadsheets(self):
        """
        Return the resource corresponding to all the spreadsheets
        """
        return resource.Spreadsheets(self)

    @base.resource(resource.Spreadsheet)
    def spreadsheet(self, key):
        """
        Return the resource corresponding to a single spreadsheet
        """
        return resource.Spreadsheet(self, key)
