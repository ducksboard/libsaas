from . import resource


class AuthorizationsBase(resource.GitHubResource):

    path = 'authorizations'


class Authorization(AuthorizationsBase):
    pass


class Authorizations(AuthorizationsBase):
    pass
