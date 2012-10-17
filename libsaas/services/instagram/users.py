from libsaas import http, parsers
from libsaas.services import base

from . import resource, media, feed, relationships


class UserBase(resource.ReadonlyResource):

    path = 'users'


class Users(UserBase):

    path = 'users/search'

    @base.apimethod
    def get(self, query, count=None):
        """
        Fetch all users by name.

        :var query: A query string.
        :vartype query: str

        :var count: Number of users to return.
        :vartype count: int
        """
        params = base.get_params(('count',), locals())
        params['q'] = query
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class User(UserBase):

    @base.resource(media.RecentMedia)
    def recent_media(self):
        """
        Return the resource corresponding to all recent media for the user.
        """
        return media.RecentMedia(self)

    @base.resource(relationships.Follows)
    def follows(self):
        """
        Return the resource corresponding to all follows for the user.
        """
        return relationships.Follows(self)

    @base.resource(relationships.FollowedBy)
    def followed_by(self):
        """
        Return the resource corresponding to all followers for the user.
        """
        return relationships.FollowedBy(self)

    @base.resource(relationships.Relationship)
    def relationship(self):
        """
        Return the resource corresponding to all relationships for the user.
        """
        return relationships.Relationship(self)


class AuthenticatedUser(UserBase):

    path = 'users/self'

    @base.resource(feed.Feed)
    def feed(self):
        """
        Return the resource corresponding to all entries for the user.
        """
        return feed.Feed(self)

    @base.resource(media.LikedMedia)
    def liked_media(self):
        """
        Return the resource corresponding to all liked media for the user.
        """
        return media.LikedMedia(self)

    @base.resource(relationships.RequestedBy)
    def requested_by(self):
        """
        Return the resource corresponding to all requests for the user.
        """
        return relationships.RequestedBy(self)

