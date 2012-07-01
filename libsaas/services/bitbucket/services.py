from . import resource


class BaseServices(resource.BitBucketResource):

    path = 'services'


class Service(BaseServices):
    pass


class Services(BaseServices):
    pass
