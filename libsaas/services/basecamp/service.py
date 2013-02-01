import json

from libsaas import http
from libsaas.filters import auth
from libsaas.services import base

from .attachments import GlobalAttachments
from .documents import GlobalDocuments
from .topics import Topics
from .events import Events
from . import todolists as tdl
from . import calendars as c
from . import projects as p
from . import people as pp


class Basecamp(base.Resource):
    def __init__(self, account_id, token_or_username, password=None):
        """
        Create a Basecamp service.

        :var account_id: Your Basecamp account id.
        :vartype account_id: int

        :var token_or_username: Either an OAuth 2.0 token, or the username if
          you want to use Basic authentication.
        :vartype token_or_username: str

        :var password: Only used with the Basic authentication, leave this as
            `None` when using OAuth.
        :vartype password: str

        """
        self.apiroot = 'https://basecamp.com/{0}/api/v1'

        self.add_filter(self.use_json)

        if password is None:
            self.access_token = token_or_username
            self.add_filter(self.add_authorization)
        else:
            self.add_filter(auth.BasicAuth(token_or_username, password))

        self.account_id = account_id

    def add_authorization(self, request):
        header = 'Bearer {0}'.format(self.access_token)
        request.headers['Authorization'] = header

    def use_json(self, request):
        request.uri += '.json'
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.headers['Content-Type'] = 'application/json; charset=utf-8'
            request.params = json.dumps(request.params)

    def get_url(self):
        return self.apiroot.format(self.account_id)

    def set_access_token(self, access_token):
        self.access_token = access_token

    def set_account_id(self, account_id):
        self.account_id = account_id

    @base.resource(p.Projects)
    def projects(self):
        """
        Return the resource corresponding to all projects.
        """
        return p.Projects(self)

    @base.resource(p.Project)
    def project(self, project_id):
        """
        Return the resource corresponding to a single project.
        """
        return p.Project(self, project_id)

    @base.resource(pp.People)
    def people(self):
        """
        Return the resource corresponding to all people.
        """
        return pp.People(self)

    @base.resource(pp.Person, pp.CurrentPerson)
    def person(self, person_id=None):
        """
        Return the resource corresponding to a single person. If
        `person_id` is `None`, current person will be returned.
        """
        if person_id is None:
            return pp.CurrentPerson(self)

        return pp.Person(self, person_id)

    @base.resource(Events)
    def events(self):
        """
        Return the resource corresponding to all events.
        """
        return Events(self)

    @base.resource(c.Calendars)
    def calendars(self):
        """
        Return the resource corresponding to all calendars.
        """
        return c.Calendars(self)

    @base.resource(c.Calendar)
    def calendar(self, calendar_id):
        """
        Return the resource corresponding to a single calendar.
        """
        return c.Calendar(self, calendar_id)

    @base.resource(Topics)
    def topics(self):
        """
        Return the resource corresponding to all topics.
        """
        return Topics(self)

    @base.resource(tdl.GlobalTodolists)
    def todolists(self):
        """
        Return the resource corresponding to all todolists.
        """
        return tdl.GlobalTodolists(self)

    @base.resource(GlobalDocuments)
    def documents(self):
        """
        Return the resource corresponding to all documents.
        """
        return GlobalDocuments(self)

    @base.resource(GlobalAttachments)
    def attachments(self):
        """
        Return the resource corresponding to all attachments.
        """
        return GlobalAttachments(self)
