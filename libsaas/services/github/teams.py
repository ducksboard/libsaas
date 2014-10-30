from libsaas import http, parsers
from libsaas.services import base

from .members import Members
from . import resource
from . import repos


class TeamMembership(resource.GitHubResource):

    path = 'memberships'

    @base.apimethod
    def add(self):
        request = http.Request('PUT', self.get_url())

        return request, parsers.parse_json


class TeamRepos(repos.Repos):

    path = 'repos'


class TeamRepo(repos.Repo):
    @base.apimethod
    def add(self):
        request = http.Request('PUT', self.get_url())

        return request, parsers.parse_json


class Teams(resource.GitHubResource):

    path = 'teams'

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Team(resource.GitHubResource):

    path = 'teams'

    @base.resource(Members)
    def members(self):
        """
        Return a resource corresponding to a team's members.
        """
        return Members(self)

    @base.resource(TeamMembership)
    def member(self, user):
        """
        Return a resource corresponding to a single member of a team.
        """
        return TeamMembership(self, user)

    @base.resource(TeamRepos)
    def repos(self):
        """
        Return a resource corresponding to the repos manged by this team.
        """
        return TeamRepos(self)

    @base.resource(TeamRepo)
    def repo(self, user, repo):
        """
        Return a resource corresponding to a single repo to determine if it 
        is managed by this team.
        """
        return TeamRepo(self, user, repo)
