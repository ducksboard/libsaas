from libsaas.services import base

from . import resource


class ResourceMixin(object):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Groups(resource.PaginatedDeskResource, ResourceMixin):

    path = 'groups'


class Group(resource.DeskResource, ResourceMixin):

    path = 'groups'


class UsersBase(resource.DeskResource):

    path = 'users'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Users(resource.PaginatedDeskResource, ResourceMixin):

    path = 'users'


class User(resource.DeskResource, ResourceMixin):

    path = 'users'


class Account(resource.DeskResource, ResourceMixin):

    path = 'account/verify_credentials'
