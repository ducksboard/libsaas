from libsaas.services import base

from .base import YouTubeBaseResource
from .analytics import Analytics
from . import v3


class YouTube(YouTubeBaseResource):

    APIROOT = 'https://www.googleapis.com/youtube/v3'

    @base.resource(Analytics)
    def analytics(self):
        """
        Return the resource corresponding to the Analytics API
        """
        return Analytics(self.access_token)

    @base.resource(v3.Activities)
    def activities(self):
        """
        Return the resource corresponding to the YouTube Activities
        """
        return v3.Activities(self)

    @base.resource(v3.Channels)
    def channels(self):
        """
        Return the resource corresponding to the YouTube Channels
        """
        return v3.Channels(self)

    @base.resource(v3.GuideCategories)
    def guide_categories(self):
        """
        Return the resource corresponding to the YouTube GuideCategories
        """
        return v3.GuideCategories(self)

    @base.resource(v3.PlaylistItems)
    def playlist_items(self):
        """
        Return the resource corresponding to the YouTube PlaylistItems
        """
        return v3.PlaylistItems(self)

    @base.resource(v3.Playlists)
    def playlists(self):
        """
        Return the resource corresponding to the YouTube Playlists
        """
        return v3.Playlists(self)

    @base.resource(v3.Search)
    def search(self):
        """
        Return the resource corresponding to the YouTube Search
        """
        return v3.Search(self)

    @base.resource(v3.Subscriptions)
    def subscriptions(self):
        """
        Return the resource corresponding to the YouTube Subscriptions
        """
        return v3.Subscriptions(self)

    @base.resource(v3.VideoCategories)
    def video_categories(self):
        """
        Return the resource corresponding to the YouTube VideoCategories
        """
        return v3.VideoCategories(self)

    @base.resource(v3.Videos)
    def videos(self):
        """
        Return the resource corresponding to the YouTube Videos
        """
        return v3.Videos(self)
