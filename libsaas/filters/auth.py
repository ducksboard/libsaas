import base64


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
