from libsaas import http, parsers, port
from libsaas.services import base
from . import analysis, results, summary


class ChecksBase(base.RESTResource):

    path = 'checks'


class Checks(ChecksBase):

    def require_item(self):
        pass

    @base.apimethod
    def get(self, limit=None, offset=None):
        """
        Returns a list overview of all checks.

        Upstream documentation: {0}
        """

        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    get.__doc__ = get.__doc__.format(
        'https://www.pingdom.com/services/api-documentation-rest/'
        '#ResourceChecks')


port.method_func(Checks, 'create').__doc__ = """
Creates a new check with settings specified by provided parameters.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodCreate+New+Check')


port.method_func(Checks, 'update').__doc__ = """
Pause or change resolution for multiple checks in one bulk call.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodModify+Multiple+Checks')

port.method_func(Checks, 'delete').__doc__ = """
Deletes a list of checks. You will lose all collected data.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodDelete+Multiple+Checks')


class Check(ChecksBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(analysis.Analysis)
    def analysis(self):
        """
        Return the resource corresponding to the analysis for the check.
        """
        return analysis.Analysis(self.parent, self.object_id)

    @base.resource(results.Results)
    def results(self):
        """
        Return the resource corresponding to the results for the check.
        """
        return results.Results(self.parent, self.object_id)

    @base.resource(summary.Summary)
    def summary(self):
        """
        Return the resource corresponding to the summary for the check.
        """
        return summary.Summary(self.parent, self.object_id)


port.method_func(Check, 'get').__doc__ = """
Returns a detailed description of a specified check.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodGet+Detailed+Check+Information')

port.method_func(Check, 'update').__doc__ = """
Modify settings for a check. The provided settings will overwrite previous
values. Settings not provided will stay the same as before the update. To
clear an existing value, provide an empty value. Please note that you cannot
change the type of a check once it has been created.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           'MethodModify+Check')

port.method_func(Check, 'delete').__doc__ = """
Deletes a check. You will lose all collected data.

Upstream documentation: {0}
""".format('https://www.pingdom.com/services/api-documentation-rest/'
           '#MethodDelete+Check')
