from libsaas import http, parsers
from libsaas.services import base


class FilesResource(base.RESTResource):

    path = 'files'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Files(FilesResource):

    @base.apimethod
    def get(self, start=None, limit=None):
        """
        Returns data about all files.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Files
        """
        params = base.get_params(None, locals())
        return http.Request('GET', self.get_url(), params), parsers.parse_json


class File(FilesResource):
    pass
