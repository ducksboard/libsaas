import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import bitbucket


class BitbucketTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})
        self.user = 'user'
        self.other = 'another-user'
        self.repo = 'my-repo'

        self.service = bitbucket.BitBucket(self.user, 'password')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://api.bitbucket.org/1.0' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_privileges(self):
        self.service.privileges(self.user).get()
        self.expect('GET', '/privileges/{0}/'.format(self.user))

        self.service.privileges(self.user, repo=self.repo).get()
        self.expect('GET', '/privileges/{0}/{1}/'.format(self.user, self.repo))

        self.service.privileges(
            self.user, repo=self.repo, specificuser=self.other).get()
        self.expect('GET', '/privileges/{0}/{1}/{2}/'.format(
            self.user, self.repo, self.other))

        self.service.privileges(self.user).get(filter='admin')
        self.expect('GET', '/privileges/{0}/'.format(self.user),
                    {'filter': 'admin'})

        self.service.privileges(
            self.user, repo=self.repo, specificuser=self.other).grant('write')
        self.expect('PUT', '/privileges/{0}/{1}/{2}/'.format(
            self.user, self.repo, self.other), '"write"')

        self.service.privileges(
            self.user, repo=self.repo, specificuser=self.other).revoke()
        self.expect('DELETE', '/privileges/{0}/{1}/{2}/'.format(
            self.user, self.repo, self.other))

    def test_emails(self):
        self.service.emails().get()
        self.expect('GET', '/emails')

        self.service.email("my-email@example.org").get()
        self.expect('GET', '/emails/my-email@example.org/')

        self.service.emails().create('my-email@example.org')
        self.expect('PUT', '/emails/my-email@example.org')

        data = {'primary': 'true'}
        self.service.emails().primary('my-email@example.org')
        self.expect('POST', '/emails/my-email@example.org', json.dumps(data))

        self.service.emails().delete('my-email@example.org')
        self.expect('DELETE', '/emails/my-email@example.org')

    def test_changeset(self):
        self.service.changesets('my-user', 'my-repo').get()
        self.expect('GET', '/my-user/my-repo/changesets')

        self.service.changesets('my-user', 'my-repo', commit='f28d56d').get()
        self.expect('GET', '/my-user/my-repo/changesets/f28d56d/diffstat')

        self.service.changesets('my-user', 'my-repo').get(limit=20)
        self.expect('GET', '/my-user/my-repo/changesets',
                    {'start': 'tip', 'limit': 20})

    def test_events(self):
        self.service.events(user='my-user').get()
        self.expect('GET', '/users/my-user/events/')

        self.service.events(user='my-user').get(start=10, limit=20)
        self.expect('GET', '/users/my-user/events/',
                    {'start': 10, 'limit': 20})

        self.service.events(user='my-user', repo='my-repo').get()
        self.expect('GET', '/repositories/my-user/my-repo/events/')

        self.service.events(user='my-user', repo='my-repo').get(
            start=10, limit=20, etype='issue_comment')
        self.expect('GET', '/repositories/my-user/my-repo/events/',
                    {'etype': 'issue_comment', 'start': 10, 'limit': 20})

    def test_followers(self):
        self.service.followers(user='my-user', repo='my-repo').get()
        self.expect('GET', '/repositories/my-user/my-repo/followers/')

        self.service.followers(
            user='my-user', repo='my-repo', issue='my-issue').get()
        self.expect('GET',
            '/repositories/my-user/my-repo/issues/my-issue/followers/')

        self.service.followers().follows()
        self.expect('GET', '/user/follows/')

    def test_groups(self):
        self.service.groups('my-user').get()
        self.expect('GET', '/groups/my-user')

        self.service.groups('my-user@example.org').get()
        self.expect('GET', '/groups/my-user@example.org')

        data = {'name': 'my-group'}
        self.service.group('my-user').create(data)
        self.expect('POST', '/groups/my-user', json.dumps(data))

        data = {'name': 'my-other-group', 'auto-add': 'true'}
        self.service.group('my-user', 'my-group').update(data)
        self.expect('PUT', '/groups/my-user/my-group', json.dumps(data))

        self.service.group('my-user', 'my-group').delete()
        self.expect('DELETE', '/groups/my-user/my-group')

        self.service.group('my-user', 'my-group').get()
        self.expect('GET', '/groups/my-user/my-group/members')

        self.service.group('my-user', 'my-group').add('another-user')
        self.expect('PUT', '/groups/my-user/my-group/members/another-user')

        self.service.group('my-user', 'my-group').delete('another-user')
        self.expect('DELETE', '/groups/my-user/my-group/members/another-user')

    def test_groups_privileges(self):
        self.service.group_privileges('my-user', 'my-repo').get()
        self.expect('GET', '/group-privileges/my-user/my-repo/')

        self.service.group_privileges('my-user').get()
        self.expect('GET', '/group-privileges/my-user/')

        self.service.group_privileges('my-user').get(filter='admin')
        self.expect('GET', '/group-privileges/my-user/',
                                        {'filter': 'admin', 'private': False})

        self.service.group_privileges('my-user', 'my-group').grant(
                                                            privilege='read')
        self.expect('PUT', '/group-privileges/my-user/my-group/', '"read"')

    def test_invitation(self):
        self.service.invitations(
            'my-user', 'my-repo', 'invited@example.org').invite('write')
        self.expect('PUT', '/invitations/my-user/my-repo/invited@example.org',
                    '"write"')

    def test_issues(self):
        self.service.issues('my-user', 'my-repo').get()
        self.expect('GET', '/repositories/my-user/my-repo/issues/')

        self.service.issues('my-user', 'my-repo').get(
                                                search='easy_install')
        self.expect('GET', '/repositories/my-user/my-repo/issues/',
                                                {'search': 'easy_install'})

        data = {
            'title': 'my-issue',
            'content': 'my-issue-content',
            'component': 'my-issue-component',
            'milestone': '2',
            'version': '2.0',
            'responsible': 'some-user',
            'priotiry': 'minor',
            'status': 'new',
            'kid': 'bug'
        }
        self.service.issue('my-user', 'my-repo').create(data)
        self.expect('POST', '/repositories/my-user/my-repo/issues/',
                                                            json.dumps(data))

        self.service.issue('my-user', 'my-repo', '1000').update(data)
        self.expect('PUT', '/repositories/my-user/my-repo/issues/1000/',
                                                            json.dumps(data))

        self.service.issue('my-user', 'my-repo', '1000').delete()
        self.expect('DELETE', '/repositories/my-user/my-repo/issues/1000/')

    def test_issues_comments(self):
        self.service.issue('my-user', 'my-repo', '1000').comments()
        self.expect('GET',
            '/repositories/my-user/my-repo/issues/1000/comments/')

        self.service.issue('my-user', 'my-repo', '1000').comments('12345')
        self.expect('GET',
            '/repositories/my-user/my-repo/issues/1000/comments/12345/')

        data = {'content': 'This is my comment content'}
        self.service.issue('my-user', 'my-repo', '1000').add_comment(data)
        self.expect('POST',
            '/repositories/my-user/my-repo/issues/1000/comments/',
                                                            json.dumps(data))

        self.service.issue('my-user', 'my-repo', '1000').edit_comment('1',
                                                                        data)
        self.expect('PUT',
            '/repositories/my-user/my-repo/issues/1000/comments/1/',
                                                            json.dumps(data))

        self.service.issue('my-user', 'my-repo', '1000').delete_comment('1')
        self.expect('DELETE',
                    '/repositories/my-user/my-repo/issues/1000/comments/1/')

    def test_issues_components(self):
        self.service.issues('my-user', 'my-repo').components()
        self.expect('GET', '/repositories/my-user/my-repo/issues/components/')

        self.service.issues('my-user', 'my-repo').components('42')
        self.expect('GET',
                        '/repositories/my-user/my-repo/issues/components/42/')

        data = {'name': 'My new issues component'}
        self.service.issues('my-user', 'my-repo').add_component(data)
        self.expect('POST', '/repositories/my-user/my-repo/issues/components/',
                                                            json.dumps(data))

        self.service.issues('my-user', 'my-repo').edit_component('42', data)
        self.expect('PUT',
            '/repositories/my-user/my-repo/issues/components/42/',
            json.dumps(data)
        )

        self.service.issues('my-user', 'my-repo').delete_component('42')
        self.expect('DELETE',
                        '/repositories/my-user/my-repo/issues/components/42/')

    def test_issues_milestones(self):
        self.service.issues('my-user', 'my-repo').milestones()
        self.expect('GET', '/repositories/my-user/my-repo/issues/milestones/')

        self.service.issues('my-user', 'my-repo').milestones('42')
        self.expect('GET',
                        '/repositories/my-user/my-repo/issues/milestones/42/')

        data = {'name': 'My new issues component'}
        self.service.issues('my-user', 'my-repo').add_milestone(data)
        self.expect('POST', '/repositories/my-user/my-repo/issues/milestones/',
                                                            json.dumps(data))

        self.service.issues('my-user', 'my-repo').edit_milestone('42', data)
        self.expect('PUT',
            '/repositories/my-user/my-repo/issues/milestones/42/',
            json.dumps(data)
        )

        self.service.issues('my-user', 'my-repo').delete_milestone('42')
        self.expect('DELETE',
                        '/repositories/my-user/my-repo/issues/milestones/42/')

    def test_issues_versions(self):
        self.service.issues('my-user', 'my-repo').versions()
        self.expect('GET', '/repositories/my-user/my-repo/issues/versions/')

        self.service.issues('my-user', 'my-repo').versions('42')
        self.expect('GET',
                        '/repositories/my-user/my-repo/issues/versions/42/')

        data = {'name': 'My new issues component'}
        self.service.issues('my-user', 'my-repo').add_version(data)
        self.expect('POST', '/repositories/my-user/my-repo/issues/versions/',
                                                            json.dumps(data))

        self.service.issues('my-user', 'my-repo').edit_version('42', data)
        self.expect('PUT',
            '/repositories/my-user/my-repo/issues/versions/42/',
            json.dumps(data)
        )

        self.service.issues('my-user', 'my-repo').delete_version('42')
        self.expect('DELETE',
                        '/repositories/my-user/my-repo/issues/versions/42/')

    def test_repositories(self):
        self.service.repositories('my-user').get()
        self.expect('GET', '/my-user/repositories/')

        self.service.repositories().get(name='django')
        self.expect('GET', '/repositories/', {'name': 'django'})

        self.service.repositories('my-user', 'my-repo').tags()
        self.expect('GET', '/repositories/my-user/my-repo/tags/')

        self.service.repositories('my-user', 'my-repo').branches()
        self.expect('GET', '/repositories/my-user/my-repo/branches/')

        self.service.repositories().create(name='my-repo', scm='git')
        self.expect('POST', '/repositories/',
                                json.dumps({"name": "my-repo", "scm": "git"}))

        self.service.repositories('my-user', 'my-repo').delete()
        self.expect('DELETE', '/repositories/my-user/my-repo/')

    def test_repository_links(self):
        self.service.repository('my-user', 'my-repo').links()
        self.expect('GET', '/repositories/my-user/my-repo/links/')

        self.service.repository('my-user', 'my-repo').links(id='42')
        self.expect('GET', '/repositories/my-user/my-repo/links/42/')

        data = {
            'handler': 'jira', 'link_url': 'http://test.com', 'link_key': 'PRJ'
        }
        self.service.repository('my-user', 'my-repo').add(data)
        self.expect('POST', '/repositories/my-user/my-repo/links/',
                                                            json.dumps(data))

        self.service.repository('my-user', 'my-repo').edit('42', data)
        self.expect('PUT', '/repositories/my-user/my-repo/links/42/',
                                                            json.dumps(data))

        self.service.repository('my-user', 'my-repo').delete('42')
        self.expect('DELETE', '/repositories/my-user/my-repo/links/42/')

    def test_services(self):
        self.service.services('my-user', 'my-repo').get()
        self.expect('GET', '/repositories/my-user/my-repo/services/')

        self.service.service('my-user', 'my-repo', '1').get()
        self.expect('GET', '/repositories/my-user/my-repo/services/1/')

        data = {'type': 'post', 'URL': 'http://test.org/post'}
        self.service.services('my-user', 'my-repo').add(data)
        self.expect('POST', '/repositories/my-user/my-repo/services/',
                                                            json.dumps(data))

        self.service.services('my-user', 'my-repo').edit('1', data)
        self.expect('PUT', '/repositories/my-user/my-repo/services/1/',
                                                            json.dumps(data))

        self.service.services('my-user', 'my-repo').delete(id='1')
        self.expect('DELETE', '/repositories/my-user/my-repo/services/1/')
