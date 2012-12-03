import base64

from libsaas import http


class BasicAuth(object):
    """
    Adds a Basic authentication header to each request.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, request):
        auth = '{0}:{1}'.format(self.username, self.password)
        # According to RFC2617 the username and password are *TEXT, which
        # RFC2616 says may contain characters from outside of ISO-8859-1 if
        # they are MIME-encoded. Let's make life easier and assume this means
        # that the username and password will be latin-1
        encoded = base64.b64encode(auth.encode('latin-1')).decode('latin-1')
        header = 'Basic {0}'.format(encoded)
        request.headers['Authorization'] = header


class DummyRequest(object):

    def __init__(self, url=None, headers={}, method=None, data={}, params={}):
        self.url = url
        self.headers = headers
        self.method = method
        self.data = data
        self.params = params


class OAuth(object):
    """
    Signs each request according to OAuth 1.0a.

    Raises an ImportError if the oauth2 library is not present.
    """
    def __init__(self, key, secret, oauth_token, oauth_token_secret):
        import oauth_hook

        self.hook = oauth_hook.OAuthHook(key, secret, oauth_token,
                                         oauth_token_secret, True)

    def __call__(self, request):
        # prepare the parameters
        kwargs = {'method': request.method, 'url': request.uri,
                  'headers': request.headers.copy()}
        if request.params:
            if request.method.upper() in http.URLENCODE_METHODS:
                kwargs['params'] = request.params
            else:
                kwargs['data'] = request.params

        # create a dummy Request object
        req = DummyRequest(**kwargs)

        # sign it
        self.hook(req)

        # use Authorization header
        request.headers['Authorization'] = req.headers['Authorization']
