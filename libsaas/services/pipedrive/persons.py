from libsaas import http, parsers
from libsaas.services import base


class PersonsResource(base.RESTResource):

    path = 'persons'


class Persons(PersonsResource):

    @base.apimethod
    def get(self, filter_id=None, start=None, limit=None, sort_by=None,
            sort_mode=None):
        """
        Returns all persons

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        params = base.get_params(None, locals())

        return http.Request('GET', self.get_url(), params), parsers.parse_json

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple persons as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        params = base.get_params(None, locals())
        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json

    @base.apimethod
    def find(self, term, org_id=None, start=None, limit=None):
        """
        Searches all persons by their name.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        params = base.get_params(None, locals())
        url = '{0}/find'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class Person(PersonsResource):

    @base.apimethod
    def merge(self, merge_with_id):
        """
        Merges a person with another person.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        params = base.get_params(None, locals())
        url = '{0}/merge'.format(self.get_url())
        return http.Request('POST', url, params), parsers.parse_json

    @base.apimethod
    def activities(self, start=None, limit=None, done=None, exclude=None):
        """
        Lists activities associated with a person.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        params = base.get_params(None, locals())
        url = '{0}/activities'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def followers(self):
        """
        Lists the followers of a person.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        url = '{0}/followers'.format(self.get_url())
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def products(self, start=None, limit=None):
        """
        Lists the products of a person.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-products
        """
        params = base.get_params(None, locals())
        url = '{0}/products'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def updates(self, start=None, limit=None):
        """
        Lists updates about a person.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        params = base.get_params(None, locals())
        url = '{0}/updates'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def deals(self, start=None, limit=None):
        """
        Lists deals associated with a person.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        params = base.get_params(None, locals())
        url = '{0}/deals'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def files(self, start=None, limit=None):
        """
        Lists files associated with a person.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-Persons
        """
        params = base.get_params(None, locals())
        url = '{0}/files'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json


class PersonFieldsResource(base.RESTResource):

    path = 'personFields'

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()


class PersonFields(PersonFieldsResource):

    @base.apimethod
    def delete(self, ids):
        """
        Marks multiple activities as deleted.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-PersonFields
        """
        params = base.get_params(None, locals())
        request = http.Request('DELETE', self.get_url(), params)
        return request, parsers.parse_json


class PersonField(PersonFieldsResource):
    pass
