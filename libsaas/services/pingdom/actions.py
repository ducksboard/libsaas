from libsaas import http, parsers
from libsaas.services import base
from . import resource


class Actions(resource.PingdomGETResource):

    path = 'actions'

    @base.apimethod
    def get(self, from_=None, to=None, limit=None, offset=None, checkids=None,
            contactids=None, status=None, via=None):
        """
        Returns a list of actions (alerts) that have been generated for
        your account.

        Upstream documentation: {0}
        """

        params = base.get_params(None, locals(),
                                 translate_param=resource.translate_param)

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    get.__doc__ = get.__doc__.format(
        'https://www.pingdom.com/services/api-documentation-rest/'
        '#ResourceActions')
