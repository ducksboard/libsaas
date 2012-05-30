from libsaas import http, parsers
from libsaas.services import base

from . import resource, labels


class Issues(resource.GitHubResource):

    path = 'issues'

    @base.apimethod
    def get(self, filter='assigned', state='open', labels=None,
            sort='created', direction='desc', since=None, format=None,
            page=None, per_page=None):
        """
        Fetch the authenticated user's issues based on the filter parameters,
        and using the specified format.

        For details on the meanings and allowed values for each parameter, see
        http://developer.github.com/v3/issues/#list-issues.
        """
        url = self.get_url()
        params = base.get_params(
            ('filter', 'state', 'labels', 'sort', 'direction',
             'since', 'page', 'per_page'), locals())

        headers = resource.mimetype_accept(format)

        return http.Request('GET', url, params, headers), parsers.parse_json


class IssueCommentsBase(resource.GitHubResource):

    path = 'comments'

    def wrap_object(self, obj):
        return {'body': obj}


class IssueComments(IssueCommentsBase):
    pass


class IssueComment(IssueCommentsBase):
    pass


class RepoIssuesBase(resource.GitHubResource):

    path = 'issues'


class IssueEventsBase(resource.GitHubResource):

    path = 'events'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class IssueEvent(IssueEventsBase):
    pass


class IssueEvents(IssueEventsBase):
    pass


class RepoIssue(RepoIssuesBase):

    @base.resource(IssueComment)
    def comment(self, comment_id):
        """
        Return the resource corresponding to a single comment of this issue.

        When updating comments, use a simple string as the parameter to
        `update`, you don't have to use `{"body": <comment body>}`.
        """
        return IssueComment(self, comment_id)

    @base.resource(IssueComments)
    def comments(self):
        """
        Return the resource corresponding to the comments of this issue.

        When creating comments, use a simple string as the parameter to
        `create`, you don't have to use `{"body": <comment body>}`.
        """
        return IssueComments(self)

    @base.resource(IssueEvent)
    def event(self, event_id):
        """
        Return the resource corresponding to a single event of this issue.
        """
        return IssueEvent(self, event_id)

    @base.resource(IssueEvents)
    def events(self):
        """
        Return the resource corresponding to all the events of this issue.
        """
        return IssueEvents(self)

    @base.resource(labels.IssueLabel)
    def label(self, name):
        """
        Return the resource corresponding to a single label of this issue.
        """
        return labels.IssueLabel(self, name)

    @base.resource(labels.IssueLabels)
    def labels(self):
        """
        Return the resource corresponding to all labels of this issue.
        """
        return labels.IssueLabels(self)


class RepoIssues(RepoIssuesBase):

    @base.apimethod
    def get(self, milestone=None, state='open', assignee=None, mentioned=None,
            labels=None, sort='created', direction='desc', since=None):
        """
        Fetch issues for this repository based on the filter parameters and
        using the specified format.

        For details on the meanings and allowed values for each parameter, see
        http://developer.github.com/v3/issues/#list-issues-for-a-repository
        """
        url = self.get_url()
        params = base.get_params(
            ('milestone', 'state', 'assignee', 'mentioned', 'labels', 'sort',
             'direction', 'since', 'page', 'per_page'), locals())

        headers = resource.mimetype_accept(format)

        return http.Request('GET', url, params, headers), parsers.parse_json

    @base.resource(IssueEvents)
    def events(self):
        """
        Return the resource corresponding to all events of this repo's issues.
        """
        return IssueEvents(self)
