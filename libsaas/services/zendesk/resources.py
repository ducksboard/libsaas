from libsaas import http, parsers, port
from libsaas.services import base


class ZendeskResource(base.RESTResource):

    path = None

    @base.apimethod
    def get(self, page=None, per_page=None):
        """
        For single-object resources, fetch the object's data. For collections,
        fetch all of the objects.

        :var page: For collections, where should paging start. If left as
            `None`, the first page is returned.
        :vartype page: int

        :var per_page: For collections, how many objects sould be returned. The
            maximum is 100. If left as `None`, 100 objects are returned.
        :vartype per_page: int
        """
        params = base.get_params(('page', 'per_page'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class TicketsBase(ZendeskResource):

    path = 'tickets'


class Tickets(TicketsBase):

    @base.apimethod
    def recent(self, page=None, per_page=None):
        """
        Fetch all recent tickets. The parameters are the same as for the `get`
        method.
        """
        url = '{0}/{1}'.format(self.get_url(), 'recent')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json


class Ticket(TicketsBase):

    # XXX gives 404 in Zendesk
    @base.apimethod
    def collaborators(self, page=None, per_page=None):
        """
        Fetch the collaborators on a ticket.
        """
        url = '{0}/{1}'.format(self.get_url(), 'collaborators')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def audits(self, page=None, per_page=None):
        """
        Fetch the audits on a ticket.
        """
        url = '{0}/{1}'.format(self.get_url(), 'audits')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json


class UsersBase(ZendeskResource):

    path = 'users'


class Users(UsersBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def search(self, query, page=None, per_page=None):
        """
        Fetch users based on their usernames or email addresses.

        :var query: A username or an email address.
        :vartype query: str
        """
        url = '{0}/{1}'.format(self.get_url(), 'search')
        params = base.get_params(('query', 'page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json


class CurrentUser(base.HierarchicalResource):

    path = 'users'

    @base.apimethod
    def get(self):
        url = '{0}/{1}'.format(self.get_url(), 'me')

        return http.Request('GET', url), parsers.parse_json


class User(UsersBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def tickets_requested(self, page=None, per_page=None):
        """
        Fetch tickets requested by this user.
        """
        url = '{0}/tickets/{1}'.format(self.get_url(), 'requested')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def tickets_ccd(self, page=None, per_page=None):
        """
        Fetch tickets where this user is CC'd.
        """
        url = '{0}/tickets/{1}'.format(self.get_url(), 'ccd')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json


class GroupsBase(ZendeskResource):

    path = 'groups'


class Groups(GroupsBase):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def assignable(self, page=None, per_page=None):
        """
        Fetch assignable groups.
        """
        url = '{0}/{1}'.format(self.get_url(), 'assignable')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json


class Group(GroupsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class ActivitiesBase(ZendeskResource):

    path = 'activities'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Activities(ActivitiesBase):

    @base.apimethod
    def get(self, since=None, page=None, per_page=None):
        """
        Fetch the list of activities

        :var since: Timestamp offset in UTC on ISO8601 form %Y-%m-%dT%H:%M:%SZ
        :vartype since: str
        """
        params = base.get_params(('since', 'page', 'per_page'), locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json


class Activity(ActivitiesBase):
    pass


class SatisfactionRatingsBase(ZendeskResource):

    path = 'satisfaction_ratings'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class SatisfactionRatings(SatisfactionRatingsBase):

    @base.apimethod
    def received(self, page=None, per_page=None):
        """
        Fetch ratings provided by customers.
        """
        url = '{0}/{1}'.format(self.get_url(), 'received')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json


class SatisfactionRating(SatisfactionRatingsBase):
    pass


class ViewsBase(ZendeskResource):

    path = 'views'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Views(ViewsBase):

    @base.apimethod
    def active(self, page=None, per_page=None):
        """
        Fetch active shared and personal Views available to the current user.
        """
        url = '{0}/{1}'.format(self.get_url(), 'active')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def count_many(self, ids):
        """
        Calculates the size of the view in terms of number of tickets the view
        will return. Only returns values for personal and shared views
        accessible to the user performing the request.

        :var ids: List of view ids
        :vartype ids: tuple of int
        """

        def serializer(val):
            if isinstance(val, (list, tuple)):
                return ','.join(map(port.to_b, val))
            return base.serialize_param(val)

        url = '{0}/{1}'.format(self.get_url(), 'count_many')
        params = base.get_params(('ids',), locals(), serializer)
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def preview(self, conditions, columns=None, group_by=None,
                group_order=None, sort_by=None, sort_order=None):
        """
        Views can be previewed by constructing the conditions
        in the proper format. See {0}.

        :var conditions: A representation of the conditions that constitute the
            view. See {1}.
        :vartype conditions: dict

        :var columns: The ticket fields to display. System fields are looked up
            by name, custom fields by title or id.
        :vartype columns: tuple of int or str

        :var group_by: When present, the field by which the tickets are grouped
        :vartype group_by: str

        :var group_order: The direction the tickets are grouped.
            May be one of 'asc' or 'desc'
        :vartype group_order: str

        :var sort_by: The field used for sorting. This will either be a title
            or a custom field id.
        :vartype sort_by: str

        :var sort_order: The direction the tickets are sorted. May be one of
            'asc' or 'desc'
        :vartype sort_order: str
        """

        url = '{0}/{1}'.format(self.get_url(), 'preview')
        params = base.get_params(('columns', 'group_by', 'group_order',
                                  'sort_by', 'sort_order'), locals())

        view = {'view': conditions.copy()}
        view['view'].update({'output': params})

        request = http.Request('POST', url, view)
        return request, parsers.parse_json

    preview.__doc__ = preview.__doc__.format(
        'http://developer.zendesk.com/documentation/'
        'rest_api/views.html#previewing-views',
        'http://developer.zendesk.com/documentation/'
        'rest_api/views.html#conditions')


class View(ViewsBase):

    @base.apimethod
    def execute(self, sort_by=None, sort_order=None):
        """
        Get the view output. View output sorting can be controlled by passing
        the sort_by and sort_order parameters.

        :var sort_by: The field used for sorting. This will either be a title
            or a custom field id.
        :vartype sort_by: str

        :var sort_order: The direction the tickets are sorted. May be one of
            'asc' or 'desc'
        :vartype sort_order: str
        """
        url = '{0}/{1}'.format(self.get_url(), 'execute')
        params = base.get_params(('sort_by', 'sort_order'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def count(self):
        """
        Returns the ticket count for a single view.
        """
        url = '{0}/{1}'.format(self.get_url(), 'count')

        return http.Request('GET', url), parsers.parse_json


class Exports(ZendeskResource):

    path = 'exports'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def tickets(self, start_time):
        """
        Retrieve tickets that changed in Zendesk "since last you asked"

        :var start_time:  The time of the oldest ticket you are interested in.
            Tickets modified on or since this time will be returned. The start
            time is provided as the number of seconds since epoch UTC.
        :vartype start_time: int
        """
        url = '{0}/{1}'.format(self.get_url(), 'tickets')
        params = base.get_params(('start_time',), locals())

        return http.Request('GET', url, params), parsers.parse_json
