from libsaas import http, parsers
from libsaas.services import base


class SpotifyResource(base.RESTResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Search(SpotifyResource):

    path = 'search/1'

    @base.apimethod
    def get(self, type, q, page=None):
        """
        Search in the Spotify's music catalogue.

        See https://developer.spotify.com/technologies/web-api/search/ and
        http://www.spotify.com/es/about/features/advanced-search-syntax/

        :var type: What to search for, artist, album or track.
        :vartype type: str

        :var q: Search string.
        :vartype q: str

        :var page: The page of the result set to return. defaults to 1
        :vartype page: int
        """
        url = '{0}/{1}'.format(self.get_url(), type)
        params = base.get_params(('q', 'page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    def artist(self, q, page=None):
        """
        Search for artists in the Spotify's music catalogue
        See http://www.spotify.com/es/about/features/advanced-search-syntax/

        :var q: Search string.
        :vartype q: str

        :var page: The page of the result set to return. defaults to 1
        :vartype page: int
        """
        return self.get('artist', q, page)

    def album(self, q, page=None):
        """
        Search for albums in the Spotify's music catalogue
        See http://www.spotify.com/es/about/features/advanced-search-syntax/

        :var q: Search string.
        :vartype q: str

        :var page: The page of the result set to return. defaults to 1
        :vartype page: int
        """
        return self.get('album', q, page)

    def track(self, q, page=None):
        """
        Search for tracks in the Spotify's music catalogue
        See http://www.spotify.com/es/about/features/advanced-search-syntax/

        :var q: Search string.
        :vartype q: str

        :var page: The page of the result set to return. defaults to 1
        :vartype page: int
        """
        return self.get('track', q, page)


class Lookup(SpotifyResource):

    NONE, BASIC, DETAILED = range(3)

    ALBUM_DETAIL = {
        BASIC: 'track',
        DETAILED: 'trackdetail'
    }

    ARTIST_DETAIL = {
        BASIC: 'album',
        DETAILED: 'albumdetail'
    }

    path = 'lookup/1/'

    @base.apimethod
    def get(self, uri, extras=None):
        """
        Lookup for an artist, album or track in the Spotify's music catalogue

        :var uri: Spotify valid uri
        :vartype uri: str

        :var extras: A comma-separated list of words that defines the detail
            level expected in the response.
        :vartype extras: str

        See https://developer.spotify.com/technologies/web-api/lookup/
        """
        params = base.get_params(('uri', 'extras'), locals())
        return http.Request('GET', self.get_url(), params), parsers.parse_json

    def artist(self, uri, detail=None):
        """
        Lookup for an artist in the Spotify's music catalogue

        :var uri: Spotify artist uri
        :vartype uri: str

        :var detail: Detail level expected in the response.
            Valid values are:
            1: returns basic information about all the albums the artist
            is featured in.
            2: returns detailed information about all the albums
            the artist is featured in.
        :vartype detail: int
        """
        extras = self.ARTIST_DETAIL.get(detail)
        return self.get(uri, extras)

    def album(self, uri, detail=None):
        """
        Lookup for an album in the Spotify's music catalogue

        :var uri: Spotify album uri
        :vartype uri: str

        :var detail: Detail level expected in the response.
            Valid values are:
            1: returns basic information about all the tracks the artist
            is featured in.
            2: returns detailed information about all the albums
            the artist is featured in.
        :vartype detail: int
        """
        extras = self.ALBUM_DETAIL.get(detail)
        return self.get(uri, extras)

    def track(self, uri):
        """
        Lookup for a track in the Spotify's music catalogue

        :var uri: Spotify track uri
        :vartype uri: str
        """
        return self.get(uri)
