from libsaas import port
from libsaas.services import base


class Settings(base.RESTResource):

    path = 'settings'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def require_item(self):
        pass

port.method_func(Settings, 'update').__doc__ = """
Modify account-specific settings.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodModify+Account+Settings')
