from libsaas.filters import auth
from libsaas.services import base

from . import actions, analysis, checks, contacts, credit, probes, reference
from . import reports, results, servertime, settings, summary
from . import single, traceroute


class Pingdom(base.Resource):
    """
    """
    def __init__(self, username, password, app_key):
        """
        Create a Pingdom service.

        :var username: The username for the authenticated user.
        :vartype username: str

        :var password: The password for the authenticated user.
        :vartype password: str

        :var app_key: The app_key for the application.
        :vartype app_key: str
        """
        self.apiroot = 'https://api.pingdom.com/api/2.0'
        self.app_key = app_key

        self.add_filter(auth.BasicAuth(username, password))
        self.add_filter(self.add_app_header)

    def add_app_header(self, request):
        request.headers['App-Key'] = self.app_key

    def get_url(self):
        return self.apiroot

    @base.resource(actions.Actions)
    def actions(self):
        """
        Return the resource corresponding to all actions
        """
        return actions.Actions(self)

    @base.resource(analysis.Analysis)
    def analysis(self, checkid):
        """
        Return the resource corresponding to the analysis for specified check

        :var checkid: The check id
        :vartype checkid: str
        """
        return analysis.Analysis(self, checkid)

    @base.resource(checks.Checks)
    def check(self, checkid):
        """
        Return the resource corresponding to a single check

        :var checkid: The check id
        :vartype checkid: str
        """
        return checks.Check(self, checkid)

    @base.resource(checks.Checks)
    def checks(self):
        """
        Return the resource corresponding to all checks
        """
        return checks.Checks(self)

    @base.resource(contacts.Contacts)
    def contact(self, contactid):
        """
        Return the resource corresponding to a single contact

        :var contactid: The contact id
        :vartype contactid: str
        """
        return contacts.Contact(self, contactid)

    @base.resource(contacts.Contacts)
    def contacts(self):
        """
        Return the resource corresponding to all contacts
        """
        return contacts.Contacts(self)

    @base.resource(credit.Credits)
    def credits(self):
        """
        Return the resource corresponding to all credits
        """
        return credit.Credits(self)

    @base.resource(probes.Probes)
    def probes(self):
        """
        Return the resource corresponding to all probes
        """
        return probes.Probes(self)

    @base.resource(reference.Reference)
    def reference(self):
        """
        Return the resource corresponding to the reference of regions
        """
        return reference.Reference(self)

    @base.resource(reports.ReportsEmail)
    def reports_email(self):
        """
        Return the resource corresponding to the email reports
        """
        return reports.ReportsEmail(self)

    @base.resource(reports.ReportsEmail)
    def report_email(self, reportid):
        """
        Return the resource corresponding to a single email report

        :var reportid: The report id
        :vartype reportid: str
        """
        return reports.ReportsEmail(self, reportid)

    @base.resource(reports.ReportsPublic)
    def reports_public(self):
        """
        Return the resource corresponding to the public reports
        """
        return reports.ReportsPublic(self)

    @base.resource(reports.ReportsPublic)
    def report_public(self, reportid):
        """
        Return the resource corresponding to a single public report

        :var reportid: The report id
        :vartype reportid: str
        """
        return reports.ReportsPublic(self, reportid)

    @base.resource(reports.ReportsShared)
    def reports_shared(self):
        """
        Return the resource corresponding to the shared reports
        """
        return reports.ReportsShared(self)

    @base.resource(reports.ReportsShared)
    def report_shared(self, reportid):
        """
        Return the resource corresponding to a single shared report

        :var reportid: The report id
        :vartype reportid: str
        """
        return reports.ReportsShared(self, reportid)

    @base.resource(results.Results)
    def results(self, checkid):
        """
        Return the resource corresponding to the raw test results for
        a specified check

        :var checkid: The check id
        :vartype checkid: str
        """
        return results.Results(self, checkid)

    @base.resource(servertime.Servertime)
    def servertime(self):
        """
        Return the resource corresponding to the servertime
        """
        return servertime.Servertime(self)

    @base.resource(settings.Settings)
    def settings(self):
        """
        Return the resource corresponding to the settings
        """
        return settings.Settings(self)

    @base.resource(summary.Summary)
    def summary(self, checkid):
        """
        Return the resource corresponding to the summary for a specified check.

        :var checkid: The check id
        :vartype checkid: str
        """
        return summary.Summary(self, checkid)

    @base.resource(single.Single)
    def single(self):
        """
        Return the resource corresponding to the single test
        """
        return single.Single(self)

    @base.resource(traceroute.Traceroute)
    def traceroute(self):
        """
        Return the resource corresponding to the traceroute test
        """
        return traceroute.Traceroute(self)
