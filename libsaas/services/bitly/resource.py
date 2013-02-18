from libsaas.services import base
from libsaas import http, parsers


class BitlyResource(base.HierarchicalResource):

    def _get(self, path, params):
        url = '{0}/{1}'.format(self.get_url(), path)
        request = http.Request('GET', url, params)
        return request, parsers.parse_json


class HighValue(BitlyResource):
    path = 'highvalue'

    @base.apimethod
    def get(self, limit):
        """
        Returns a specified number of "high-value" bitly links that
        are popular across bitly at this particular moment.

        :var limit: the maximum number of high-value links to return.
        :vartype limit: int
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class Search(BitlyResource):
    path = 'search'

    @base.apimethod
    def get(self, limit=None, offset=None, query=None, lang=None,
            cities=None, domain=None, fields=None):
        """
        Search links receiving clicks across bitly by content, language, location, and more

        :var limit: the maximum number of links to return.
        :vartype limit: int

        :var offset: which result to start with (defaults to 0).
        :vartype offset: int

        :var query: the string to query for.
        :vartype query: str

        :var lang: favor results in this language (two letter ISO code).
        :vartype lang: str

        :var cities: show links active in this city.
        :vartype cities: str

        :var domain: restrict results to this web domain.
        :vartype domain: str

        :var fields: which fields to return in the response (comma-separated).
            May be any of: domain, initial_epoch, h2, h3, site, lastindexed,
            keywords, last_indexed_epoch, title, initial, summaryText, content,
            score, summaryTitle, type, description, cities, lang, url,
            referrer, aggregate_link, lastseen, page, ogtitle aggregate_link.
            By default, all will be returned.
        :vartype fields: str
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class RealTime(BitlyResource):
    path = 'realtime'

    @base.apimethod
    def bursting_phrases(self):
        """
        Returns phrases that are receiving an uncharacteristically
        high volume of click traffic, and the individual links (hashes)
        driving traffic to pages containing these phrases.
        """
        return self._get('bursting_phrases', {})

    @base.apimethod
    def hot_phrases(self):
        """
        Returns phrases that are receiving a consistently high volume of click
        traffic, and the individual links (hashes) driving traffic to pages
        containing these phrases.
        """
        return self._get('hot_phrases', {})

    @base.apimethod
    def clickrate(self, phrase):
        """
        Returns the click rate for content containing a specified phrase.

        :var phrase: the phrase for which you'd like to get the click rate.
        :vartype phrase: str
        """
        params = base.get_params(None, locals())
        return self._get('clickrate', params)
