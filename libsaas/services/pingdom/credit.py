from libsaas import port
from libsaas.services import base
from . import resource


class Credits(resource.PingdomGETResource):

    path = 'credits'

    # redefine methods to set docstring later

    @base.mark_apimethod
    def get(self):
        return super(Credits, self).get()


port.method_func(Credits, 'get').__doc__ = """
Returns information about remaining checks, SMS credits and
SMS auto-refill status.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceCredits')
