from libsaas import http, parsers
from libsaas.services import base

from .resource import BasecampResource
from .comments import Comments


class TodoResource(BasecampResource):
    path = 'todos'


class Todos(TodoResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Todo(TodoResource):

    @base.resource(Comments)
    def comments(self):
        """
        Return the resource corresponding to all comments.
        """
        return Comments(self)


class TodolistResource(BasecampResource):
    path = 'todolists'


class Todolists(TodolistResource):

    @base.apimethod
    def completed(self):
        url = '{0}/completed'.format(self.get_url())
        request = http.Request('GET', url, {})

        return request, parsers.parse_json


class GlobalTodolists(TodolistResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


    @base.apimethod
    def completed(self):
        url = '{0}/completed'.format(self.get_url())
        request = http.Request('GET', url, {})

        return request, parsers.parse_json


class AssignedTodos(TodolistResource):
    path = 'assigned_todos'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Todolist(TodolistResource):

    @base.resource(Todos)
    def todos(self):
        """
        Return the resource corresponding to all todos.
        """
        return Todos(self)
