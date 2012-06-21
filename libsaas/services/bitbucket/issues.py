from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Issues(resource.BitBucketResource):

    def __init__(self, parent, user, repo):
        self.parent = parent
        self.user = user
        self.repo = repo

    def get_url(self):
        url = '{0}/repositories/{1}/{2}/issues/'.format(self.parent.get_url(),
                                                    self.user, self.repo)
        return url

    @base.apimethod
    def get(self, search=None, offset=None, limit=None):
        """
        Fetch issues

        :var filter: https://confluence.atlassian.com/display/BITBUCKET/Issues
        """
        params = resource.get_params(('search', 'offset', 'limit'), locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def components(self, id=None):
        """
        Fetch components

        :var id: If setted just the component ID to return
        """
        url = '{0}components/'.format(self.get_url())
        if id is not None:
            url += '{0}/'.format(id)
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def add_component(self, obj):
        """
        Add a component to the issues.

        :var obj: a Python object with the needed params:
            name: the component name
        """
        url = '{0}components/'.format(self.get_url())
        request = http.Request('POST', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def edit_component(self, id, obj):
        """
        Edit a component from the issues.

        :var id: the component ID
        :var obj: a Python object wuth the needed params:
            name: the component name
        """
        url = '{0}components/{1}/'.format(self.get_url(), id)
        request = http.Request('PUT', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete_component(self, id):
        """
        Delete a component from the issues.

        :var id: the component ID
        """
        url = '{0}components/{1}/'.format(self.get_url(), id)
        request = http.Request('DELETE', url)

        return request, parsers.parse_json

    @base.apimethod
    def milestones(self, id=None):
        """
        Fetch milestones

        :var id: If setted just the component ID to return
        """
        url = '{0}milestones/'.format(self.get_url())
        if id is not None:
            url += '{0}/'.format(id)
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def add_milestone(self, obj):
        """
        Add a milestone to the issues.

        :var obj: a Python object with the needed params:
            name: the milestone name
        """
        url = '{0}milestones/'.format(self.get_url())
        request = http.Request('POST', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def edit_milestone(self, id, obj):
        """
        Edit a milestone from the issues.

        :var id: the milestone ID
        :var obj: a Python object wuth the needed params:
            name: the milestone name
        """
        url = '{0}milestones/{1}/'.format(self.get_url(), id)
        request = http.Request('PUT', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete_milestone(self, id):
        """
        Delete a milestone from the issues.

        :var id: the milestone ID
        """
        url = '{0}milestones/{1}/'.format(self.get_url(), id)
        request = http.Request('DELETE', url)

        return request, parsers.parse_json

    @base.apimethod
    def versions(self, id=None):
        """
        Fetch versions

        :var id: If setted just the component ID to return
        """
        url = '{0}versions/'.format(self.get_url())
        if id is not None:
            url += '{0}/'.format(id)
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def add_version(self, obj):
        """
        Add a version to the issues.

        :var obj: a Python object with the needed params:
            name: the version name
        """
        url = '{0}versions/'.format(self.get_url())
        request = http.Request('POST', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def edit_version(self, id, obj):
        """
        Edit a version from the issues.

        :var id: the version ID
        :var obj: a Python object wuth the needed params:
            name: the version name
        """
        url = '{0}versions/{1}/'.format(self.get_url(), id)
        request = http.Request('PUT', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete_version(self, id):
        """
        Delete a version from the issues.

        :var id: the version ID
        """
        url = '{0}versions/{1}/'.format(self.get_url(), id)
        request = http.Request('DELETE', url)

        return request, parsers.parse_json


class Issue(resource.BitBucketResource):

    def __init__(self, parent, user, repo, id=None, comments=None):
        self.parent = parent
        self.user = user
        self.repo = repo
        self.id = id

    def get_url(self):
        url = '{0}/repositories/{1}/{2}/issues/'.format(
                            self.parent.get_url(), self.user, self.repo)
        if self.id is not None:
            url += '{0}/'.format(self.id)

        return url

    @base.apimethod
    def create(self, obj):
        """
        Create a new Issue.

        :var obj: a Python object with the needed params that can be:
            title: The title of the new issue
            content: The content of the new issue
            component: The componen associated with the issue
            milestone: The milestone associated with  the issue
            version: The version associated with the issue
            responsible: The username of the person responsible for the issue
            priority: The priority of the issue. Valid priorities are:
                trivial
                minor
                major
                critical
                blocker
            status: The status of the issue. Val statuses are:
                new
                open
                resolved
                on hold
                invalid
                duplicate
                wontfix
            kind: The kinf of the issue. Valid kinds are:
                bug
                enhancement
                proposal
                task
        """
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def update(self, obj):
        """
        Update an issue.

        :var obj: a Python object with the needed params that are like create
        """
        request = http.Request('PUT', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Delete an issue.
        """
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_json

    @base.apimethod
    def comments(self, id=None):
        """
        Get an issue comments
        """
        url = '{0}comments/'.format(self.get_url())
        if id is not None:
            url += '{0}/'.format(id)

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def add_comment(self, obj):
        """
        Add a new comment to an issue.

        :var obj: a Python object with the needed params
        """
        url = '{0}comments/'.format(self.get_url())
        request = http.Request('POST', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def edit_comment(self, id, obj):
        """
        Edit a comment from an issue.

        :var id: The comment id for the issue.
        :var obj: a Python object with the needed params
        """
        url = '{0}comments/{1}/'.format(self.get_url(), id)
        request = http.Request('PUT', url, self.wrap_object(obj))

        return request, parsers.parse_json

    @base.apimethod
    def delete_comment(self, id):
        """
        Remove a comment from an issue.

        :var id: the ID of the comment to remove from the issue.
        """
        url = '{0}comments/{1}/'.format(self.get_url(), id)

        return http.Request('DELETE', url), parsers.parse_json
