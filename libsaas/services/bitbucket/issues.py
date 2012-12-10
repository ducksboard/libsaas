from libsaas import http, parsers, port
from libsaas.services import base

from . import resource


class IssueComponentsBase(resource.BitBucketResource):

    path = 'components'

    def wrap_object(self, obj):
        return {'name': obj}


class IssueComponents(IssueComponentsBase):
    pass


class IssueComponent(IssueComponentsBase):
    pass


class IssueCommentsBase(resource.BitBucketResource):

    path = 'comments'

    def wrap_object(self, obj):
        return {'content': obj}


class IssueComments(IssueCommentsBase):
    pass


class IssueComment(IssueCommentsBase):
    pass


class IssueMilestonesBase(resource.BitBucketResource):

    path = 'milestones'

    def wrap_object(self, obj):
        return {'name': obj}


class IssueMilestone(IssueMilestonesBase):
    pass


class IssueMilestones(IssueMilestonesBase):
    pass


class IssueVersionsBase(resource.BitBucketResource):

    path = 'versions'

    def wrap_object(self, obj):
        return {'name': obj}


class IssueVersion(IssueVersionsBase):
    pass


class IssueVersions(IssueVersionsBase):
    pass


class RepoIssuesBase(resource.BitBucketResource):

    path = 'issues'


class RepoIssue(RepoIssuesBase):

    @base.apimethod
    def followers(self):
        """
        Fetch the followers of this issue.
        """
        request = http.Request('GET', '{0}/followers/'.format(self.get_url()))

        return request, parsers.parse_json

    @base.resource(IssueComments)
    def comments(self):
        """
        Return the resource corresponding to the comments of this issue.
        """
        return IssueComments(self)

    @base.resource(IssueComment)
    def comment(self, comment_id):
        """
        Return the resource corresponding to a single comment of this issue.
        """
        return IssueComment(self, comment_id)


class RepoIssues(RepoIssuesBase):

    @base.apimethod
    def get(self, search=None, start=None, limit=None):
        """
        Fetch issues for this repository based on the filter parameters.
        """
        url = self.get_url()
        params = base.get_params(
            ('id', 'search', 'filter', 'start', 'limit'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def search(self, search=None):
        """
        Search through issues.

        :var search: the query string parameter.
        """
        url = self.get_url()
        params = base.get_params(('search', ), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def filter(self, filters):
        """
        Search through the issues applying filters.

        Look at https://confluence.atlassian.com/display/BITBUCKET/Issues
        to get a complete list of possible filters.

        :var filters: A dictionary of filters. Keys are strings corresponding
            to the filter names and values are ether string filter values or
            tuples, in which case their conditions are implicitly ORed. For
            example, {"title": ("~one", "~two")} would mean issues with the
            title containing either "one" or "two"
        :vartype filters: dict of str to str or tuple of str
        """
        # because http.Request needs params to be a dict of strings to strings
        # (roughly) and since BitBucket wants repeated parameters to express
        # OR, we'll do the quoting by hand ourselves
        def flatten_conditions(filters):
            for key, val in filters.items():
                if isinstance(val, (list, tuple)):
                    for v in val:
                        yield (port.to_b(key), port.to_b(v))
                else:
                    yield (port.to_b(key), port.to_b(val))

        to_encode = tuple(flatten_conditions(filters))
        qs = port.urlencode(to_encode)

        url = '{0}/?{1}'.format(self.get_url(), qs)
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def create(self, obj):
        """
        Create a new Issue.

        :var obj: a Python object with the needed params that can be:
            title: The title of the new issue
            content: The content of the new issue
            component: The componen associated with the issue
            milestone: The milestone associated with  the issue
            version: The version associated with the issue
            responsible: The username of the person responsible for the issue
            priority: The priority of the issue. Valid priorities are:

              * trivial
              * minor
              * major
              * critical
              * blocker

            status: The status of the issue. Val statuses are:

              * new
              * open
              * resolved
              * on hold
              * invalid
              * duplicate
              * wontfix

            kind: The kind of the issue. Valid kinds are:

              * bug
              * enhancement
              * proposal
              * task
        """
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.resource(IssueComponents)
    def components(self):
        """
        Return the resource corresponding to the components of this issue.
        """
        return IssueComponents(self)

    @base.resource(IssueComment)
    def component(self, component_id):
        """
        Return the resources corresponding to one component of this issue.
        """
        return IssueComponent(self, component_id)

    @base.resource(IssueMilestones)
    def milestones(self):
        """
        Return the resources corresponding to the milestones of this issue.
        """
        return IssueMilestones(self)

    @base.resource(IssueMilestone)
    def milestone(self, milestone_id):
        """
        Return the resource corresponding to one milestone of this issue.
        """
        return IssueMilestone(self, milestone_id)

    @base.resource(IssueVersions)
    def versions(self):
        """
        Return the resource corresponding to the versions of this issue.
        """
        return IssueVersions(self)

    @base.resource(IssueVersion)
    def version(self, version_id):
        """
        Return the resource corresponding to one version of this issue.
        """
        return IssueVersion(self, version_id)
