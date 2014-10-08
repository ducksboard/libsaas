from libsaas.services import base

from . import resource


class ReleaseAssetBase(resource.GitHubResource):

    path = 'assets'


class ReleaseAssets(ReleaseAssetBase):
    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ReleaseAsset(ReleaseAssetBase):
    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ReleasesBase(resource.GitHubResource):

    path = 'releases'


class Releases(ReleasesBase):
    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Release(ReleasesBase):

    @base.resource(ReleaseAssets)
    def assets(self):
        return ReleaseAssets(self)

    @base.resource(ReleaseAsset)
    def asset(self, asset_id):
        return ReleaseAsset(self, asset_id)
