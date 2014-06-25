from libsaas import http, parsers
from libsaas.services import base

from . import resource


class PlansBaseResource(resource.StripeResource):

    path = 'plans'


class Plan(PlansBaseResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Plans(PlansBaseResource):

    @base.apimethod
    def get(self, limit=10):
        """
        Fetch all plans.

        :var limit: A limit on the number of objects to be returned. Limit can
            range between 1 and 100 items.
        :vartype limit: int
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
