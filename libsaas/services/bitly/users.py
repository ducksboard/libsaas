from libsaas.services import base

from .resource import BitlyResource


class User(BitlyResource):
    path = 'user'

    @base.apimethod
    def info(self, login=None, full_name=None):
        """
        Return or update information about a user.

        :var login: the bitly login of the user whose info to look up.
            If not given, the authenticated user will be used.
        :vartype login: str

        :var full_name: set the users full name value (only available
            for the authenticated user).
        :vartype full_name: str
        """
        params = base.get_params(None, locals())
        return self._get('info', params)

    @base.apimethod
    def link_history(self, link=None, limit=None, offset=None,
                     created_before=None, created_after=None,
                     modified_after=None, expand_client_id=None,
                     archived=None, private=None, user=None):
        """
        Returns entries from a user's link history
        in reverse chronological order.

        :var link the bitly link to return metadata for (when specified,
            overrides all other options).
        :vartype login: str

        :var limit the max number of results to return.
        :vartype login: int

        :var offset the numbered result at which to start (for pagination).
        :vartype offset: int

        :var created_before timestamp as an integer unix epoch.
        :vartype created_before: int

        :var created_after timestamp as an integer unix epoch.
        :vartype created_after: int

        :var modified_after timestamp as an integer unix epoch.
        :vartype modified_after: int

        :var expand_client_id whether to provide additional information about
            encoding application.
        :vartype expand_client_id: bool

        :var archived whether to include or exclude archived
            history entries. Defaults to 'off'.
        :vartype archived: str

        :var private whether to include or exclude private
            history entries. Defaults to 'both'.
        :vartype private: str

        :var user: the user for whom to retrieve history entries
            (if different from authenticated user).
        :vartype user: str

        """
        params = base.get_params(None, locals())
        return self._get('link_history', params)

    @base.apimethod
    def network_history(self, limit=None, offset=None,
                        expand_client_id=None, expand_user=None):
        """
        Returns entries from a user's network history
        in reverse chronogical order.

        :var limit the max number of results to return.
        :vartype login: int

        :var offset the numbered result at which to start (for pagination).
        :vartype offset: int

        :var expand_client_id whether to provide additional information about
            encoding application.
        :vartype expand_client_id: bool

        :var expand_user include extra user info in response.
        :vartype expand_user: bool
        """
        params = base.get_params(None, locals())
        return self._get('network_history', params)

    @base.apimethod
    def tracking_domain_list(self):
        """
        Returns a list of tracking domains a user has configured.
        """
        params = base.get_params(None, locals())
        return self._get('tracking_domain_list', params)

    @base.apimethod
    def clicks(self, unit=None, units=None, timezone=None,
               rollup=None, limit=None, unit_reference_ts=None):
        """
        Returns the aggregate number of clicks on all of the
        authenticated user's bitly links.

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
                  rollup=None, limit=None, unit_reference_ts=None):
        """
        Returns aggregate metrics about the countries referring click traffic
        to all of the authenticated user's bitly links.

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
        return self._get('countries', params)

    @base.apimethod
    def popular_links(self, unit=None, units=None, timezone=None,
                  limit=None, unit_reference_ts=None):
        """
        Returns the authenticated user's most-clicked bitly links
        (ordered by number of clicks) in a given time period.

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
        return self._get('popular_links', params)

    @base.apimethod
    def referrers(self, unit=None, units=None, timezone=None,
                  rollup=None, limit=None, unit_reference_ts=None):
        """
        Returns aggregate metrics about the pages referring click traffic
        to all of the authenticated user's bitly links.

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
        return self._get('referrers', params)

    @base.apimethod
    def referring_domains(self, unit=None, units=None, timezone=None,
                          rollup=None, limit=None, unit_reference_ts=None):
        """
        Returns aggregate metrics about the domains referring click traffic
        to all of the authenticated user's bitly links

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
        return self._get('referring_domains', params)

    @base.apimethod
    def share_counts(self, unit=None, units=None, timezone=None,
                     rollup=None, limit=None, unit_reference_ts=None):
        """
        Returns the number of shares by the authenticated user
        in a given time period.

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
        return self._get('share_counts', params)
