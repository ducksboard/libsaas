from libsaas import http, parsers
from libsaas.services import base


class TextAd(base.HierarchicalResource):

    path = 'gdn/textads'

    @base.apimethod
    def publishers(self, offset=None, page_size=None, min_times_seen=None,
                   max_times_seen=None, first_seen_before=None,
                   first_seen_after=None, last_seen_before=None,
                   last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network publishers for this ad.

        Upstream documentation: http://mixrank.com/api/documentation#textad_publishers
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/publishers'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def destinations(self, offset=None, page_size=None, min_avg_position=None,
                     max_avg_position=None, min_times_seen=None,
                     max_times_seen=None, first_seen_before=None,
                     first_seen_after=None, last_seen_before=None,
                     last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network destinations for this ad.

        Upstream documentation: http://mixrank.com/api/documentation#textad_destinations
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/destinations'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json


class DisplayAd(base.HierarchicalResource):

    path = 'gdn/displayads'

    @base.apimethod
    def publishers(self, offset=None, page_size=None, min_times_seen=None,
                   max_times_seen=None, first_seen_before=None,
                   first_seen_after=None, last_seen_before=None,
                   last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network publishers for this ad.

        Upstream documentation: http://mixrank.com/api/documentation#displayad_publishers
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/publishers'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def destinations(self, offset=None, page_size=None, min_times_seen=None,
                     max_times_seen=None, first_seen_before=None,
                     first_seen_after=None, last_seen_before=None,
                     last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network destinations for this ad.

        Upstream documentation: http://mixrank.com/api/documentation#displayad_destinations
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/destinations'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json
