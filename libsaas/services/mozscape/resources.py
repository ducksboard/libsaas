from libsaas import parsers, http
from libsaas.services import base


class Metadata(base.Resource):

    @base.apimethod
    def last_update(self):
        """
        Fetch the Unix timestamp of the last Mozscape Index update.
        """
        request = http.Request('GET', '/metadata/last_update.json')
        return request, parsers.parse_json

    @base.apimethod
    def next_update(self):
        """
        Fetch the Unix timestamp of the next Mozscape Index update.
        """
        request = http.Request('GET', '/metadata/next_update.json')
        return request, parsers.parse_json

    @base.apimethod
    def index_stats(self):
        """
        Fetch data about the volume of information in the Mozscape Index.
        """
        request = http.Request('GET', '/metadata/index_stats')
        return request, parsers.parse_json
