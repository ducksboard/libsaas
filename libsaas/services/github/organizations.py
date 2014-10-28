from libsaas.services import base

from .members import Members, Member, PublicMembers, PublicMember
from .teams import Teams
from . import resource
from . import repos


class OrganizationRepos(repos.Repos):

    path = 'repos'


class OrganizationRepo(repos.Repo):
    pass


class Organizations(resource.GitHubResource):

    path = 'orgs'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(repos.Repo)
    def repos(self):
        """
        Return a resource corresponding to repos for this org.
        """
        return OrganizationRepos(self)

    @base.resource(OrganizationRepo)
    def repo(self, repo):
        """
        Return a resource corresponding to single repo for this org.
        """
        return OrganizationRepo(self.parent, self.object_id, repo)

    @base.resource(Members)
    def members(self):
        """
        Return a resource corresponding to members of this org.
        """
        return Members(self)

    @base.resource(Member)
    def member(self, user):
        """
        Return a resource corresponding to a member of this org.
        """
        return Member(self, user)

    @base.resource(PublicMembers)
    def public_members(self):
        """
        Return a resource corresponding to public members of this org.
        """
        return PublicMembers(self)

    @base.resource(PublicMember)
    def public_member(self, user):
        """
        Return a resource corresponding to a public member of this org.
        """
        return PublicMember(self, user)

    @base.resource(Teams)
    def teams(self):
        """
        Return a resource corresponding to this org's teams.
        """
        return Teams(self)
