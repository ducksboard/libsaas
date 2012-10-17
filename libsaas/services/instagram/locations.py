from libsaas import http, parsers
from libsaas.services import base

from . import resource, media


class LocationBase(resource.ReadonlyResource):

    path = 'locations'


class Locations(LocationBase):

    path = 'locations/search'

    @base.apimethod
    def get(self, lat=None, distance=None, lng=None,
            foursquare_v2_id=None, foursquare_id=None):
        """
        fetch all locations by geographic coordinate.

        :var lat: Latitude of the center search coordinate.
            If used, lng is required.
        :vartype lat: float

        :var distance: Default is 1km (distance=1000), max distance is 5km.
        :vartype distance: int

        :var lng: Longitude of the center search coordinate.
            If used, lat is required.
        :vartype lng: float

        :var foursquare_v2_id: A foursquare v2 api location id.
            If used, you are not required to use lat and ln
        :vartype foursquare_v2_id: str

        :var foursquare_id: A foursquare v1 api location id.
            If used, you are not required to use lat and lng.
            Note that this method is deprecated; you should use the
            new foursquare IDs with V2 of their API.
        :vartype foursquare_id: str
        """
        params = base.get_params(
            ('lat', 'distance', 'lng', 'foursquare_v2_id', 'foursquare_id'),
            locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class Location(LocationBase):

    @base.resource(media.RecentMedia)
    def recent_media(self):
        """
        Return the resource corresponding to all recent media
        for the location.
        """
        return media.RecentMedia(self)
