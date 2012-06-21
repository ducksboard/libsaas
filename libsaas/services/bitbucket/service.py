import json

from libsaas import http
from libsaas.filters import auth
from libsaas.services import base

from . import (
    privileges, emails, changesets, events, followers, groups, issues,
    repositories, services
)


class BitBucket(base.Resource):
    """
    """
    def __init__(self, username, password=None):
        """
        Create a BitBucket service.

        :var username: The username for the authenticated user.
        :vartype username: str

        :var password: The password for the authenticated user.
        :vartype password: str
        """
        self.apiroot = 'https://api.bitbucket.org/1.0'

        self.add_filter(auth.BasicAuth(username, password))
        self.add_filter(self.use_json)

    def add_authorization(self, request):
        request.headers['Authorization'] = 'token {0}'.format(self.oauth_token)

    def use_json(self, request):
        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = json.dumps(request.params)

    def get_url(self):
        return self.apiroot

    @base.resource(privileges.Invitations)
    def invitations(self, user, group, address):
        """
        Perform invitations.
        """
        return privileges.Invitations(self, user, group, address)

    @base.resource(privileges.Privileges)
    def privileges(self, user, repo=None, specificuser=None):
        """
        Return the resource corresponding to all the privileges.
        """
        return privileges.Privileges(self, user, repo, specificuser)

    @base.resource(emails.Email)
    def email(self, email_id):
        """
        Return the resource corresponding to a single email
        """
        return emails.Email(self, email_id)

    @base.resource(emails.Emails)
    def emails(self):
        """
        Return the resource corresponding to all the emails
        """
        return emails.Emails(self)

    @base.resource(changesets.Changesets)
    def changesets(self, user, repo, commit=None):
        """
        Return the resource corresponding to all the changesets
        """
        return changesets.Changesets(self, user, repo, commit)

    @base.resource(events.Events)
    def events(self, user=None, repo=None):
        """
        Return the resource corresponding to all the events
        """
        return events.Events(self, user, repo)

    @base.resource(followers.Followers)
    def followers(self, user=None, repo=None, issue=None):
        """
        Return the resource corresponding to all the followers
        """
        return followers.Followers(self, user, repo, issue)

    @base.resource(groups.GroupPrivileges)
    def group_privileges(self, user=None, group=None):
        return groups.GroupPrivileges(self, user, group)

    @base.resource(groups.Group)
    def group(self, user, group=None):
        """
        Return the resource corresponding to one group
        """
        return groups.Group(self, user, group)

    @base.resource(groups.Groups)
    def groups(self, user):
        """
        Return the resource corresponding to all the groups
        """
        return groups.Groups(self, user)

    @base.resource(issues.Issue)
    def issue(self, user, repo, id=None):
        """
        Return the resource corresponding to one issue
        """
        return issues.Issue(self, user, repo, id)

    @base.resource(issues.Issues)
    def issues(self, user, repo):
        """
        Return the resource corresponding to all the issues
        """
        return issues.Issues(self, user, repo)

    @base.resource(repositories.Repository)
    def repository(self, user, repo):
        """
        Return the resource corresponding to one repository
        """
        return repositories.Repository(self, user, repo)

    @base.resource(repositories.Repositories)
    def repositories(self, user=None, repo=None):
        """
        Return the resource corresponding to all the repositories
        """
        return repositories.Repositories(self, user, repo)

    @base.resource(services.Service)
    def service(self, user, repo, id):
        """
        Return the resource corresponding to one of the repository services
        """
        return services.Service(self, user, repo, id)

    @base.resource(services.Services)
    def services(self, user, repo):
        """
        Return the resource corresponding to all the repository services
        """
        return services.Services(self, user, repo)



Bitbucket = BitBucket
