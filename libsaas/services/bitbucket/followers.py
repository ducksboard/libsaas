from . import resource


class BaseFollowers(resource.BitBucketResource):

    path = 'followers'


class UserFollowers(BaseFollowers):
    pass


class RepoFollowers(BaseFollowers):
    pass


class IssueFollowers(BaseFollowers):
    pass
