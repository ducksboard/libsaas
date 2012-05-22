from . import resource


class RepoKeysBase(resource.GitHubResource):

    path = 'keys'


class RepoKey(RepoKeysBase):
    pass


class RepoKeys(RepoKeysBase):
    pass
