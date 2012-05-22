import base64


class BasicAuth(object):
    """
    Adds a Basic authentication header to each request.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __call__(self, request):
        auth = '%s:%s' % (self.username, self.password)
        header = 'Basic %s' % base64.b64encode(auth)
        request.headers['Authorization'] = header
