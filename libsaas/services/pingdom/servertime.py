from libsaas import port
from libsaas.services import base
from . import resource


class Servertime(resource.PingdomGETResource):

    path = 'servertime'

    # redefine methods to set docstring later

    @base.mark_apimethod
    def get(self):
        return super(Servertime, self).get()


port.method_func(Servertime, 'get').__doc__ = """
Get the current time of the API server.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceServertime')
