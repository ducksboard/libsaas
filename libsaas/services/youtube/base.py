from libsaas.services import base


class YouTubeBaseResource(base.Resource):

    APIROOT = None

    def __init__(self, access_token=None):
        """
        Create a YouTube service.

        :var access_token:
        :vartype access_token:
        """
        self.access_token = access_token

        self.add_filter(self.add_auth)

    def add_auth(self, request):
        header = 'Bearer {0}'.format(self.access_token)
        request.headers['Authorization'] = header

    def get_url(self):
        return self.APIROOT

    def set_access_token(self, access_token):
        self.access_token = access_token
