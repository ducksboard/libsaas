from libsaas.services import base

from . import resource


class TokensBaseResource(resource.StripeResource):

    path = 'tokens'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Token(TokensBaseResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Tokens(TokensBaseResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()
