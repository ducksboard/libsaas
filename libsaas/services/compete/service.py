from libsaas.services import base

from . import resource


class Compete(base.Resource):
    """
    """
    def __init__(self, api_key):
        """
        Create an Compete service.

        :var api_key: The API key.
        :vartype api_key: str
        """
        self.apiroot = 'http://apps.compete.com'

        self.api_key = api_key
        self.add_filter(self.add_api_key)

    def get_url(self):
        return self.apiroot

    def add_api_key(self, request):
        request.params.update({'apikey': self.api_key})

    @base.resource(resource.Site)
    def site(self, domain):
        """
        Return the resource corresponding to a single site.
        """
        return resource.Site(self, domain)
