from libsaas.services import base

from .resource import GoogleCalendarResource


class AclResource(GoogleCalendarResource):
    path = 'acl'


class Acls(AclResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def patch(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Acl(AclResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()
