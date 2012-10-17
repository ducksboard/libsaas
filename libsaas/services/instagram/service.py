from libsaas import http
from libsaas.services import base

from . import geographies
from .tags import Tags, Tag
from .locations import Locations, Location
from .media import Medias, Media, PopularMedia
from .users import Users, User, AuthenticatedUser

class Instagram(base.Resource):
    """
    """
    def __init__(self, client_id=None, access_token=None):
        """
        Create an Instagram service.

        :var client_id: Associates your script with a specific application.
            Required if no access_token.
        :vartype client_id: str

        :var access_token: For some requests, specifically those made on behalf
            of a user, authentication is needed. Required if no client_id.
        :vartype access_token: str
        """
        if not client_id and not access_token:
           raise TypeError('__init__() must be passed at least one '
                           'of client_id, access_token')

        self.apiroot = 'https://api.instagram.com/v1'

        self.client_id = client_id
        self.access_token = access_token
        self.add_filter(self.add_authorization)

    def add_authorization(self, request):
        params = {}
        if self.access_token:
            params['access_token'] = self.access_token
        else:
            params['client_id'] = self.client_id

        # executors will only url encode params for the methods
        # in http.URLENCODED_METHODS. That won't work for Instagram API
        # as they expect the token to be part of the url.
        if request.method.upper() == 'DELETE':
            request.uri += '?' + http.urlencode_any(params)
        else:
            request.params.update(params)
            if request.method.upper() not in http.URLENCODE_METHODS:
                request.headers['Content-Type'] = (
                    'application/x-www-form-urlencoded')

    def get_url(self):
        return self.apiroot

    @base.resource(Users)
    def users(self):
        """
        Return the resource corresponding to all users.
        """
        return Users(self)

    @base.resource(User)
    def user(self, user_id):
        """
        Return the resource corresponding to a single user.
        """
        return User(self, user_id)

    @base.resource(AuthenticatedUser)
    def authenticated_user(self):
        """
        Return the resource corresponding to the authenticated user.
        """
        return AuthenticatedUser(self)

    @base.resource(Medias)
    def medias(self):
        """
        Return the resource corresponding to all medias.
        """
        return Medias(self)

    @base.resource(PopularMedia)
    def popular_media(self):
        """
        Return the resource corresponding to all most popular media.
        """
        return PopularMedia(self)

    @base.resource(Media)
    def media(self, media_id):
        """
        Return the resource corresponding to a single media.
        """
        return Media(self, media_id)

    @base.resource(Tags)
    def tags(self):
        """
        Return the resource corresponding to all tags.
        """
        return Tags(self)

    @base.resource(Tag)
    def tag(self, tag_name):
        """
        Return the resource corresponding to a single tag.
        """
        return Tag(self, tag_name)

    @base.resource(Locations)
    def locations(self):
        """
        Return the resource corresponding to all locations.
        """
        return Locations(self)

    @base.resource(Location)
    def location(self, location_id):
        """
        Return the resource corresponding to a single location.
        """
        return Location(self, location_id)

    @base.resource(geographies.Geography)
    def geography(self, geo_id):
        """
        Return the resource corresponding to a single geography
        """
        return geographies.Geography(self, geo_id)
