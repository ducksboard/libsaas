from libsaas import http, parsers
from libsaas.services import base

from .resource import BasecampResource
from .attachments import Attachments
from .topics import ProjectTopics
from . import todolists as tdl
from . import documents as doc
from . import accesses as acc
from . import comments as c
from . import uploads as u
from . import events as ev
from . import calendars


class MessageResource(BasecampResource):
    path = 'messages'


class Messages(MessageResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Message(MessageResource):

    @base.resource(c.Comments)
    def comments(self):
        """
        Return the resource corresponding to all comments.
        """
        return c.Comments(self)


class ProjectResource(BasecampResource):
    path = 'projects'


class Projects(ProjectResource):

    @base.apimethod
    def archived(self):
        url = '{0}/archived'.format(self.get_url())
        request = http.Request('GET', url, {})

        return request, parsers.parse_json


class Project(ProjectResource):

    @base.resource(acc.Accesses)
    def accesses(self):
        """
        Return the resource corresponding to all project accesses.
        """
        return acc.Accesses(self)

    @base.resource(acc.Access)
    def access(self, access_id):
        """
        Return the resource corresponding to a single access.
        """
        return acc.Access(self, access_id)

    @base.resource(ev.Events)
    def events(self):
        """
        Return the resource corresponding to all events.
        """
        return ev.Events(self)

    @base.resource(ProjectTopics)
    def topics(self):
        """
        Return the resource corresponding to all project topics.
        """
        return ProjectTopics(self)

    @base.resource(Messages)
    def messages(self):
        """
        Return the resource corresponding to all project messages.
        """
        return Messages(self)

    @base.resource(Message)
    def message(self, message_id):
        """
        Return the resource corresponding to a single message.
        """
        return Message(self, message_id)

    @base.resource(c.Comment)
    def comment(self, comment_id):
        """
        Return the resource corresponding to a single comment.
        """
        return c.Comment(self, comment_id)

    @base.resource(tdl.Todolists)
    def todolists(self):
        """
        Return the resource corresponding to all todolists.
        """
        return tdl.Todolists(self)

    @base.resource(tdl.Todolist)
    def todolist(self, todolist_id):
        """
        Return the resource corresponding to a single todolist.
        """
        return tdl.Todolist(self, todolist_id)

    @base.resource(tdl.Todo)
    def todo(self, todo_id):
        """
        Return the resource corresponding to a single todo.
        """
        return tdl.Todo(self, todo_id)

    @base.resource(doc.Documents)
    def documents(self):
        """
        Return the resource corresponding to all documents.
        """
        return doc.Documents(self)

    @base.resource(doc.Document)
    def document(self, document_id):
        """
        Return the resource corresponding to a single document.
        """
        return doc.Document(self, document_id)

    @base.resource(u.Uploads)
    def uploads(self):
        """
        Return the resource corresponding to all uploads.
        """
        return u.Uploads(self)

    @base.resource(u.Upload)
    def upload(self, upload_id):
        """
        Return the resource corresponding to a single upload.
        """
        return u.Upload(self, upload_id)

    @base.resource(Attachments)
    def attachments(self):
        """
        Return the resource corresponding to all attachments.
        """
        return Attachments(self)

    @base.resource(calendars.CalendarEvents)
    def calendar_events(self):
        """
        Return the resource corresponding to all calendar events.
        """
        return calendars.CalendarEvents(self)

    @base.resource(calendars.CalendarEvent)
    def calendar_event(self, calendar_event_id):
        """
        Return the resource corresponding to a single calendar event.
        """
        return calendars.CalendarEvent(self, calendar_event_id)
