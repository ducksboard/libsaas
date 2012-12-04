from libsaas import http, parsers, port
from libsaas.services import base


class ContactsBase(base.RESTResource):

    path = 'contacts'


class Contacts(ContactsBase):

    def require_item(self):
        pass

    @base.apimethod
    def get(self, limit=None, offset=None):
        """
        Returns a list of all contacts.

        Upstream documentation: {0}
        """

        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    get.__doc__ = get.__doc__.format(
        'https://www.pingdom.com/services/api-documentation-rest/'
        '#ResourceContacts')


port.method_func(Contacts, 'create').__doc__ = """
Creates a new contact with settings specified by provided parameters.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodCreate+Contact')

port.method_func(Contacts, 'update').__doc__ = """
Modifies a list of contacts.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodModify+Multiple+Contacts')

port.method_func(Contacts, 'delete').__doc__ = """
Deletes a list of contacts.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodDelete+Multiple+Contacts')


class Contact(ContactsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

port.method_func(Contact, 'update').__doc__ = """
Modify a contact.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           'MethodModify+Contact')

port.method_func(Contact, 'delete').__doc__ = """
Deletes a contact.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodDelete+Contact')
