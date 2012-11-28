from libsaas import http, parsers
from libsaas.services import base

from . import resource


class CasesBase(resource.DeskResource):

    path = 'cases'


class Cases(CasesBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, name=None, first_name=None, last_name=None, email=None,
            phone=None, company=None, twitter=None, labels=None,
            case_id=None, subject=None, description=None,
            status=None, priority=None, assigned_group=None,
            assigned_user=None, channels=None, notes=None, attachments=None,
            created=None, updated=None, since_created_at=None,
            max_created_at=None, since_updated_at=None, max_updated_at=None,
            since_id=None, max_id=None, count=None, page=None,
            **case_custom_fields):
        """
        Search cases based on a combination of parameters with pagination.

        Upstream documentation: http://dev.desk.com/docs/api/cases
        """
        store = locals()
        store.update(store.pop('case_custom_fields'))

        params = base.get_params(None, store)

        return http.Request('GET', self.get_url(), params), parsers.parse_json


class Case(CasesBase):

    def __init__(self, parent, object_id, is_external=False):
        super(Case, self).__init__(parent, object_id)
        self.is_external = is_external

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self):
        """
        Show the case
        """
        params = {'by': 'external_id'} if self.is_external else None
        return http.Request('GET', self.get_url(), params), parsers.parse_json
