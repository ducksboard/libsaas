from libsaas import http, parsers
from libsaas.services import base

from . import resource, labels


class MilestonesBase(resource.GitHubResource):

    path = 'milestones'

    def get_url(self):
        if self.object_id is None:
            return '{0}/{1}'.format(self.parent.get_url(), self.path)

        return '{0}/{1}/{2}'.format(self.parent.get_url(), self.path,
                                    self.object_id)


class Milestone(MilestonesBase):

    @base.resource(labels.MilestoneLabels)
    def labels(self):
        """
        Return the resource corresponding to the labels of this milestone.
        """
        return labels.MilestoneLabels(self)


class Milestones(MilestonesBase):

    @base.apimethod
    def get(self, state='open', sort='due_date', direction='desc',
            page=None, per_page=None):
        """
        Fetch milestones for this repository, based on the filter parameters.

        For details on the meanings and allowed values for each parameter,
        see {0}.
        """
        url = self.get_url()
        params = base.get_params(
            ('state', 'sort', 'direction', 'page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    get.__doc__ = get.__doc__.format(
        'http://developer.github.com/v3/issues/milestones/'
        '#list-milestones-for-a-repository')
