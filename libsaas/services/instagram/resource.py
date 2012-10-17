from libsaas.services import base


class InstagramResource(base.RESTResource):

    pass


class ReadonlyResource(InstagramResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
