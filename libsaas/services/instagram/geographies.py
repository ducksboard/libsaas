from libsaas.services import base

from . import resource, media


class Geography(resource.ReadonlyResource):

    path = 'geographies'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(media.RecentMedia)
    def recent_media(self):
        """
        Return the resource corresponding to all recent media
        for the greography.
        """
        return media.RecentMedia(self)

