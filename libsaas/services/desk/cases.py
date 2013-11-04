from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Replies(resource.PaginatedDeskResource):

    path = 'replies'


class Reply(resource.DeskResource):

    path = 'replies'


class CasesBase(resource.DeskResource):

    path = 'cases'


class Cases(CasesBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, embed=None, fields=None, per_page=None, page=None):
        """
        Retrieve a paginated list of all cases.

        Upstream documentation: http://dev.desk.com/API/cases#list
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def search(self, name=None, first_name=None, last_name=None, email=None,
               phone=None, company=None, twitter=None, labels=None,
               case_id=None, subject=None, description=None,
               status=None, priority=None, assigned_group=None,
               assigned_user=None, channels=None, notes=None, attachments=None,
               created=None, updated=None, since_created_at=None,
               max_created_at=None, since_updated_at=None, max_updated_at=None,
               since_id=None, max_id=None, per_page=None, page=None,
               embed=None, fields=None, **case_custom_fields):
        """
        Search cases based on a combination of parameters with pagination.

        Upstream documentation: http://dev.desk.com/API/cases#search
        """
        store = locals()
        store.update(store.pop('case_custom_fields'))

        params = base.get_params(None, store)
        url = '{0}/{1}'.format(self.get_url(), 'search')
        return http.Request('GET', url, params), parsers.parse_json


class Case(CasesBase):

    def __init__(self, parent, object_id, is_external=False):
        case_id = 'e-%s' % object_id if is_external else object_id
        super(Case, self).__init__(parent, case_id)

    @base.apimethod
    def message(self):
        """
        Retrieve the original message for this case.

        Upstream documentation: http://dev.desk.com/API/cases#message-show
        """
        url = '{0}/{1}'.format(self.get_url(), 'message')
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def history(self, per_page=None, page=None):
        """
        The case history endpoint will display a paginated list of all
        events/actions that have happened to the case

        Upstream documentation: http://dev.desk.com/API/cases#history
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'history')
        return http.Request('GET', url, params), parsers.parse_json

    @base.resource(Replies)
    def replies(self):
        """
        Return the resource corresponding to the case replies
        """
        return Replies(self)

    @base.resource(Reply)
    def reply(self, reply_id):
        """
        Return the resource corresponding to a single reply
        """
        return Reply(self, reply_id)
