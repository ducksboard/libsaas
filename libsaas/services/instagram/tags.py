from libsaas import http, parsers
from libsaas.services import base

from . import resource, media


class TagBase(resource.ReadonlyResource):

    path = 'tags'


class Tags(TagBase):

    path = 'tags/search'

    @base.apimethod
    def get(self, query):
        """
        fetch all tags by name.

        :var query: A valid tag name without a leading #. (eg. snow, nofilter).
        :vartype query: str
        """
        params = {'q': query}
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class Tag(TagBase):

    @base.resource(media.RecentMedia)
    def recent_media(self):
        """
        Return the resource corresponding to all recent media for the tag.
        """
        return media.RecentMedia(self)
