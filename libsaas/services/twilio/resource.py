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


def get_params(param_names, param_store, serialize_param=base.serialize_param,
               translate_param=translate_inequality):
    """
    Return the dictionary of params using by default translate_inequality
    as translation function
    """
    return base.get_params(param_names, param_store, serialize_param,
                           translate_param)


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
