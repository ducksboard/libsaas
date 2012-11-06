from libsaas import http, parsers
from libsaas.services import base


class YouTubeResource(base.RESTResource):

    #def get_url(self):
        #return '{0}/{1}'.format(self.parent.get_url(), self.path)

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Activities(YouTubeResource):

    path = 'activities'

    @base.apimethod
    def get(self, part, channelId=None, home=None, mine=None,
           maxResults=None, publishedAfter=None, publishedBefore=None,
           pageToken=None):
        """
        Returns a collection of channel activity events matching the
        request criteria. For example, you can retrieve events
        associated with a particular channel, events associated
        with the user's subscriptions and Google+ friends, or the
        YouTube home page feed, which is customized for each user.

        :var part: The part parameter specifies a comma-separated list
            of one or more activity resource properties that the API
            response will include. The part names that you can include
            in the parameter value are id, snippet, and contentDetails.
        :vartype part: str

        :var channelId: The channelId parameter specifies a unique YouTube
            channel ID. The API will then return a list of that channel's
            activities.
        :vartype channelId: str

        :var home: Set this parameter's value to true to retrieve the activity
            feed that displays on the YouTube home page for the currently
            authenticated user.
        :vartype home: bool

        :var mine: Set this parameter's value to true to retrieve a feed
            of the authenticated user's activities.
        :vartype mine: bool

        :var maxResults: The maxResults parameter specifies the maximum number
            of items that should be returned in the result set. Acceptable
            values are 0 to 50, inclusive. The default value is 5.
        :vartype maxResults: int

        :var publishedAfter: The publishedAfter parameter specifies the
            earliest date and time that an activity could have occurred
            for that activity to be included in the API response. If the
                parameter value specifies a day, but not a time, then any
                activities that occurred that day will be included in the
                result set. The value is specified in
                ISO 8601 (YYYY-MM-DDThh:mm:ss.sZ) format.
        :vartype publishedAfter: str

        :var publishedBefore: The publishedBefore parameter specifies the date
            and time before which an activity must have occurred for that
            activity to be included in the API response. If the parameter
            value specifies a day, but not a time, then any activities that
            occurred that day will be excluded from the result set. The
            value is specified in ISO 8601 (YYYY-MM-DDThh:mm:ss.sZ) format.
        :vartype publishedBefore: str

        :var pageToken: The pageToken parameter identifies a specific page in
            the result set that should be returned. In an API response, the
            nextPageToken and prevPageToken properties identify other pages
            that could be retrieved.
        :vartype pageToken: str
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class Channels(YouTubeResource):

    path = 'channels'

    @base.apimethod
    def get(self, part, id=None, mine=None, categoryId=None,
            mySubscribers=None, maxResults=None, pageToken=None):
        """
        Returns a collection of zero or more channel resources that
        match the request criteria.

        :var part: The part parameter specifies a comma-separated list
            of one or more channel resource properties that the API
            response will include. The part names that you can include
            in the parameter value are id, snippet, contentDetails,
            statistics, and topicDetails.
        :vartype part: str

        :var id: The id parameter specifies a comma-separated list of
            the YouTube channel ID(s) for the resource(s) that are
            being retrieved. In a channel resource, the id property
            specifies the channel's YouTube channel ID.
        :vartype id: str

        :var mine: Set this parameter's value to true to instruct the
            API to only return channels owned by the authenticated user.
        :vartype mine: bool

        :var categoryId: The categoryId parameter specifies a
            Freebase topic ID thereby requesting YouTube channels associated
            with that topic. In a channel resource, the
            (key).topicDetails.topicIds[] property identifies the topic IDs
            associated with that channel.
        :vartype categoryId: str

        :var mySubscribers: Set this parameter's value to true to retrieve
            a list of channels that subscribed to the authenticated
            user's channel.
        :vartype mySubscribers: str

        :var maxResults: The maxResults parameter specifies the maximum number
            of items that should be returned in the result set. Acceptable
            values are 0 to 50, inclusive. The default value is 5.
        :vartype maxResults: int

        :var pageToken: The pageToken parameter identifies a specific page in
            the result set that should be returned. In an API response, the
            nextPageToken and prevPageToken properties identify other pages
            that could be retrieved.
        :vartype pageToken: str
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class GuideCategories(YouTubeResource):

    path = 'guideCategories'

    @base.apimethod
    def get(self, part, id=None, regionCode=None, hl=None):
        """
        Returns a collection of categories that can be associated with
        YouTube videos.

        :var part: The part parameter specifies a comma-separated list
            of one or more guideCategory resource properties that
            the API response will include. The part names that you
            can include in the parameter value are id and snippet.
        :vartype part: str

        :var id: The id parameter specifies a comma-separated list
            of the YouTube channel category ID(s) for the resource(s)
            that are being retrieved. In a guideCategory resource, the
            id property specifies the YouTube channel category ID.
        :vartype id: str

        :var regionCode: The regionCode parameter instructs the API to return
            the list of video categories available in the specified country.
            The parameter value is an ISO 3166-1 alpha-2 country code.
        :vartype regionCode: str

        :var hl: The hl parameter specifies the language that should be used
            for text values in the API response. The default value is en_US.
        :vartype hl: str
        """

        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class PlaylistItems(YouTubeResource):

    path = 'playlistItems'

    @base.apimethod
    def get(self, part, id=None, playlistId=None,
            maxResults=None, pageToken=None):
        """
        Returns a collection of playlist items that match the API request
        parameters. You can retrieve all of the playlist items in a specified
        playlist or retrieve one or more playlist items by their unique IDs.

        :var part: The part parameter specifies a comma-separated list of one
            or more playlistItem resource properties that the API response will
            include. The part names that you can include in the parameter value
            are id, snippet, and contentDetails.
        :vartype part: str

        :var id: The id parameter specifies a comma-separated list of one or
            more unique playlist item IDs. Note that even though this is an
            optional parameter, every request to retrieve playlist items must
            specify a value for either the id parameter or the playlistId
            parameter.
        :vartype id: str

        :var playlistId: The playlistId parameter specifies the unique ID of
            the playlist for which you want to retrieve playlist items. Note
            that even though this is an optional parameter, every request to
            retrieve playlist items must specify a value for either the id
            parameter or the playlistId parameter.
        :vartype playlistId: str

        :var maxResults: The maxResults parameter specifies the maximum number
            of items that should be returned in the result set. Acceptable
            values are 0 to 50, inclusive. The default value is 5.
        :vartype maxResults: int

        :var pageToken: The pageToken parameter identifies a specific page in
            the result set that should be returned. In an API response, the
            nextPageToken and prevPageToken properties identify other pages
            that could be retrieved.
        :vartype pageToken: str
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class Playlists(YouTubeResource):

    path = 'playlists'

    @base.apimethod
    def get(self, part, id=None, mine=None,
            maxResults=None, pageToken=None):
        """
        Returns a collection of playlists that match the API request
        parameters.

        :var part: The part parameter specifies a comma-separated list of one
            or more playlist resource properties that the API response will
            include. The part names that you can include in the parameter
            value are id, snippet, and status.
        :vartype part: str

        :var id: The id parameter specifies a comma-separated list of the
        YouTube playlist ID(s) for the resource(s) that are being retrieved.
            In a playlist resource, the id property specifies the playlist's
            YouTube playlist ID.
        :vartype id: str

        :var mine: Set this parameter's value to true to instruct the API to
            only return playlists owned by the authenticated user.
        :vartype mine: bool

        :var maxResults: The maxResults parameter specifies the maximum number
            of items that should be returned in the result set. Acceptable
            values are 0 to 50, inclusive. The default value is 5.
        :vartype maxResults: int

        :var pageToken: The pageToken parameter identifies a specific page in
            the result set that should be returned. In an API response, the
            nextPageToken and prevPageToken properties identify other pages
            that could be retrieved.
        :vartype pageToken: str
        """

        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class Search(YouTubeResource):

    path = 'search'

    @base.apimethod
    def get(self, part, q=None, relativeToVideo=None, maxResults=None,
            order=None, published=None, type=None, videoCaption=None,
            videoDefiniton=None, videoDimension=None,
            videoDuration=None, videoLicense=None,
            topicId=None, pageToken=None):
        """
        Returns a collection of search results that match the query parameters
        specified in the API request. By default, a search result set
        identifies matching video, channel, and playlist resources, but you
        can also configure queries to only retrieve a specific type of resource

        :var part: The part parameter specifies a comma-separated list of one
            or more search resource properties that the API response will
            include. The part names that you can include in the parameter
            value are id and snippet.
        :vartype part: str

        :var q: The q parameter specifies the query term to search for.
        :vartype q: str

        :var relativeToVideo: The relatedToVideo parameter retrieves a list
            of videos that are related to the video that the parameter value
            identifies. The parameter value must be set to a YouTube video
            ID and, if you are using this parameter, the type parameter must
            be set to video.
        :vartype relativeToVideo: str

        :var maxResults: The maxResults parameter specifies the maximum number
            of items that should be returned in the result set. Acceptable
            values are 0 to 50, inclusive. The default value is 5.
        :vartype maxResults: int

        :var order: The order parameter specifies the method that will be used
            to order resources in the API response.
            The default value is relevance. Acceptable values are: date,
            rating, relevance and view_count.
        :vartype order: str

        :var published: The published parameter indicates that the API response
            should only contain resources created within the specified time
            period. Acceptable values are: any, thisWeek, today and thisMonth.
        :vartype publsihed: str

        :var type: The type parameter restricts a search query to only retrieve
            a particular type of resource.
            The default value is video,channel,playlist.
        :vartype type: str

        :var videoCaption: The videoCaption parameter indicates whether the
            API should filter video search results based on whether they have
            captions. Acceptable values are: any, closedCaption and none.
        :vartype videoCaption: str

        :var videoDefiniton: The videoDefinition parameter lets you restrict a
            search to only include HD videos. Acceptable values are: any, high
            and standard.
        :vartype videoDefiniton: str

        :var videoDimension: The videoDimension parameter lets you restrict
            a search to only retrieve 2D or 3D videos. Acceptable values are:
            2d, 3d and any.
        :vartype videoDimension: str

        :var videoDuration: The videoDuration parameter filters video search
            results based on their duration. Acceptable values are: any, long,
            medium and shot.
        :var videoDuration: str

        :var videoLicense: The videoLicense parameter filters search results
            to only include videos with a particular license. Acceptable values
            are: any, creativeCommons and youtube.
        :var videoLicense: str

        :var topicId: The topicId parameter indicates that the API response
            should only contain resources associated with the specified topic.
            The value identifies a Freebase topic ID.
        :vartype topicId: str

        :var pageToken: The pageToken parameter identifies a specific page in
            the result set that should be returned. In an API response, the
            nextPageToken and prevPageToken properties identify other pages
            that could be retrieved.
        :vartype pageToken: str
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class Subscriptions(YouTubeResource):

    path = 'subscriptions'

    @base.apimethod
    def get(self, part, id=None, mine=None, channelId=None,
            forChannelId=None, maxResults=None, order=None, pageToken=None):
        """
        Returns subscription resources that match the API request criteria.

        :var part: The part parameter specifies a comma-separated list of one
            or more subscription resource properties that the API response
            will include. The part names that you can include in the parameter
            value are id, snippet, and contentDetails.
        :vartype: str

        :var id: The id parameter specifies a comma-separated list of the
            YouTube subscription ID(s) for the resource(s) that are being
            retrieved. In a subscription resource, the id property
            specifies the YouTube subscription ID.
        :vartype id: str

        :var mine: Set this parameter's value to True to retrieve a feed of
            the authenticated user's subscriptions.
        :vartype: bool

        :var channelId: The channelId parameter specifies a YouTube
            channel ID. The API will only return that channel's subscriptions.
        :vartype channelId: str

        :var forChannelId: The forChannelId parameter specifies a
            comma-separated list of channel IDs. The API response
            will then only contain subscriptions matching those channels.
        :vartype forChannelId: str

        :var maxResults: The maxResults parameter specifies the maximum number
            of items that should be returned in the result set. Acceptable
            values are 0 to 50, inclusive. The default value is 5.
        :vartype maxResults: int

        :var order: The order parameter specifies the method that will be used
            to sort resources in the API response. Acceptable values are:
            alphabetical, relevance and unread.
        :vartype order: str

        :var pageToken: The pageToken parameter identifies a specific page in
            the result set that should be returned. In an API response, the
            nextPageToken and prevPageToken properties identify other pages
            that could be retrieved.
        :vartype pageToken: str
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class VideoCategories(YouTubeResource):

    path = 'videoCategories'

    @base.apimethod
    def get(self, part, id=None, regionCode=None, hl=None):
        """
        Returns a list of categories that can be associated with
        YouTube videos.

        :var part: The part parameter specifies the videoCategory
            resource parts that the API response will include.
            Supported values are id and snippet.
        :vartype part: str

        :var id: The id parameter specifies a comma-separated list
            of video category IDs for the resources that you are retrieving.
        :vartype id: str

        :var regionCode: The regionCode parameter instructs the API to return
            the list of video categories available in the specified country.
            The parameter value is an ISO 3166-1 alpha-2 country code.
        :vartype regionCode: str

        :var hl: The hl parameter specifies the language that should be used
            for text values in the API response. The default value is en_US.
        :vartype hl: str
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json


class Videos(YouTubeResource):

    path = 'videos'

    @base.apimethod
    def get(self, part, id):
        """
        Returns a collection of videos that match the API request parameters.

        :var part: The part parameter specifies a comma-separated list of one
            or more video resource properties that the API response will
            include. The part names that you can include in the parameter value
            are id, snippet, contentDetails, player, statistics, status, and
            topicDetails.
        :vartype part: str

        :var id: The id parameter specifies a comma-separated list of the
            YouTube video ID(s) for the resource(s) that are being retrieved.
            In a video resource, the id property specifies the video's ID.
        :vartype id: str
        """
        params = base.get_params(None, locals())

        request = http.Request('GET', self.get_url(), params)
        return request, parsers.parse_json
