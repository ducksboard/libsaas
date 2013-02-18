from libsaas.services import base

from . import resource, links, users


class Bitly(base.Resource):
    def __init__(self, token):
        """
        Create a Bitly service.

        :var token: an OAuth 2.0 token.
        :vartype token: str

        """
        self.apiroot = 'https://api-ssl.bitly.com/v3'

        self.access_token = token
        self.add_filter(self.add_authorization)

    def add_authorization(self, request):
        request.params.update({
            'access_token': self.access_token
        })

    def get_url(self):
        return self.apiroot

    @base.resource(users.User)
    def user(self):
        """
        Return the resource corresponding to a single user.
        """
        return users.User(self)

    @base.resource(links.Link)
    def link(self, link):
        """
        Return the resource corresponding to a single link.
        """
        return links.Link(self, link)

    @base.resource(resource.HighValue)
    def highvalue(self):
        """
        Return the resource corresponding to all high-value links.
        """
        return resource.HighValue(self)

    @base.resource(resource.Search)
    def search(self):
        """
        Return the resource corresponding to all links.
        """
        return resource.Search(self)

    @base.resource(resource.RealTime)
    def realtime(self):
        """
        Return the resource corresponding to a single object.
        """
        return resource.RealTime(self)
