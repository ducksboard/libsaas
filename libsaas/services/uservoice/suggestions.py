from libsaas import http, parsers
from libsaas.services import base

from . import resource, comments, flags, notes


class SuggestionsBase(resource.UserVoiceResource):

    path = 'suggestions'

    def wrap_object(self, obj):
        return {'suggestion': obj}


class Suggestions(SuggestionsBase):

    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def search(self, page=None, per_page=None, query=None):
        """
        Search for suggestions.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var query: Search string.
        :vartype query: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'search')

        return http.Request('GET', url, params), parsers.parse_json


class Suggestion(SuggestionsBase):

    def update(self, obj):
        raise base.MethodNotSupported()

    def delete(self):
        raise base.MethodNotSupported()


class ForumSuggestion(SuggestionsBase):

    @base.apimethod
    def supporters(self, page=None, per_page=None, sort=None):
        """
        Fetch the supporters for this suggestion.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'supporters')

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def respond(self, obj):
        """
        Respond to a suggestion.

        :var obj: a Python object representing the response. Refer to the
            upstream documentation for details.
        """
        url = '{0}/{1}'.format(self.get_url(), 'respond')
        request = http.Request('PUT', url, {'response': obj})

        return request, parsers.parse_json

    @base.apimethod
    def vote(self):
        """
        Vote for this suggestion.
        """
        url = '{0}/{1}'.format(self.get_url(), 'votes')
        request = http.Request('POST', url, {'to': '1'})

        return request, parsers.parse_json

    @base.resource(notes.ForumSuggestionNote)
    def note(self, note_id):
        """
        Return the resource corresponding to a single note on this suggestion.
        """
        return notes.ForumSuggestionNote(self, note_id)

    @base.resource(notes.ForumSuggestionNotes)
    def notes(self):
        """
        Return the resource corresponding to all the notes on this suggestion.
        """
        return notes.ForumSuggestionNotes(self)

    @base.resource(comments.ForumSuggestionComment)
    def comment(self, comment_id):
        """
        Return the resource corresponding to a single comment on this suggestion.
        """
        return comments.ForumSuggestionComment(self, comment_id)

    @base.resource(comments.ForumSuggestionComments)
    def comments(self):
        """
        Return the resource corresponding to all the comments on this suggestion.
        """
        return comments.ForumSuggestionComments(self)

    @base.resource(flags.SuggestionFlags)
    def flags(self):
        """
        Return the resource corresponding to all the flags of this suggestion.
        """
        return flags.SuggestionFlags(self)


class ForumSuggestions(SuggestionsBase):

    @base.apimethod
    def get(self, page=None, per_page=None, category=None,
            filter=None, sort=None, updated_after_date=None):
        """
        Fetch suggestions from this forum.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var category: Either a category ID, `all` or `uncategorized`. See
            upstream documentation for details.
        :vartype category: str

        :var filter: The kind of suggestions to return, see upstream
            documentation for possible values.
        :vartype filter: str

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str

        :var updated_after_date: If `filter` is `assigned_after`, a date string
            formatted `yyyy-mm-dd HH:MM:SS -0000`.
        :var updated_after_date: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def search(self, page=None, per_page=None, category_id=None, query=None):
        """
        Search for suggestions on this forum.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var category_id: A category ID.
        :vartype category_id: int

        :var query: Search string.
        :vartype query: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'search')

        return http.Request('GET', url, params), parsers.parse_json


class UserSuggestions(SuggestionsBase):

    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, page=None, per_page=None, category=None,
            filter=None, sort=None):
        """
        Fetch suggestions from this user on this forum.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var category: Either a category ID, `all` or `uncategorized`. See
            upstream documentation for details.
        :vartype category: str

        :var filter: The kind of suggestions to return, see upstream
            documentation for possible values.
        :vartype filter: str

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class ForumUserSuggestions(SuggestionsBase):

    def get_url(self):
        return '{0}/users/{1}/{2}'.format(self.parent.get_url(),
                                          self.object_id, self.path)

    def update(self, obj):
        raise base.MethodNotSupported()

    def delete(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, page=None, per_page=None, category=None,
            filter=None, sort=None):
        """
        Fetch suggestions from this user on this forum.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var category: Either a category ID, `all` or `uncategorized`. See
            upstream documentation for details.
        :vartype category: str

        :var filter: The kind of suggestions to return, see upstream
            documentation for possible values.
        :vartype filter: str

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
