from libsaas.services import base

from . import resources


class Spotify(base.Resource):
    """
    """
    def __init__(self):
        """
        Create a Spotify service.
        """
        self.apiroot = 'http://ws.spotify.com/'
        self.add_filter(self.use_json)

    def use_json(self, request):
        request.headers['Content-Type'] = 'application/json'
        request.headers['Accept'] = 'application/json'

    def get_url(self):
        return self.apiroot

    @base.resource(resources.Search)
    def search(self):
        """
        Return the resource corresponding to the search service
        """
        return resources.Search(self)

    @base.resource(resources.Lookup)
    def lookup(self):
        """
        Return the resource corresponding to the lookup service
        """
        return resources.Lookup(self)
