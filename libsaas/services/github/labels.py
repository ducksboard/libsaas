from libsaas import http, parsers
from libsaas.services import base

from . import resource


class LabelsBase(resource.GitHubResource):

    path = 'labels'

    def get_url(self):
        if self.object_id is None:
            return '{0}/{1}'.format(self.parent.get_url(), self.path)

        return '{0}/{1}/{2}'.format(self.parent.get_url(), self.path,
                                    self.object_id)


class RepoLabel(LabelsBase):
    pass


class RepoLabels(LabelsBase):
    pass


class MilestoneLabels(LabelsBase):
    pass


class IssueLabelsBase(LabelsBase):

    @base.apimethod
    def get(self, page=None, per_page=None):
        self.require_collection()
        params = base.get_params(('page', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
    get.__doc__ = LabelsBase.get.__doc__


class IssueLabel(IssueLabelsBase):
    pass


class IssueLabels(IssueLabelsBase):

    @base.apimethod
    def replace(self, labels):
        """
        Replace all labels on this issue with new ones.

        :var labels: A list of labels to use.
        :vartype labels: list of str
        """
        request = http.Request('PUT', self.get_url(), labels)

        return request, parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Delete all labels from this issue.
        """
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_empty
