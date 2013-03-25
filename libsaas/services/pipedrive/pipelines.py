from libsaas import http, parsers
from libsaas.services import base


class StagesResource(base.RESTResource):

    path = 'stages'


class Stages(StagesResource):

    @base.apimethod
    def get(self, pipeline_id=None):
        """
        Returns data about all stages

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Stages
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple stages as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Stages
        """
        params = base.get_params(None, locals())

        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json


class Stage(StagesResource):

    @base.apimethod
    def deals(self, filter_id=None, user_id=None, everyone=None,
              start=None, limit=None):
        """
        Lists deals in a specific stage

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Stages
        """
        params = base.get_params(None, locals())
        url = '{0}/deals'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class PipelinesResource(base.RESTResource):

    path = 'pipelines'


class Pipelines(PipelinesResource):
    pass


class Pipeline(PipelinesResource):

    @base.apimethod
    def deals(self, filter_id=None, user_id=None, everyone=None,
              stage_id=None, start=None, limit=None):
        """
        Lists deals in a specific pipeline across all its stages.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Pipelines
        """
        params = base.get_params(None, locals())
        url = '{0}/deals'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def conversion_rates(self, start_date, end_date, user_id=None):
        """
        Returns all stage-to-stage conversion and pipeline-to-close
        rates for given time period.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Pipelines
        """
        params = base.get_params(None, locals())
        url = '{0}/conversion_statistics'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def movements(self, start_date, end_date, user_id=None):
        """
        Returns statistics for deals movements for given time period.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Pipelines
        """
        params = base.get_params(None, locals())
        url = '{0}/movement_statistics'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json
