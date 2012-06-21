from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Repositories(resource.BitBucketResource):

    def __init__(self, parent, user=None, repo=None):
        self.parent = parent
        self.user = user
        self.repo = repo

    def get_url(self):
        url = '{0}'.format(self.parent.get_url())
        if self.user is not None and self.repo is not None:
            url += '/repositories/{0}/{1}/'.format(self.user, self.repo)
        else:
            if self.user is not None:
                url += '/{0}'.format(self.user)
            if self.repo is not None:
                url += '/{0}'.format(self.repo)
            url += '/repositories/'

        return url

    @base.apimethod
    def get(self, name=None):
        """
        Fetch repositories
        """
        params = resource.get_params(('name', ), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def tags(self):
        """
        Fetch the repository tags
        """
        url = '{0}tags/'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json

    @base.apimethod
    def branches(self):
        """
        Fetch the repository branches
        """
        url = '{0}branches/'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json

    @base.apimethod
    def create(self, name, scm=None, is_private=False):
        """
        Create a new repository.

        :var name: the repository name.
        :var scm: the type of repository you want to create, can be:
            git: for git repository
            hg: for mercurial repository
        """
        params = resource.get_params(('name', 'scm'), locals())
        if is_private:
            params['is_private'] = True
        request = http.Request('POST', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Delete a repository.
        """
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_json


class Repository(resource.BitBucketResource):

    def __init__(self, parent, user, repo):
        self.parent = parent
        self.user = user
        self.repo = repo

    def get_url(self):
        return '{0}/repositories/{1}/{2}/'.format(self.parent.get_url(),
                                                        self.user, self.repo)

    @base.apimethod
    def links(self, id=None):
        """
        Fetch repository links
        """
        links = 'links/'
        if id is not None:
            links += '{0}/'.format(id)

        request = http.Request('GET', self.get_url() + links)

        return request, parsers.parse_json

    @base.apimethod
    def add(self, obj):
        """
        Add new link to the repository.

        :var obj: a Python object with the required data
        """
        url = '{0}links/'.format(self.get_url())
        request = http.Request('POST', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def edit(self, id, obj):
        """
        Add new link to the repository.

        :var id: the link id
        :var obj: a Python object with the required data
        """
        url = '{0}links/{1}/'.format(self.get_url(), id)
        request = http.Request('PUT', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete(self, id):
        """
        Add new link to the repository.

        :var id: the link id
        """
        url = '{0}links/{1}/'.format(self.get_url(), id)
        request = http.Request('DELETE', url)

        return request, parsers.parse_json
