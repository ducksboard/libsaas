from libsaas.services import base

from . import resource, categories, streams, suggestions


class ForumsBase(resource.UserVoiceResource):

    path = 'forums'

    def wrap_object(self, obj):
        return {'forum': obj}


class Forums(ForumsBase):
    pass


class Forum(ForumsBase):

    @base.resource(suggestions.ForumUserSuggestions)
    def user_suggestions(self, user_id):
        """
        Return a resource corresponding to all the suggestions of a  single
        user on this forum.
        """
        return suggestions.ForumUserSuggestions(self, user_id)

    @base.resource(suggestions.ForumSuggestion)
    def suggestion(self, suggestion_id):
        """
        Return a resource corresponding to a single suggestion on a forum.
        """
        return suggestions.ForumSuggestion(self, suggestion_id)

    @base.resource(suggestions.ForumSuggestions)
    def suggestions(self):
        """
        Return a resource corresponding to all the suggestion on a forum.
        """
        return suggestions.ForumSuggestions(self)

    @base.resource(streams.Stream)
    def stream(self):
        """
        Return a resource corresponding to the stream of events for this forum.
        """
        return streams.Stream(self)

    @base.resource(categories.ForumCategory)
    def category(self, category_id):
        """
        Return a resource corresponding to a single category on this forum.
        """
        return categories.ForumCategory(self, category_id)

    @base.resource(categories.ForumCategories)
    def categories(self):
        """
        Return a resource corresponding to all the categories on this forum.
        """
        return categories.ForumCategories(self)
