import re

from libsaas import http, parsers
from libsaas.services import base


def translate_inequality(param_name):
    """
    Replace GT or LT at the end of a param name by '>' or '<' to
    achieve Twilio-like inequalities.
    """
    for suffix, replacement in (('GT', '>'), ('LT', '<')):
        if param_name.endswith(suffix):
            return param_name[:-len(suffix)] + replacement

    return param_name


def get_params(param_names, param_store, translate_param=translate_inequality,
               serialize_param=base.serialize_param):
    """
    Return a dictionary suitable to be used as params in a libsaas.http.Request
    object.

    Arguments are a tuple of parameter names, a dictionary mapping those names
    to parameter values and an optional custom parameter serialization
    function. This is useful for constructs like

    def apifunc(self, p1, p2, p3=None):
        params = get_params(('p1', 'p2', 'p3'), locals())

    which will extract parameters from the called method's environment.

    As an additional convenience, if param_names is None, all parameters from
    the param store will be considered, except for 'self'. This allows for even
    shorter code in the common situation.

    The translation function allows changing the param name before serializing
    it. For instance, param names abused to provide inequalities, like
    'start_time<=' need such translation since 'start_time<' is not a valid
    variable name in Python. The function is expected to return the name
    to use as the query param in the URL.

    The serialization function can be used for instance when the service
    expects boolean values to be represented as '0' and '1' instead of 'true'
    and 'false' or when it accepts types that can be mapped to Python types and
    mandates a specific way of encoding them as strings.
    """
    if param_names is None:
        param_names = [name for name in param_store.keys() if name != 'self']

    return dict((translate_param(name), serialize_param(param_store[name]))
                for name in param_names if param_store.get(name) is not None)


class TwilioResource(base.RESTResource):

    @base.apimethod
    def update(self, obj):
        """
        Update this resource.

        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        :vartype obj: dict
        """
        self.require_item()
        # In most cases, Twilio uses POST for updates and ignores PUT.
        # In some others, both POST and PUT can update a resource.
        # Always use POST which will work everytime.
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json
