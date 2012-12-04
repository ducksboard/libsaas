from libsaas import port
from . import resource


class Servertime(resource.PingdomGETResource):

    path = 'servertime'


port.method_func(Servertime, 'get').__doc__ = """
Get the current time of the API server.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceServertime')
