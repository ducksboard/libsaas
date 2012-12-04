from libsaas import port
from . import resource


class Credits(resource.PingdomGETResource):

    path = 'credits'

port.method_func(Credits, 'get').__doc__ = """
Returns information about remaining checks, SMS credits and
SMS auto-refill status.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceCredits')
