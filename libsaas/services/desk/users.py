from libsaas import http, parsers
from libsaas.services import base

from . import resource


class ResourceMixin(object):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Groups(ResourceMixin, resource.PaginatedDeskResource):

    path = 'groups'


class Group(ResourceMixin, resource.DeskResource):

    path = 'groups'

    @base.apimethod
    def group_filters(self, per_page=None, page=None):
        """
        Retrieve a paginated list of all filters for the given group.

        Upstream documentation: http://dev.desk.com/API/groups#list-filters
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'filters')
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def users(self, per_page=None, page=None):
        """
        Retrieve a paginated list of all users for the given group.

        Upstream documentation: http://dev.desk.com/API/groups#list-users
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'users')
        return http.Request('GET', url, params), parsers.parse_json


class Users(ResourceMixin, resource.PaginatedDeskResource):

    path = 'users'


class User(ResourceMixin, resource.DeskResource):

    path = 'users'

    @base.apimethod
    def preferences(self, per_page=None, page=None):
        """
        List all of the user's preferences.

        Upstream documentation: http://dev.desk.com/API/users/#preferences-list
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'preferences')
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def preference(self, preference_id):
        """
        Show a single user preference

        Upstream documentation: http://dev.desk.com/API/users/#preferences-show
        """
        url = '{0}/{1}/{2}'.format(self.get_url(), 'preferences', preference_id)
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def update_preference(self, preference_id, obj):
        """
        Update a user preference

        Upstream documentation: http://dev.desk.com/API/users/#preferences
        """
        url = '{0}/{1}/{2}'.format(self.get_url(), 'preferences', preference_id)
        request = http.Request('PATCH', url, self.wrap_object(obj))
        return request, parsers.parse_json


class SiteSettings(ResourceMixin, resource.PaginatedDeskResource):

    path = 'site_settings'
