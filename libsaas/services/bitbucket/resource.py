from libsaas import http, parsers
from libsaas.services import base


def get_params(param_names, param_store):
    """
    Return a dictionary suitable to be used as params in a libsaas.http.Request
    object.

    Arguments are a tuple of parameters names and a dictionary mapping those
    names to parameter values. This is useful for constructs like

    def apifunc(self, p1, p2, p3=None):
        params = get_params(('p1', 'p2', 'p3'), locals())

    which will extract parameters from the called method's environment.
    """
    return dict((name, param_store[name]) for name in param_names
                if param_store.get(name) is not None)


def parse_boolean(body, code, headers):
    if code == 401 or code == 403 or code == 404:
        return False
    if code == 200 or code == 203:
        return True
    raise http.HTTPError(body, code, headers)


class BitBucketResource(base.RESTResource):

    @base.apimethod
    def get(self):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json
