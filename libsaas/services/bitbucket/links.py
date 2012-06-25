from . import resource


class RepoLinksBase(resource.BitBucketResource):

    path = 'links'


class RepoLink(RepoLinksBase):
    pass


class RepoLinks(RepoLinksBase):
    pass
