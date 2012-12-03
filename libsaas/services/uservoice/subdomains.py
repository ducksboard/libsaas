from libsaas import http, parsers, port
from libsaas.services import base


class Subdomain(base.HierarchicalResource):

    @base.apimethod
    def get(self):
        """
        Fetch information about the subdomain.
        """
        url = '{0}/subdomains/{1}'.format(self.parent.get_url(),
                                          port.to_u(self.object_id))
        return http.Request('GET', url), parsers.parse_json
