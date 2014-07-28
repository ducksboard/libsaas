from libsaas import http
from libsaas.services import base


class NewRelicResource(base.RESTResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ApplicationResource(NewRelicResource):

    path = 'applications'


class ApplicationRelatedResource(NewRelicResource):

    def __init__(self, parent, application_id, object_id=None):
        self.parent = parent
        self.object_id = object_id
        self.application_id = http.quote_any(application_id)

        if self.object_id:
            self.object_id = http.quote_any(self.object_id)

    def get_url(self):
        if self.object_id is None:
            return '{0}/applications/{1}/{2}'.format(self.parent.get_url(),
                self.application_id, self.path)

        return '{0}/applications/{1}/{2}/{3}'.format(self.parent.get_url(),
            self.application_id, self.path, self.object_id)
