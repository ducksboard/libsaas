from libsaas import http, parsers
from libsaas.services import base


class ReportsBase(base.RESTResource):

    path = 'reports'
    type = None

    def get_url(self):
        if self.object_id is None:
            return '{0}/{1}.{2}'.format(self.parent.get_url(), self.path,
                                        self.type)

        return '{0}/{1}.{2}/{3}'.format(self.parent.get_url(), self.path,
                                        self.type, self.object_id)

    @base.apimethod
    def get(self):
        self.require_collection()
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json


class ReportsEmail(ReportsBase):

    type = 'email'


class ReportsPublic(ReportsBase):

    type = 'public'


class ReportsShared(ReportsBase):

    type = 'shared'
