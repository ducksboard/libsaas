import inspect

from libsaas import http, parsers, port
from libsaas.services import base


class Mailchimp(base.Resource):
    """
    """
    def __init__(self, api_key):
        """
        Create a Mailchimp service.

        :var api_key: The API key including the region, for instance
            `8ac789caf98879caf897a678fa76daf-us2`.
        :vartype api_key: str
        """
        self.api_key, dc = port.to_u(api_key).split('-')

        tmpl = '{0}.api.mailchimp.com/1.3/'
        self.apiroot = http.quote_any(tmpl.format(dc))
        self.apiroot = 'https://' + self.apiroot

        self.add_filter(self.add_api_root)
        self.add_filter(self.add_params)

    def add_api_root(self, request):
        request.uri = self.apiroot + request.uri

    def add_params(self, request):
        request.params.update({'output': 'json',
                               'apikey': self.api_key})

    def get_url(self, method):
        return '?method={0}'.format(method)

    def method_call(self, params):
        # a trick - get the method name from the stack frame preceding the
        # current one
        method = inspect.stack()[1][3]

        # serialize the parameters
        serialized = {}
        for name, value in params.items():
            if name == 'self':
                continue
            if value is None:
                continue
            serialized.update(http.serialize_flatten(name, value))

        request = http.Request('POST', self.get_url(method), serialized)
        return request, parsers.parse_json

    @base.apimethod
    def campaignContent(self, cid, for_archive=True):
        return self.method_call(locals())

    @base.apimethod
    def campaignCreate(self, type, options, content,
                       segment_opts={}, type_opts={}):
        return self.method_call(locals())

    @base.apimethod
    def campaignDelete(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignEcommOrderAdd(self, order):
        return self.method_call(locals())

    @base.apimethod
    def campaignPause(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignReplicate(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignResume(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignSchedule(self, cid, schedule_time, schedule_time_b=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignSegmentTest(self, list_id, options={}):
        return self.method_call(locals())

    @base.apimethod
    def campaignSendNow(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignSendTest(self, cid, test_emails=[], send_type=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignShareReport(self, cid, opts={}):
        return self.method_call(locals())

    @base.apimethod
    def campaignTemplateContent(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignUnschedule(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignUpdate(self, cid, name, value):
        return self.method_call(locals())

    @base.apimethod
    def campaigns(self, filters={}, start=None, limit=None):
        return self.method_call(locals())

    # XXX params order
    @base.apimethod
    def campaignAbuseReports(self, cid, since=None, start=None, limit=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignAdvice(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignAnalytics(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignBounceMessage(self, cid, email):
        return self.method_call(locals())

    @base.apimethod
    def campaignBounceMessages(self, cid, start=None, limit=None, since=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignClickStats(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignEcommOrders(self, cid, start=None, limit=None, since=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignEepUrlStats(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignGeoOpens(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignGeoOpensForCountry(self, cid, code):
        return self.method_call(locals())

    @base.apimethod
    def campaignMembers(self, cid, status=None, start=None, limit=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignStats(self, cid):
        return self.method_call(locals())

    @base.apimethod
    def campaignUnsubscribes(self, cid, start=None, limit=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignClickDetailAIM(self, cid, url, start=None, limit=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignEmailStatsAIM(self, cid, email_address=[]):
        return self.method_call(locals())

    @base.apimethod
    def campaignNotOpenedAIM(self, cid, start=None, limit=None):
        return self.method_call(locals())

    @base.apimethod
    def campaignOpenedAIM(self, cid, start=None, limit=None):
        return self.method_call(locals())

    @base.apimethod
    def ecommOrderAdd(self, order={}):
        return self.method_call(locals())

    @base.apimethod
    def ecommOrderDel(self, store_id, order_id):
        return self.method_call(locals())

    @base.apimethod
    def ecommOrders(self, start=None, limit=None, since=None):
        return self.method_call(locals())

    @base.apimethod
    def folderAdd(self, name, type=None):
        return self.method_call(locals())

    # XXX is type actually used?
    @base.apimethod
    def folderDel(self, fid, type=None):
        return self.method_call(locals())

    @base.apimethod
    def folderUpdate(self, fid, name, type=None):
        return self.method_call(locals())

    @base.apimethod
    def folders(self, type=None):
        return self.method_call(locals())

    @base.apimethod
    def gmonkeyActivity(self):
        return self.method_call(locals())

    @base.apimethod
    def gmonkeyAdd(self, cid, id, email_address=[]):
        return self.method_call(locals())

    @base.apimethod
    def gmonkeyDel(self, cid, id, email_address=[]):
        return self.method_call(locals())

    @base.apimethod
    def gmonkeyMembers(self):
        return self.method_call(locals())

    @base.apimethod
    def campaignsForEmail(self, email_address, options={}):
        return self.method_call(locals())

    @base.apimethod
    def chimpChatter(self):
        return self.method_call(locals())

    @base.apimethod
    def generateText(self, type, content):
        return self.method_call(locals())

    @base.apimethod
    def getAccountDetails(self):
        return self.method_call(locals())

    @base.apimethod
    def inlineCss(self, html, strip_css=False):
        return self.method_call(locals())

    @base.apimethod
    def listsForEmail(self, email_address):
        return self.method_call(locals())

    @base.apimethod
    def ping(self, cid, email_address=[]):
        return self.method_call(locals())

    @base.apimethod
    def listAbuseReports(self, id, start=None, limit=None, since=None):
        return self.method_call(locals())

    @base.apimethod
    def listActivity(self, id):
        return self.method_call(locals())

    @base.apimethod
    def listBatchSubscribe(self, id, batch=[], double_optin=True,
                           update_existing=False, replace_interests=True):
        return self.method_call(locals())

    @base.apimethod
    def listBatchUnsubscribe(self, id, emails=[], delete_member=False,
                           send_goodbye=True, send_notify=False):
        return self.method_call(locals())

    @base.apimethod
    def listClients(self, id):
        return self.method_call(locals())

    @base.apimethod
    def listGrowthHistory(self, id):
        return self.method_call(locals())

    @base.apimethod
    def listInterestGroupAdd(self, id, group_name, grouping_id=None):
        return self.method_call(locals())

    @base.apimethod
    def listInterestGroupDel(self, id, group_name, grouping_id=None):
        return self.method_call(locals())

    @base.apimethod
    def listInterestGroupUpdate(self, id, old_name, new_name,
                                grouping_id=None):
        return self.method_call(locals())

    @base.apimethod
    def listInterestGroupingAdd(self, id, name, type, groups=[]):
        return self.method_call(locals())

    @base.apimethod
    def listInterestGroupingDel(self, grouping_id):
        return self.method_call(locals())

    @base.apimethod
    def listInterestGroupingUpdate(self, grouping_id, name, value):
        return self.method_call(locals())

    @base.apimethod
    def listInterestGroupings(self, id):
        return self.method_call(locals())

    @base.apimethod
    def listLocations(self, id):
        return self.method_call(locals())

    @base.apimethod
    def listMemberActivity(self, id, email_address=[]):
        return self.method_call(locals())

    @base.apimethod
    def listMemberInfo(self, id, email_address=[]):
        return self.method_call(locals())

    # XXX params order
    @base.apimethod
    def listMembers(self, id, status='subscribed',
                    since=None, start=None, limit=None):
        return self.method_call(locals())

    @base.apimethod
    def listMergeVarAdd(self, id, tag, name, options={}):
        return self.method_call(locals())

    @base.apimethod
    def listMergeVarDel(self, id, tag):
        return self.method_call(locals())

    @base.apimethod
    def listMergeVarUpdate(self, id, tag, options={}):
        return self.method_call(locals())

    @base.apimethod
    def listMergeVars(self, id):
        return self.method_call(locals())

    @base.apimethod
    def listStaticSegmentAdd(self, id, name):
        return self.method_call(locals())

    @base.apimethod
    def listStaticSegmentDel(self, id, seg_id):
        return self.method_call(locals())

    @base.apimethod
    def listStaticSegmentMembersAdd(self, id, seg_id, batch=[]):
        return self.method_call(locals())

    @base.apimethod
    def listStaticSegmentMembersDel(self, id, seg_id, batch=[]):
        return self.method_call(locals())

    @base.apimethod
    def listStaticSegmentReset(self, id, seg_id):
        return self.method_call(locals())

    @base.apimethod
    def listStaticSegments(self, id):
        return self.method_call(locals())

    @base.apimethod
    def listSubscribe(self, id, email_address, merge_vars={},
                      email_type='html', double_optin=True,
                      update_existing=False,
                      replace_interests=True, send_welcome=False):
        return self.method_call(locals())

    @base.apimethod
    def listUnsubscribe(self, id, email_address, delete_member=False,
                        send_goodbye=True, send_notify=True):
        return self.method_call(locals())

    @base.apimethod
    def listUpdateMember(self, id, email_address, merge_vars={},
                         email_type=None, replace_interests=True):
        return self.method_call(locals())

    @base.apimethod
    def listWebhookAdd(self, id, url, actions={}, sources={}):
        return self.method_call(locals())

    @base.apimethod
    def listWebhookDel(self, id, url):
        return self.method_call(locals())

    @base.apimethod
    def listWebhooks(self, id):
        return self.method_call(locals())

    @base.apimethod
    def lists(self, filters={}, start=None, limit=None):
        return self.method_call(locals())

    @base.apimethod
    def apikeyAdd(self, username, password):
        return self.method_call(locals())

    @base.apimethod
    def apikeyExpire(self, username, password):
        return self.method_call(locals())

    @base.apimethod
    def apikeys(self, username, password, apikey, expired=False):
        return self.method_call(locals())

    @base.apimethod
    def templateAdd(self, name, html):
        return self.method_call(locals())

    @base.apimethod
    def templateDel(self, id):
        return self.method_call(locals())

    # XXX tid vs id?
    @base.apimethod
    def templateInfo(self, tid, type='user'):
        return self.method_call(locals())

    @base.apimethod
    def templateUndel(self, id):
        return self.method_call(locals())

    @base.apimethod
    def templateUpdate(self, id, values={}):
        return self.method_call(locals())

    @base.apimethod
    def templates(self, types=None, category=None, inactives=None):
        if types is None:
            types = {'user': True, 'gallery': False, 'base': False}
        if inactives is None:
            inactives = {'include': False, 'only': False}
        return self.method_call(locals())


def add_docstrings():
    for method_name in Mailchimp.list_methods():
        function = port.method_func(Mailchimp, method_name)
        # set the docstring
        function.__doc__ = """
Call Mailchimp's {0} method.

Upstream documentation: http://apidocs.mailchimp.com/api/rtfm/{1}.func.php
""".format(method_name, method_name.lower())


add_docstrings()
