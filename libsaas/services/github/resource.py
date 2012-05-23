from libsaas import http, parsers
from libsaas.services import base


def mimetype_accept(format):
    if not format:
        return {}
    mimetype = 'application/vnd.github.v3.{0}+json'.format(format)
    return {'Accept': mimetype}


def serialize_param(val):
    if isinstance(val, bool):
        return 'true' if val else 'false'
    return val


def get_params(param_names, param_store):
    """
    Return a dictionary suitable to be used as params in a libsaas.http.Request
    object.

    Arguments are a tuple of parameter names and a dictionary mapping those
    names to parameter values. This is useful for constructs like

    def apifunc(self, p1, p2, p3=None):
        params = get_params(('p1', 'p2', 'p3'), locals())

    which will extract parameters from the called method's environment.
    """
    return dict((name, serialize_param(param_store[name])) for name in param_names
                if param_store.get(name) is not None)


def parse_boolean(body, code, headers):
    # The boolean value endpoints respond with 204 if the response is true and
    # 404 if it is not.
    if code == 204:
        return True
    if code == 404:
        return False
    raise http.HTTPError(body, code, headers)


class GitHubResource(base.RESTResource):

    @base.apimethod
    def get(self, page=None, per_page=None):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.

        :var page: For collections, where should paging start. If left as
            `None`, the first page is returned.
        :vartype page: int

        :var per_page: For collections, how many objects sould be returned. The
            maximum is 100. If left as `None`, 30 objects are returned.
        :vartype per_page: int
        """
        params = get_params(('page', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        """
        self.require_item()
        # GitHub uses PATCH for updates
        request = http.Request('PATCH', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json
