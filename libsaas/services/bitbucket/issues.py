from libsaas import http, parsers
from libsaas.services import base

from . import resource, followers


class IssueComponentsBase(resource.BitBucketResource):

    path = 'components'


class IssueComponents(IssueComponentsBase):
    pass


class IssueComponent(IssueComponentsBase):
    pass


class IssueCommentsBase(resource.BitBucketResource):

    path = 'comments'


class IssueComments(IssueCommentsBase):
    pass


class IssueComment(IssueCommentsBase):
    pass


class IssueMilestonesBase(resource.BitBucketResource):

    path = 'milestones'


class IssueMilestone(IssueMilestonesBase):
    pass


class IssueMilestones(IssueMilestonesBase):
    pass


class IssueVersionsBase(resource.BitBucketResource):

    path = 'versions'


class IssueVersion(IssueVersionsBase):
    pass


class IssueVersions(IssueVersionsBase):
    pass


class RepoIssuesBase(resource.BitBucketResource):

    path = 'issues'


class RepoIssue(RepoIssuesBase):

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

    @base.resource(followers.IssueFollowers)
    def followers(self):
        """
        Return the resource corresponding to the followers of this issue.
        """
        return followers.IssueFollowers(self)


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
    def filter(self, **kwargs):
        """
        Search through the issues applying filters.

        Look at https://confluence.atlassian.com/display/BITBUCKET/Issues
        to get a complete list of possible filters
        """
        def symbol(lenght):
            return '&' if lenght else '?'

        query = ''
        for key, value in kwargs.iteritems():
            if type(value) is tuple:
                # Each element is treated as OR
                for element in value:
                    query += '{0}{1}={2}'.format(
                                            symbol(len(query)), key, element)
            elif type(value) is str:
                query += '{0}{1}={2}'.format(symbol(len(query)), key, value)

        url = '{0}{1}'.format(self.get_url(), query)

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
                trivial
                minor
                major
                critical
                blocker
            status: The status of the issue. Val statuses are:
                new
                open
                resolved
                on hold
                invalid
                duplicate
                wontfix
            kind: The kinf of the issue. Valid kinds are:
                bug<
                enhancement
                proposal
                task
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
