from libsaas.services import base

from .resource import Application, Applications


class Flurry(base.Resource):
    """
    """
    def __init__(self, api_access_code):
        """
        Create a Flurry service.

        :var api_access_code: The API access code.
        :vartype api_access_code: str
        """
        self.apiroot = 'http://api.flurry.com'

        self.api_access_code = api_access_code

        self.add_filter(self.add_authorization)
        self.add_filter(self.add_json)

    def add_authorization(self, request):
        request.params['apiAccessCode'] = self.api_access_code

    def add_json(self, request):
        request.headers['Content-Type'] = 'application/json'

    def get_url(self):
        return self.apiroot

    @base.resource(Applications)
    def applications(self):
        """
        Return the resource corresponding to all applications.
        """
        return Applications(self)

    @base.resource(Application)
    def application(self, application_api_key):
        """
        Returns the resource corresponding to a single application.
        """
        return Application(self, application_api_key)
