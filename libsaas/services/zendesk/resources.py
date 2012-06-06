from libsaas import http, parsers
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

    # XXX does not work
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
        url = '{0}/{1}/tickets/requested.json'.format(self.path,
                                                      self.object_id)
        params = self.collection_params(page, per_page)

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def tickets_ccd(self, page=None, per_page=None):
        """
        Fetch tickets where this user is CC'd.
        """
        url = '{0}/{1}/tickets/ccd.json'.format(self.path, self.object_id)
        params = self.collection_params(page, per_page)

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


class Views(ZendeskResource):

    path = 'views'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def active(self, page=None, per_page=None):
        """
        Fetch active shared and personal Views available to the current user.
        """
        url = '{0}/{1}'.format(self.get_url(), 'active')
        params = base.get_params(('page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json
