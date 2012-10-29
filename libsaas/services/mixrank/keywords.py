from libsaas import http, parsers
from libsaas.services import base


class Keyword(base.HierarchicalResource):

    path = 'keywords'

    @base.apimethod
    def summary(self):
        """
        Fetch the keyword summary.

        Upstream documentation: http://mixrank.com/api/documentation#keyword
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json

    @base.apimethod
    def advertisers(self, offset=None, page_size=None, min_times_seen=None,
                    max_times_seen=None, first_seen_before=None,
                    first_seen_after=None, last_seen_before=None,
                    last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the advertisers that show ads for this keyword.

        Upstream documentation: http://mixrank.com/api/documentation#keyword_advertisers
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/gdn/advertisers'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def textads(self, offset=None, page_size=None, min_avg_position=None,
                max_avg_position=None, min_times_seen=None,
                max_times_seen=None, first_seen_before=None,
                first_seen_after=None, last_seen_before=None,
                last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network text ads targeting this keyword.

        Upstream documentation: http://mixrank.com/api/documentation#keyword_textads
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/gdn/textads'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def displayads(self, offset=None, page_size=None, min_times_seen=None,
                   max_times_seen=None, first_seen_before=None,
                   first_seen_after=None, last_seen_before=None,
                   last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network display ads targeting at this keyword.

        Upstream documentation: http://mixrank.com/api/documentation#keyword_displayads
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/gdn/displayads'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json
