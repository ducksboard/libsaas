from libsaas import http, parsers
from libsaas.services import base

from . import resource


class TicketsBase(resource.UserVoiceResource):

    path = 'tickets'

    def wrap_object(self, obj):
        return {'ticket': obj}


class Tickets(TicketsBase):

    @base.apimethod
    def get(self, page=None, per_page=None, assigne_id=None, filter=None,
            sort=None, state=None, updated_after_date=None):
        """
        Fetch all of the tickets.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var assignee_id: The ID of the user assigned to the ticket.
        :vartype assignee_id: int

        :var filter: Either `all` or `assigned_after`.
        :vartype filter: str

        :var sort: How should the returned collection be sorted. Refer to
            upstream documentation for possible values.
        :vartype sort: str

        :var state: Ticket state. Refer to upstream documentation for possible
            values.
        :vartype state: str

        :var updated_after_date: If `filter` is `assigned_after`, a date string
            formatted `yyyy-mm-dd HH:MM:SS -0000`.
        :var updated_after_date: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def upsert(self, obj):
        """
        Create or update a ticket

        :var obj: a Python object representing the ticket. Refer to the upstream
            documentation for details.
        """
        url = '{0}/upsert'.format(self.get_url())
        request = http.Request('PUT', url, self.wrap_object(obj))

        return request, parsers.parse_empty

    @base.apimethod
    def search(self, page=None, per_page=None, query=None):
        """
        Search for tickets.

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


class TicketNotesBase(resource.UserVoiceTextResource):

    path = 'notes'

    def wrap_object(self, obj):
        return {'note': {'text': obj}}


class TicketNotes(TicketNotesBase):
    pass


class TicketNote(TicketNotesBase):
    pass


class TicketMessages(resource.UserVoiceTextResource):

    path = 'ticket_messages'

    def wrap_object(self, obj):
        return {'ticket_message': obj}


class Ticket(TicketsBase):

    @base.resource(TicketNote)
    def note(self, note_id):
        """
        Return the resource corresponding to a single ticket note.
        """
        return TicketNote(self, note_id)

    @base.resource(TicketNotes)
    def notes(self):
        """
        Return the resource corresponding to all the ticket notes.
        """
        return TicketNotes(self)

    @base.resource(TicketMessages)
    def messages(self):
        """
        Return the resource corresponding to all the ticket messages.
        """
        return TicketMessages(self)
