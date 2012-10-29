from libsaas import http, parsers, port
from libsaas.services import base

from . import advertisers
from . import publishers
from . import keywords


class MixRank(base.Resource):
    """
    """
    def __init__(self, api_key):
        """
        Create a MixRank service.

        :var api_key: The MixRank API key.
        :vartype api_key: str
        """
        self.apiroot = 'http://api.mixrank.com/v2/json/' + port.to_u(api_key)

    def get_url(self):
        return self.apiroot

    @base.resource(advertisers.Advertiser)
    def advertiser(self, advertiser):
        """
        Return the resource corresponding to an advertiser.

        :var advertiser: The advertiser's domain name. Use the root domain
          name; in particular, do not prefix with "www." or any other
          subdomain.
        :vartype advertiser: str
        """
        return advertisers.Advertiser(self, advertiser)

    @base.resource(publishers.Publisher)
    def publisher(self, publisher):
        """
        Return the resource corresponding to a publisher.

        :var publisher: The pubisher's domain name. Use the root domain
          name; in particular, do not prefix with "www." or any other
          subdomain.
        :vartype publisher: str
        """
        return publishers.Publisher(self, publisher)

    @base.resource(keywords.Keyword)
    def keyword(self, keyword):
        """
        Return the resource corresponding to a keyword.

        :var keyword: The keyword, can contain spaces.
        :vartype keyword: str
        """
        return keywords.Keyword(self, keyword)

    @base.apimethod
    def echo(self):
        """
        Verify that the API key is valid.
        """
        request = http.Request('GET', self.get_url() + '/echo')

        return request, parsers.parse_json
