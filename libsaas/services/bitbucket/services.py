from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Services(resource.BitBucketResource):

    def __init__(self, parent, user, repo):
        self.parent = parent
        self.user = user
        self.repo = repo

    def get_url(self):
        url = '{0}/repositories/{1}/{2}/services/'.format(
                                self.parent.get_url(), self.user, self.repo)

        return url

    @base.apimethod
    def get(self):
        """
        Fetch repository services
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json

    @base.apimethod
    def add(self, obj):
        """
        Adds a new service to a repository
        :var obj: a Python object with the needed data. Available types:
            POST: fields -> URL
            FogBugz: fields -> Repository ID, CVSSubmit URL
            Basecamp: fields -> Username, Password, Discussion URL
            Lighthouse: fields -> Project ID, API Key, Subdomain
            CIA.vc fields -> Module, Project
            Issues fields -> None
            Email fields -> Email
            Email Diff fields -> Email
            FriendFeed fields -> Username, Remote Key, Format
            Rietveld fields -> Email, Password, URL
            Superfeedr fields -> None
            Geocommit fields -> None
            Pivotal Tracker fields -> Token
        """
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def edit(self, id, obj):
        """
        Edit a service from a repository
        :var id: the service id
        :var obj: a Python object with the needed data. Available types:
            POST: fields -> URL
            FogBugz: fields -> Repository ID, CVSSubmit URL
            Basecamp: fields -> Username, Password, Discussion URL
            Lighthouse: fields -> Project ID, API Key, Subdomain
            CIA.vc fields -> Module, Project
            Issues fields -> None
            Email fields -> Email
            Email Diff fields -> Email
            FriendFeed fields -> Username, Remote Key, Format
            Rietveld fields -> Email, Password, URL
            Superfeedr fields -> None
            Geocommit fields -> None
            Pivotal Tracker fields -> Token
        """
        url = '{0}{1}/'.format(self.get_url(), id)
        request = http.Request('PUT', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete(self, id):
        """
        Delete a service from a repository
        :var id: the service id
        """
        url = '{0}{1}/'.format(self.get_url(), id)
        request = http.Request('DELETE', url)

        return request, parsers.parse_json


class Service(resource.BitBucketResource):

    def __init__(self, parent, user, repo, id):
        self.parent = parent
        self.user = user
        self.repo = repo
        self.id = id

    def get_url(self):
        url = '{0}/repositories/{1}/{2}/services/{3}/'.format(
                        self.parent.get_url(), self.user, self.repo, self.id)

        return url

    @base.apimethod
    def get(self):
        """
        Fetch repository services
        """
        request = http.Request('GET', self.get_url())

        return request, parsers.parse_json
