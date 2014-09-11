from libsaas.services import base

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
