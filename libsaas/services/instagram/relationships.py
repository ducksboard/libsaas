from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Follows(resource.ReadonlyResource):

    path = 'follows'


class FollowedBy(resource.ReadonlyResource):

    path = 'followed-by'


class RequestedBy(resource.ReadonlyResource):

    path = 'requested-by'


class Relationship(resource.ReadonlyResource):

    path = 'relationship'

    @base.apimethod
    def update(self, action):
        """
        Modifies the relationship between the current user and the target user.

        :var action: One of follow/unfollow/block/unblock/approve/deny.
        :vartype action: str
        """
        request = http.Request('POST', self.get_url(), {'action': action})

        return request, parsers.parse_json
