from libsaas import http, parsers
from libsaas.services import base

from . import resource
from . import downloads, forks, issues, keys, labels, milestones, repocommits


class Repos(resource.GitHubResource):

    path = 'user/repos'

    @base.apimethod
    def get(self, type='all', page=None, per_page=None):
        """
        Fetch repos for this user.

        :var type: What type of repos to fetch. For details of allowed values,
            see http://developer.github.com/v3/repos/#list-user-repositories.
        """
        params = base.get_params(('page', 'per_page'), locals())
        params['type'] = type
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class RepoCollaborators(base.Resource):

    path = 'collaborators'

    def get_url(self):
        return '{0}/{1}'.format(self.parent.get_url(), self.path)

    @base.apimethod
    def get(self, page=None, per_page=None):
        params = base.get_params(('page', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json
    get.__doc__ = resource.GitHubResource.get.__doc__

    @base.apimethod
    def add(self, user):
        """
        Add a collaborator to this repo.

        :var user: The username of the new collaborator.
        :vartype user: str
        """
        url = '{0}/{1}'.format(self.get_url(), user)

        # include a body, because requests does not send content-length when no
        # body is present, and that makes GitHub respond with HTTP 411
        return http.Request('PUT', url, '*'), parsers.parse_empty

    @base.apimethod
    def remove(self, user):
        """
        Remove a collaborator from this repo.

        :var user: The username of the collaborator.
        :vartype user: str
        """
        url = '{0}/{1}'.format(self.get_url(), user)

        return http.Request('DELETE', url), parsers.parse_empty

    @base.apimethod
    def is_collaborator(self, user):
        """
        Check if a user is a collaborator in this repo.

        :var user: The username to check.
        :vartype user: str

        :return: bool
        """
        url = '{0}/{1}'.format(self.get_url(), user)

        return http.Request('GET', url), resource.parse_boolean


class Repo(resource.GitHubResource):

    def __init__(self, parent, user, repo):
        self.parent = parent
        self.user = http.quote_any(user)
        self.repo = http.quote_any(repo)

    def get_url(self):
        return '{0}/repos/{1}/{2}'.format(self.parent.get_url(),
                                          self.user, self.repo)

    def require_collection(self):
        return False

    def require_item(self):
        return True

    @base.apimethod
    def contributors(self, anon=False):
        """
        Fetch the contributors from this repo.

        :var anon: Include anonymous contributors.
        :vartype anon: bool
        """
        params = {'anon': 'true' if anon else 'f'}
        url = '{0}/{1}'.format(self.get_url(), 'contributors')

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def languages(self):
        """
        Fetch the languages for this repo.
        """
        url = '{0}/{1}'.format(self.get_url(), 'languages')

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def teams(self):
        """
        Fetch the teams for this repo.
        """
        url = '{0}/{1}'.format(self.get_url(), 'teams')

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def tags(self):
        """
        Fetch the tags for this repo.
        """
        url = '{0}/{1}'.format(self.get_url(), 'tags')

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def branches(self):
        """
        Fetch the branches for this repo.
        """
        url = '{0}/{1}'.format(self.get_url(), 'branches')

        return http.Request('GET', url), parsers.parse_json

    @base.resource(issues.RepoIssue)
    def issue(self, issue_id):
        """
        Return a resource corresponding to a single issue from this repo.
        """
        return issues.RepoIssue(self, issue_id)

    @base.resource(issues.RepoIssues)
    def issues(self):
        """
        Return a resource corresponding to all issues from this repo.
        """
        return issues.RepoIssues(self)

    @base.resource(labels.RepoLabel)
    def label(self, name):
        """
        Return a resource corresponding to a single label from this repo.
        """
        return labels.RepoLabel(self, name)

    @base.resource(labels.RepoLabels)
    def labels(self):
        """
        Return a resource corresponding to all issues from this repo.
        """
        return labels.RepoLabels(self)

    @base.resource(milestones.Milestone)
    def milestone(self, milestone_id):
        """
        Return a resource corresponding to a single milestone in this repo.
        """
        return milestones.Milestone(self, milestone_id)

    @base.resource(milestones.Milestones)
    def milestones(self):
        """
        Return a resource corresponding to all milestones in this repo.
        """
        return milestones.Milestones(self)

    @base.resource(RepoCollaborators)
    def collaborators(self):
        """
        Return a resource corresponding to all collaborators in this repo.
        """
        return RepoCollaborators(self)

    @base.resource(repocommits.RepoCommit)
    def commit(self, sha):
        """
        Return a resource corresponding to a single commit in this repo.
        """
        return repocommits.RepoCommit(self, sha)

    @base.resource(repocommits.RepoCommits)
    def commits(self):
        """
        Return a resource corresponding to all commits in this repo.
        """
        return repocommits.RepoCommits(self)

    @base.resource(downloads.Download)
    def download(self, download_id):
        """
        Return a resource corresponding to a single download in this repo.
        """
        return downloads.Downloads(self, download_id)

    @base.resource(downloads.Downloads)
    def downloads(self):
        """
        Return a resource corresponding to all commits from this repo.
        """
        return downloads.Downloads(self)

    @base.resource(forks.Forks)
    def forks(self):
        """
        Return a resource corresponding to all forks of this repo.
        """
        return forks.Forks(self)

    @base.resource(keys.RepoKey)
    def key(self, key_id):
        """
        Return a resource corresponding to a single key in this repo.
        """
        return keys.RepoKey(self, key_id)

    @base.resource(keys.RepoKeys)
    def keys(self):
        """
        Return a resource corresponding to all SSH keys of this repo.
        """
        return keys.RepoKeys(self)
