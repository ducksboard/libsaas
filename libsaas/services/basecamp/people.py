from libsaas import http, parsers
from libsaas.services import base

from .resource import BasecampResource
from .todolists import AssignedTodos
from . import events as ev


class PeopleResource(BasecampResource):
    path = 'people'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class People(PeopleResource):
    pass


class CurrentPerson(PeopleResource):

    @base.apimethod
    def get(self):
        url = '{0}/me'.format(self.get_url())
        request = http.Request('GET', url, {})

        return request, parsers.parse_json

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Person(PeopleResource):

    @base.resource(ev.Events)
    def events(self):
        """
        Return the resource corresponding to all events.
        """
        return ev.Events(self)

    @base.resource(AssignedTodos)
    def assigned_todos(self):
        """
        Return the resource corresponding to all assigned todos.
        """
        return AssignedTodos(self)
