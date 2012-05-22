from libsaas.services import base

from . import resource


class DownloadsBase(resource.GitHubResource):

    path = 'downloads'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Download(DownloadsBase):
    pass


class Downloads(DownloadsBase):
    pass
