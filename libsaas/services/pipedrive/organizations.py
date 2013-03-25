from libsaas import http, parsers
from libsaas.services import base


class OrganizationsResource(base.RESTResource):

    path = 'organizations'


class Organizations(OrganizationsResource):

    @base.apimethod
    def get(self, filter_id=None, start=None, limit=None, sort_by=None,
            sort_mode=None):
        """
        Returns all organizations

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple organizations as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())

        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json

    @base.apimethod
    def find(self, term, start=None, limit=None):
        """
        Searches all organizations by their name.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())
        url = '{0}/find'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class Organization(OrganizationsResource):

    @base.apimethod
    def merge(self, merge_with_id):
        """
        Merges an organization with another organization.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())
        url = '{0}/merge'.format(self.get_url())
        return http.Request('POST', url, params), parsers.parse_json

    @base.apimethod
    def activities(self, start=None, limit=None, done=None, exclude=None):
        """
        Lists activities associated with an organization.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())
        url = '{0}/activities'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def followers(self):
        """
        Lists the followers of an organization.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        url = '{0}/followers'.format(self.get_url())
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def persons(self, start=None, limit=None):
        """
        Lists the persons of an organization.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())
        url = '{0}/persons'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def updates(self, start=None, limit=None):
        """
        Lists updates about an organization.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())
        url = '{0}/updates'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def deals(self, start=None, limit=None):
        """
        Lists deals associated with an organization.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())
        url = '{0}/deals'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def files(self, start=None, limit=None):
        """
        Lists files associated with an organization.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Organizations
        """
        params = base.get_params(None, locals())
        url = '{0}/files'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class OrganizationFieldsResource(base.RESTResource):

    path = 'organizationFields'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class OrganizationFields(OrganizationFieldsResource):

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple activities as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-OrganizationFields
        """
        params = base.get_params(None, locals())

        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json


class OrganizationField(OrganizationFieldsResource):
    pass
