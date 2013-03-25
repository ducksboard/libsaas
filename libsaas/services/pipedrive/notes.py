from libsaas import http, parsers
from libsaas.services import base


class NotesResource(base.RESTResource):

    path = 'notes'


class Notes(NotesResource):

    @base.apimethod
    def get(self, user_id=None, deal_id=None, person_id=None, org_id=None,
            start=None, limit=None, sort_by=None, sort_mode=None,
            start_date=None, end_date=None):
        """
        Returns all notes.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Notes
        """
        params = base.get_params(None, locals())
        return http.Request('GET', self.get_url(), params), parsers.parse_json


class Note(NotesResource):
    pass
