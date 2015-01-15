from libsaas import http, parsers
from libsaas.services import base
from libsaas.port import urlencode


def handle_realm(param):
    return 'openid.realm' if param == 'openid_realm' else param


class GoogleOAuth2(base.Resource):

    APIROOT = 'https://accounts.google.com/o/oauth2'

    def __init__(self, client_id, client_secret):
        """
        Create a Google Analytics service.

        :var client_id: The client_id obtained from the APIs Console. Indicates
            the client that is making the request. The value passed in this
            parameter must exactly match the value shown in the APIs Console.
        :var client_id: str

        """
        self.client_id = client_id
        self.client_secret = client_secret

        self.add_filter(self.set_header)

    def add_auth(self, request):
        header = 'Bearer {0}'.format(self.access_token)
        request.headers['Authorization'] = header

    def set_header(self, request):
        if (request.method.upper() not in http.URLENCODE_METHODS
                and request.params):
            request.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    def get_url(self, api_endpoint):
        return '{0}/{1}'.format(self.APIROOT, api_endpoint)

    def get_auth_url(self, response_type, redirect_uri, scope, state=None,
                     access_type=None, approval_prompt=None, login_hint=None,
                     openid_realm=None, hd=None):
        """
        This endpoint is the target of the initial request for an access token.
        It handles active session lookup, authenticating the user, and user
        consent. The result of requests of this endpoint include access tokens,
        refresh tokens, and authorization codes.

        :var response_type: Determines if the Google OAuth 2.0 endpoint returns
            an authorization code. For installed applications, a value of code
            should be used.
        :vartype response_type: str

        :var redirect_uri: One of the redirect_uri values registered at the
            APIs Console. Determines where the response is sent.
            You may choose between urn:ietf:wg:oauth:2.0:oob or an
            http://localhost port.
        :vartype redirect_uri: str

        :var scope: Space delimited set of permissions the application
            requests. Indicates the Google API access your application is
            requesting. The values passed in this parameter inform the consent
            page shown to the user. There is an inverse relationship between
            the number of permissions requested and the likelihood of obtaining
            user consent.
        :vartype scope: str

        :var state: Indicates any state which may be useful to your application
            upon receipt of the response. The Google Authorization Server
            roundtrips this parameter, so your application receives the same
            value it sent.
        :vartype state: str

        :var access_type: online or offline. Indicates if your application
            needs to access a Google API when the user is not present at the
            browser. This parameter defaults to online. If your application
            needs to refresh access tokens when the user is not present at the
            browser, then use offline. This will result in your application
            obtaining a refresh token the first time your application exchanges
            an authorization code for a user.
        :vartype access_type: str

        :var approval_prompt: force or auto. Indicates if the user should be
            re-prompted for consent. The default is auto, so a given user
            should only see the consent page for a given set of scopes the
            first time through the sequence. If the value is force, then the
            user sees a consent page even if they have previously given consent
            to your application for a given set of scopes.
        :vartype approval_prompt: str

        :var login_hint: When your application knows which user it is trying to
            authenticate, it may provide this parameter as a hint to the
            Authentication Server. Passing this hint will either pre-fill the
            email box on the sign-in form or select the proper multi-login
            session, thereby simplifying the login flow.
        :vartype login_hint: str

        :var openid_realm: Parameter from the OpenID 2.0 protocol, not from
            OAuth 2.0. It is used in OpenID 2.0 requests to signify the
            URL-space for which an authentication request is valid.
        :vartype openid_realm: str

        :var hd: The hd (hosted domain) parameter streamlines the login
            process for Google Apps hosted accounts. By including the domain
            (for example, mycollege.edu), you restrict sign-in to accounts at
            that domain
        :vartype hd: str
        """
        params = {'client_id': self.client_id}
        params.update(base.get_params(None, locals(),
            translate_param=handle_realm))

        return '{0}?{1}'.format(self.get_url('auth'), urlencode(params))

    @base.apimethod
    def access_token(self, code, redirect_uri):
        """
        Get the access and/or refresh token

        :var code: The authorization code returned from the initial request
        :vartype code: str


        :var redirect_uri: The URI registered with the application
        :vartype redirect_uri: str
        """
        params = (base.get_params(None, locals()))
        params.update({'client_id': self.client_id,
                       'client_secret': self.client_secret,
                       'grant_type': 'authorization_code'})

        request = http.Request('POST', self.get_url('token'), params)

        return request, parsers.parse_json

    @base.apimethod
    def refresh_token(self, refresh_token):
        """
        Refresh the access token

        :var refresh_token: The refresh token returned from the authorization
            code exchange
        :vartype code: str
        """
        params = (base.get_params(None, locals()))
        params.update({'client_id': self.client_id,
                       'client_secret': self.client_secret,
                       'grant_type': 'refresh_token'})

        request = http.Request('POST', self.get_url('token'), params)

        return request, parsers.parse_json
