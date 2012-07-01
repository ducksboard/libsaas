from libsaas import http, parsers
from libsaas.services import base

from . import resource, privileges, issues, links, changesets, services


class Repos(resource.BitBucketResource):

    path = 'repositories'

    @base.apimethod
    def get(self, *args, **kwargs):
        """
        Fetch all repositories you have access to.
        """
        url = '{0}/user/repositories/'.format(self.parent.get_url())
        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def search(self, name=None):
        """
        Search for repositories with the given name.
        """
        params = base.get_params(('name', ), locals())
        request = http.Request('GET', self.get_url(), params)

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
        params = base.get_params(('name', 'scm'), locals())
        params['is_private'] = 'true' if is_private else 'false'
        request = http.Request('POST', self.get_url(), params)

        return request, parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Delete a repository.
        """
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_json


class Repo(resource.BitBucketResource):

    def __init__(self, parent, user, repo):
        self.parent = parent
        self.user = user
        self.repo = repo

    def get_url(self):
        return '{0}/repositories/{1}/{2}'.format(self.parent.get_url(),
                                                 self.user, self.repo)

    def require_item(self):
        pass

    def require_collection(self):
        raise base.MethodNotSupported()

    @base.apimethod
    def tags(self):
        """
        Fetch the repository tags.
        """
        url = '{0}/tags/'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json

    @base.apimethod
    def branches(self):
        """
        Fetch the repository branches.
        """
        url = '{0}/branches/'.format(self.get_url())
        request = http.Request('GET', url)

        return request, parsers.parse_json

    @base.apimethod
    def invite(self, user, permission):
        """
        Invite a user to participate in the repository, with the given
        permissions.

        :var user: The email of the user to invite.
        :vartype user: str

        :var permission: The permission to grant (either read or write)
        :vartype permission: str
        """
        url = '{0}/invitations/{1}/{2}/{3}'.format(self.parent.get_url(),
                                                   self.user, self.repo, user)
        params = base.get_params(('permission', ), locals())
        request = http.Request('POST', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def followers(self):
        """
        Fetch the followers of this repo.
        """
        request = http.Request('GET', '{0}/followers/'.format(self.get_url()))

        return request, parsers.parse_json

    @base.apimethod
    def events(self, start=0, limit=15, etype=None):
        """
        Fetch events for this repository.

        :var start: Event start, default is 0.
        :var limit: Event result limit, default is 15.
        :var type: Event type, for example 'issue_comment'.
        """
        params = base.get_params(('start', 'limit', 'etype'), locals())
        url = '{0}/events/'.format(self.get_url())
        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.resource(privileges.RepoPrivileges)
    def privileges(self, specific_user=None):
        """
        Return a resource corresponding to all privileges from this repo,
        either for everyone or for a specific user.
        """
        return privileges.RepoPrivileges(
            self, self.user, self.repo, specific_user)

    @base.resource(issues.RepoIssue)
    def issue(self, id):
        """
        Return a resource corresponding to an issue from this repo.
        """
        return issues.RepoIssue(self, id)

    @base.resource(issues.RepoIssues)
    def issues(self):
        """
        Return a resource corresponding to all issues from this repo.
        """
        return issues.RepoIssues(self)

    @base.resource(links.RepoLink)
    def link(self, id):
        """
        Reurn a resource corresponding to a link from this repo.
        """
        return links.RepoLink(self, id)

    @base.resource(links.RepoLinks)
    def links(self):
        """
        Return a resouce corresponding to all the links from this repo.
        """
        return links.RepoLinks(self)

    @base.resource(changesets.Changeset)
    def changeset(self, changeset_md5):
        """
        Return a resource corresponding to a changeset for this repo.
        """
        return changesets.Changeset(self, changeset_md5)

    @base.resource(changesets.Changesets)
    def changesets(self):
        """
        Return a resource corresponding to all the changesets for this repo.
        """
        return changesets.Changesets(self)

    @base.resource(services.Service)
    def service(self, service_id):
        """
        Return a resource corresponding to one service for this repo.
        """
        return services.Service(self, service_id)

    @base.resource(services.Services)
    def services(self):
        """
        Return a resource corresponding to all the services for this repo.
        """
        return services.Services(self)
