from libsaas import http, parsers
from libsaas.services import base

from . import resource
from .comments import Comments, Comment
from .likes import Likes


class MediaBase(resource.ReadonlyResource):

    path = 'media'


class Media(MediaBase):

    @base.resource(Comments)
    def comments(self):
        """
        Return the resource corresponding to all comments for the media.
        """
        return Comments(self)

    @base.resource(Comment)
    def comment(self, comment_id):
        """
        Return the resource corresponding to a single comment for the media.
        """
        return Comment(self, comment_id)

    @base.resource(Likes)
    def likes(self):
        """
        Return the resource corresponding to all likes for the media.
        """
        return Likes(self)


class Medias(MediaBase):

    path = 'media/search'

    @base.apimethod
    def get(self, lat=None, max_timestamp=None, min_timestamp=None,
            lng=None, distance=None):
        """
        Fetch all of the objects.

        :var lat: Latitude of the center search coordinate.
            If used, lng is required.
        :vartype lat: float

        :var max_timestamp: A unix timestamp. All media returned will be
            taken later than this timestamp.
        :vartype max_timestamp: int

        :var min_timestamp: A unix timestamp. All media returned will be
            taken earlier than this timestamp.
        :vartype min_timestamp: int

        :var lng: Longitude of the center search coordinate.
            If used, lat is required.
        :vartype lng: float

        :var distance: Default is 1km (distance=1000), max distance is 5km.
        :vartype distance: int
        """
        params = base.get_params(
            ('lat', 'max_timestamp', 'min_timestamp', 'lng', 'distance'),
            locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class PopularMedia(MediaBase):

    path = 'media/popular'


class RecentMedia(MediaBase):

    path = 'media/recent'

    @base.apimethod
    def get(self, count=None, max_timestamp=None, min_timestamp=None,
            min_id=None, max_id=None):
        """
        Fetch all of the objects.

        :var count: Count of media to return.
        :vartype count: int

        :var max_timestamp: Return media before this UNIX timestamp.
        :vartype max_timestamp: int

        :var min_timestamp: Return media after this UNIX timestamp.
        :vartype min_timestamp: int

        :var min_id: Return media later than this min_id.
        :vartype min_id: int

        :var max_id: Return media earlier than this max_id.
        :vartype max_id: int
        """
        params = base.get_params(
            ('count', 'max_timestamp', 'min_timestamp', 'min_id', 'max_id'),
            locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class LikedMedia(MediaBase):

    path = 'media/liked'

    @base.apimethod
    def get(self, count=None, max_liked_id=None):
        """
        Fetch all of the objects.

        :var count: Count of media to return.
        :vartype count: int

        :var max_like_id: Return media liked before this id.
        :vartype max_like_id: int
        """
        params = base.get_params(('count', 'max_liked_id'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
