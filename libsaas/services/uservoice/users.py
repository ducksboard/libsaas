from libsaas import http, parsers
from libsaas.services import base

from . import resource, comments, notes, suggestions


class UsersBase(resource.UserVoiceResource):

    path = 'users'

    def wrap_object(self, obj):
        return {'user': obj}


class Users(UsersBase):

    @base.apimethod
    def search(self, page=None, per_page=None, guid=None, query=None):
        """
        Search for users. One of `guid` or `query` mest be present.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var guid: Search by SSO GUID
        :vartype guid: str

        :var query: Search by username substring.
        :vartype query: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'search')

        return http.Request('GET', url, params), parsers.parse_json


class User(UsersBase):

    @base.resource(suggestions.UserSuggestions)
    def suggestions(self):
        """
        Return a resource corresponding to all of this user's suggestions.
        """
        return suggestions.UserSuggestions(self)

    @base.resource(notes.UserNotes)
    def notes(self):
        """
        Return the resource corresponding to all of this user's notes.
        """
        return notes.UserNotes(self)

    @base.resource(comments.UserComments)
    def comments(self):
        """
        Return the resource corresponding to all of this user's comments.
        """
        return comments.UserComments(self)

class CurrentUser(base.HierarchicalResource):

    path = 'users'

    @base.apimethod
    def get(self):
        url = '{0}/{1}'.format(self.get_url(), 'current')

        return http.Request('GET', url), parsers.parse_json
