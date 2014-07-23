import base64
from hashlib import sha1
import hmac
import time
import random

from libsaas import http, port


class BasicAuth(object):
    """
    Adds a Basic authentication header to each request.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, request):
        # According to RFC2617 the username and password are *TEXT, which
        # RFC2616 says may contain characters from outside of ISO-8859-1 if
        # they are MIME-encoded. Our first approach was to assume latin-1 in
        # username and password, but practice has proved us wrong (services
        # like Zendesk allow non-latin-1 characters in both, which are used
        # in basic auth for their API). To be as compatible as possible,
        # allow unicode in username and password, but keep resulting base64
        # in latin-1.
        auth = port.to_u('{0}:{1}').format(port.to_u(self.username),
                                           port.to_u(self.password))
        encoded = port.to_u(base64.b64encode(port.to_b(auth)), 'latin-1')
        header = 'Basic {0}'.format(encoded)
        request.headers['Authorization'] = header


class OAuthRFC5849(object):
    """
    Signs each request according to RFC5849.

    Only supports header-based authentication and only uses HMAC-SHA1.

    The oauth_token and oauth_token_secret parameters can be None. This is
    useful for making Temporary Credentials requests (section 2.1 of the RFC).
    """
    def __init__(self, oauth_token, oauth_token_secret, key, secret):
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.key = key
        self.secret = secret

    def __call__(self, request):
        nonce = self.generate_nonce()
        timestamp = self.generate_timestamp()

        base = self.get_base_string(request, nonce, timestamp)

        key = self.encode(self.secret) + '&'
        if self.oauth_token_secret:
            key += self.encode(self.oauth_token_secret)
        digest = hmac.new(port.to_b(key), port.to_b(base), sha1).digest()
        signature = self.encode(base64.b64encode(digest))

        params = self.oauth_params(nonce, timestamp, signature)
        auth = ','.join('{0}="{1}"'.format(key, val)
                        for key, val in sorted(params))
        header = 'OAuth ' + auth

        if request.headers is None:
            request.headers = {}

        request.headers['Authorization'] = header

    def use_request_params(self, request):
        """
        Whether request parameters should be included in the signature base
        string. For RFC5849 OAuth, and under the assumptions libsaas makes,
        they are included if request params are not a blob.
        """
        if request.params is None:
            return False

        if isinstance(request.params, (port.text_type, port.binary_type)):
            return False

        return True

    def get_base_string(self, request, nonce, timestamp):
        # if there are query string params, remove them from the basic string,
        # as encode_parameters already took care of including them
        parsed = port.urlparse(request.uri)
        uri = port.urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                               parsed.params, '', parsed.fragment))

        return (self.encode(request.method) + '&' +
                self.encode(uri) + '&' +
                self.normalized_params(request, nonce, timestamp))

    def normalized_params(self, request, nonce, timestamp):
        params = ()

        # check for query string parameters
        params += self.encode_qs_params(request)

        # if request parameters are to be included, encode them
        if self.use_request_params(request):
            params += self.encode_request_params(request)

        # add OAuth parameters, like oauth_token, oauth_nonce etc
        params += self.oauth_params(nonce, timestamp)

        # sort them the way RFC5849 requires
        normalized = '&'.join(sorted((key + '=' + value
                                      for key, value in params)))

        # and encode the resulting string
        return self.encode(normalized)

    def encode_qs_params(self, request):
        # If there is a query string, split it out and include in the
        # parameters. In typical libsaas usage there will never be a query
        # string, since parameters should be passed as Request.params, but just
        # in case someone tried, check it.
        query = port.urlparse(request.uri).query
        params = port.parse_qsl(query, True)

        return tuple((self.encode(key), self.encode(val))
                     for key, val in params)

    def encode_request_params(self, request):
        # if params are a dict, make it into a sequence
        params = request.params
        try:
            params = tuple(params.items())
        except AttributeError:
            pass

        # encode keys and values
        return tuple((self.encode(key), self.encode(val))
                     for key, val in params)

    def generate_nonce(self):
        return str(random.getrandbits(64))

    def generate_timestamp(self):
        return str(int(time.time()))

    def oauth_params(self, nonce, timestamp, signature=None):
        params = (('oauth_nonce', nonce), ('oauth_timestamp', timestamp),
                  ('oauth_consumer_key', self.key),
                  ('oauth_signature_method', 'HMAC-SHA1'))
        if self.oauth_token:
            params += (('oauth_token', self.oauth_token), )
        if signature:
            params += (('oauth_signature', signature), )

        return params

    def encode(self, val):
        # RFC5849 says that ~ should not be quoted, but / should
        return port.quote(port.to_b(val), safe='~')


class OAuth1a(OAuthRFC5849):
    """
    Signs each request according to OAuth Core 1.0 Revision A.
    """
    def use_request_params(self, request):
        """
        OAuth 1.0a only mentions POST requests, so for instance PUT bodies,
        even it their content-type is application/x-www-form-urlencoded won't
        be part of the signature base string.
        """
        if request.params is None:
            return False

        # GET parameters get appended to the URL, so they're used
        if request.method.upper() in http.URLENCODE_METHODS:
            return True

        if request.method.upper() != 'POST':
            return False

        if isinstance(request.params, (port.text_type, port.binary_type)):
            return False

        return True


# alias OAuthRFC5849 (the sane version of the spec) to just OAuth
OAuth = OAuthRFC5849
