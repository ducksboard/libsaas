import json

from . import resources
from libsaas import http, parsers
from libsaas.services import base


class SegmentIO(base.Resource):

    def __init__(self, api_secret):
        """
        Create a SegmentIO service

        :var api_secret: Your project's API secret.
        :vartype api_secret: str
        """
        self.apiroot = 'https://api.segment.io/v1'
        self.api_secret = api_secret

        self.add_filter(self.add_authorization)
        self.add_filter(self.use_json)

    def add_authorization(self, request):
        request.params['secret'] = self.api_secret

    def use_json(self, request):
        request.headers['Content-Type'] = 'application/json; charset=utf-8'
        request.params = json.dumps(request.params)

    def get_url(self):
        return self.apiroot

    @base.resource(resources.User)
    def user(self, user_id):
        """
        Return the resource corresponding to a single user
        """
        return resources.User(self, user_id)

    @base.apimethod
    def alias(self, from_user_id, to_user_id, context=None, timestamp=None):
        """
        Identify an user.

        :var from_user_id: The anonymous user's id before they are logged in.
        :vartype from_user_id: str

        :var to_user_id: The identified user's id after they're logged in.
        :vartype to_user_id: str

        :var context: A dictionary of provider specific options.
        :vartype context: dict

        :var timestamp: An ISO 8601 date string representing
        when the identify took place.
        :vartype timestamp: str
        """
        params = {
            'from': from_user_id,
            'to': to_user_id,
        }
        params.update(base.get_params(('context', 'timestamp'), locals()))
        url = '{0}/{1}'.format(self.get_url(), 'alias')

        request = http.Request('POST', url, params)
        return request, parsers.parse_json

