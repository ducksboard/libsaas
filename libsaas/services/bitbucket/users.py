from libsaas import http, parsers
from libsaas.services import base

from . import resource, events, followers


class User(resource.BitBucketResource):

    def __init__(self, parent, user_id=None):
        self.parent = parent
        self.user_id = user_id

    def get_url(self):
        if self.user_id is None:
            return '{0}/user'.format(self.parent.get_url())

        return '{0}/users/{1}'.format(self.parent.get_url(), self.user_id)

    @base.apimethod
    def follows(self):
        """
        Fetch the list of repositories the authenticated user follows.
        """
        request = http.Request('GET', '{0}/follows'.format(self.get_url()))

        return request, parsers.parse_json

    @base.resource(events.UserEvents)
    def events(self):
        """
        Return a resource corresponding with this user events.
        """
        return events.UserEvents(self)

    @base.resource(followers.UserFollowers)
    def followers(self):
        """
        Return a resource corresponding with this user followers.
        """
        return followers.UserFollowers(self)
