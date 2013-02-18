from libsaas.services import base
from libsaas import http, parsers


class Link(base.Resource):
    path = 'link'

    def __init__(self, parent, link):
        self.parent = parent
        self.object_id = link

    def get_url(self):
        return '{0}/{1}'.format(self.parent.get_url(), self.path)

    def _get(self, path, params):
        params['link'] = self.object_id

        url = '{0}/{1}'.format(self.get_url(), path)
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def info(self):
        """
        Returns metadata about a single bitly link.
        """
        return self._get('info', {})

    @base.apimethod
    def content(self, content_type=None):
        """
        Returns the "main article" from the linked page,
        as determined by the content extractor, in either HTML
        or plain text format.

        :var content_type: specifies whether to return the content
            as html or plain text. if` not indicated, defaults to 'html'.
        :vartype content_type: str
        """
        params = base.get_params(None, locals())
        return self._get('content', params)

    @base.apimethod
    def category(self):
        """
        Returns the detected categories for a document,
        in descending order of confidence.
        """
        return self._get('category', {})

    @base.apimethod
    def social(self):
        """
        Returns the "social score" for a specified bitly link.
        """
        return self._get('social', {})

    @base.apimethod
    def location(self):
        """
        Returns the significant locations for the bitly link
        or None if locations do not exist.
        """
        return self._get('location', {})

    @base.apimethod
    def language(self):
        """
        Returns the significant languages for the bitly link.
        """
        return self._get('language', {})

    @base.apimethod
    def clicks(self, unit=None, units=None, timezone=None,
               rollup=None, limit=None, unit_reference_ts=None):
        """
        Returns the number of clicks on a single bitly link.

        :var unit: timspan: minute, hour, day, week or month.
            When unit is minute the maximum value for units is 60.
            if` not indicated, defaults to day.
        :vartype unit: str

        :var units: an integer representing the time units to query data for.
            If -1 is passed, it will return all units of time.
        :vartype units: int

        :var timezone: an integer hour offset from UTC (-14..14) or a timezone
            string. If not indicated, defaults to America/New_York.
        :vartype timezone: str

        :var rollup: returns data for multiple units rolled up to a single
            result instead of a separate value for each period of time.
        :vartype rollup: bool

        :var limit: the number of rows it will return. Default is 100.
        :vartype limit: int

        :var unit_reference_ts: an epoch timestamp, indicating the most recent
            time for which to pull metrics.
            If not indicated, it defaults to now.
        :vartype unit_reference_ts: int
        """
        params = base.get_params(None, locals())
        return self._get('clicks', params)

    @base.apimethod
    def countries(self, unit=None, units=None, timezone=None,
                  limit=None, unit_reference_ts=None):
        """
        Returns metrics about the countries referring click traffic
        to a single bitly link.

        :var unit: timspan: minute, hour, day, week or month.
            When unit is minute the maximum value for units is 60.
            if` not indicated, defaults to day.
        :vartype unit: str

        :var units: an integer representing the time units to query data for.
            If -1 is passed, it will return all units of time.
        :vartype units: int

        :var timezone: an integer hour offset from UTC (-14..14) or a timezone
            string. If not indicated, defaults to America/New_York.
        :vartype timezone: str

        :var limit: the number of rows it will return. Default is 100.
        :vartype limit: int

        :var unit_reference_ts: an epoch timestamp, indicating the most recent
            time for which to pull metrics.
            If not indicated, it defaults to now.
        :vartype unit_reference_ts: int
        """
        params = base.get_params(None, locals())
        return self._get('countries', params)

    @base.apimethod
    def encoders_count(self):
        """
        Returns the number of users who have shortened a single bitly link.
        """
        return self._get('encoders_count', {})

    @base.apimethod
    def referrers(self, unit=None, units=None, timezone=None,
                  limit=None, unit_reference_ts=None):
        """
        Returns metrics about the pages referring click traffic
        to a single bitly link.

        :var unit: timspan: minute, hour, day, week or month.
            When unit is minute the maximum value for units is 60.
            if` not indicated, defaults to day.
        :vartype unit: str

        :var units: an integer representing the time units to query data for.
            If -1 is passed, it will return all units of time.
        :vartype units: int

        :var timezone: an integer hour offset from UTC (-14..14) or a timezone
            string. If not indicated, defaults to America/New_York.
        :vartype timezone: str

        :var limit: the number of rows it will return. Default is 100.
        :vartype limit: int

        :var unit_reference_ts: an epoch timestamp, indicating the most recent
            time for which to pull metrics.
            If not indicated, it defaults to now.
        :vartype unit_reference_ts: int
        """
        params = base.get_params(None, locals())
        return self._get('referrers', params)

    @base.apimethod
    def referrers_by_domain(self, unit=None, units=None, timezone=None,
                            limit=None, unit_reference_ts=None):
        """
        Returns metrics about the pages referring click traffic
        to a single bitly link, grouped by referring domain.

        :var unit: timspan: minute, hour, day, week or month.
            When unit is minute the maximum value for units is 60.
            if` not indicated, defaults to day.
        :vartype unit: str

        :var units: an integer representing the time units to query data for.
            If -1 is passed, it will return all units of time.
        :vartype units: int

        :var timezone: an integer hour offset from UTC (-14..14) or a timezone
            string. If not indicated, defaults to America/New_York.
        :vartype timezone: str

        :var limit: the number of rows it will return. Default is 100.
        :vartype limit: int

        :var unit_reference_ts: an epoch timestamp, indicating the most recent
            time for which to pull metrics.
            If not indicated, it defaults to now.
        :vartype unit_reference_ts: int
        """
        params = base.get_params(None, locals())
        return self._get('referrers_by_domain', params)

    @base.apimethod
    def referring_domains(self, unit=None, units=None, timezone=None,
                          limit=None, unit_reference_ts=None):
        """
        Returns metrics about the domains referring click traffic
        to a single bitly link.

        :var unit: timspan: minute, hour, day, week or month.
            When unit is minute the maximum value for units is 60.
            if` not indicated, defaults to day.
        :vartype unit: str

        :var units: an integer representing the time units to query data for.
            If -1 is passed, it will return all units of time.
        :vartype units: int

        :var timezone: an integer hour offset from UTC (-14..14) or a timezone
            string. If not indicated, defaults to America/New_York.
        :vartype timezone: str

        :var limit: the number of rows it will return. Default is 100.
        :vartype limit: int

        :var unit_reference_ts: an epoch timestamp, indicating the most recent
            time for which to pull metrics.
            If not indicated, it defaults to now.
        :vartype unit_reference_ts: int
        """
        params = base.get_params(None, locals())
        return self._get('referring_domains', params)

    @base.apimethod
    def shares(self, unit=None, units=None, timezone=None,
               rollup=None, limit=None, unit_reference_ts=None):
        """
        Returns metrics about a shares of a single link.

        :var unit: timspan: minute, hour, day, week or month.
            When unit is minute the maximum value for units is 60.
            if` not indicated, defaults to day.
        :vartype unit: str

        :var units: an integer representing the time units to query data for.
            If -1 is passed, it will return all units of time.
        :vartype units: int

        :var timezone: an integer hour offset from UTC (-14..14) or a timezone
            string. If not indicated, defaults to America/New_York.
        :vartype timezone: str

        :var rollup: returns data for multiple units rolled up to a single
            result instead of a separate value for each period of time.
        :vartype rollup: bool

        :var limit: the number of rows it will return. Default is 100.
        :vartype limit: int

        :var unit_reference_ts: an epoch timestamp, indicating the most recent
            time for which to pull metrics.
            If not indicated, it defaults to now.
        :vartype unit_reference_ts: int
        """
        params = base.get_params(None, locals())
        return self._get('shares', params)

