from libsaas import port
from . import resource


class Reference(resource.PingdomGETResource):

    path = 'reference'


port.method_func(Reference, 'get').__doc__ = """
Get a reference of regions, timezones and date/time/number formats
and their identifiers.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#ResourceReference')
