from libsaas.services import base

from . import resource


class ReadonlyNotesBase(resource.UserVoiceResource):

    path = 'notes'

    def create(self, obj):
        raise base.MethodNotSupported()


class Notes(ReadonlyNotesBase):
    pass


class UserNotes(ReadonlyNotesBase):
    pass


class ForumSuggestionNotesBase(resource.UserVoiceTextResource):

    path = 'notes'

    def wrap_object(self, obj):
        return {'note': {'text': obj}}


class ForumSuggestionNotes(ForumSuggestionNotesBase):
    pass


class ForumSuggestionNote(ForumSuggestionNotesBase):
    pass
