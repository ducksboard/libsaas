from libsaas import http, parsers
from libsaas.services import base


def translate_param(val):
    return val.rstrip('_')


class PingdomGETResource(base.RESTResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self):
        return http.Request('GET', self.get_url()), parsers.parse_json
