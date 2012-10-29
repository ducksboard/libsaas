from libsaas import http, parsers
from libsaas.services import base

from . import ads


class Advertiser(base.HierarchicalResource):

    path = 'advertisers'

    @base.resource(ads.TextAd)
    def textad(self, hash):
        """
        Return a resource corresponding to a single text ad.

        :var hash: A unique hash identifying this ad.
        :vartype hash: str
        """
        return ads.TextAd(self, hash)

    @base.resource(ads.DisplayAd)
    def displayad(self, hash):
        """
        Return a resource corresponding to a single display ad.

        :var hash: A unique hash identifying this ad.
        :vartype hash: str
        """
        return ads.DisplayAd(self, hash)

    @base.apimethod
    def summary(self):
        """
        Fetch the advertiser's summary.

        Upstream documentation: http://mixrank.com/api/documentation#advertiser
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json

    @base.apimethod
    def textads(self, offset=None, page_size=None, min_avg_position=None,
                max_avg_position=None, min_times_seen=None,
                max_times_seen=None, first_seen_before=None,
                first_seen_after=None, last_seen_before=None,
                last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network text ads for this advertiser.

        Upstream documentation: http://mixrank.com/api/documentation#advertiser_textads
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
        Fetch the Google Display Network display ads for this advertiser.

        Upstream documentation: http://mixrank.com/api/documentation#advertiser_displayads
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/gdn/displayads'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def publishers(self, offset=None, page_size=None, min_times_seen=None,
                   max_times_seen=None, min_monthly_uniques=None,
                   max_monthly_uniques=None, last_seen_before=None,
                   last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network publishers for this advertiser.

        Upstream documentation: http://mixrank.com/api/documentation#advertiser_publishers
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/gdn/publishers'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def keywords(self, offset=None, page_size=None, min_times_seen=None,
                 max_times_seen=None, first_seen_before=None,
                 first_seen_after=None, last_seen_before=None,
                 last_seen_after=None, sort_field=None, sort_order=None):
        """
        Fetch the Google Display Network keywords for this advertiser.

        Upstream documentation: http://mixrank.com/api/documentation#advertiser_keywords
        """
        params = base.get_params(None, locals())
        url = self.get_url() + '/gdn/keywords'
        request = http.Request('GET', url, params)

        return request, parsers.parse_json
