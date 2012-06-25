import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import bitbucket


class BitbucketTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = bitbucket.BitBucket('myuser', 'password')

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

    def test_repos(self):
        self.service.repos('myuser').get()
        self.expect('GET', '/myuser/repositories/')

        self.service.repos().get(name='django')
        self.expect('GET', '/repositories/', {'name': 'django'})

        self.service.repos('myuser', 'myrepo').tags()
        self.expect('GET', '/repositories/myuser/myrepo/tags/')

        self.service.repos('myuser', 'myrepo').branches()
        self.expect('GET', '/repositories/myuser/myrepo/branches/')

        self.service.repos().create(name='myrepo', scm='git')
        self.expect('POST', '/repositories/',
                    json.dumps({"name": "myrepo", "scm": "git"}))

        self.service.repos('myuser', 'myrepo').delete()
        self.expect('DELETE', '/repositories/myuser/myrepo/')

    def test_repo_links(self):
        self.service.repo('myuser', 'myrepo').links().get()
        self.expect('GET', '/repositories/myuser/myrepo/links')

        self.service.repo('myuser', 'myrepo').link(42).get()
        self.expect('GET', '/repositories/myuser/myrepo/links/42')

        data = {
            'handler': 'jira', 'link_url': 'http://test.com', 'link_key': 'PRJ'
        }
        self.service.repo('myuser', 'myrepo').links().create(data)
        self.expect('POST', '/repositories/myuser/myrepo/links',
                    json.dumps(data))

        self.service.repo('myuser', 'myrepo').link(42).update(data)
        self.expect('PUT', '/repositories/myuser/myrepo/links/42',
                    json.dumps(data))

        self.service.repo('myuser', 'myrepo').link(42).delete()
        self.expect('DELETE', '/repositories/myuser/myrepo/links/42')

    def test_repo_privileges(self):
        self.service.repo('myuser', 'myrepo').privileges().get()
        self.expect('GET', '/privileges/myuser/myrepo/')

        self.service.repo('myuser', 'myrepo').privileges('otheruser').get()
        self.expect('GET', '/privileges/myuser/myrepo/otheruser/')

        self.service.repo('myuser', 'myrepo').privileges().get(filter='write')
        self.expect('GET', '/privileges/myuser/myrepo/', {'filter': 'write'})

        self.service.repo(
                    'myuser', 'myrepo').privileges('otheruser').grant('write')
        self.expect('PUT', '/privileges/myuser/myrepo/otheruser/',
                    json.dumps({'body': 'write'}))

        self.service.repo('myuser', 'myrepo').privileges('otheruser').revoke()
        self.expect('DELETE', '/privileges/myuser/myrepo/otheruser/')

        self.service.repo('myuser', 'myrepo').privileges().revoke()
        self.expect('DELETE', '/privileges/myuser/myrepo/')

        self.service.repo('myuser').privileges().revoke()
        self.expect('DELETE', '/privileges/myuser/')

    def test_repo_issues(self):
        self.service.repo('myuser', 'myrepo').issues().get()
        self.expect('GET', '/repositories/myuser/myrepo/issues')

        self.service.repo('myuser', 'myrepo').issue(1000).get()
        self.expect('GET', '/repositories/myuser/myrepo/issues/1000')

        self.service.repo('myuser', 'myrepo').issues().get(
                                                        search='easy_install')
        self.expect('GET', '/repositories/myuser/myrepo/issues',
                    {'search': 'easy_install'})

        self.service.repo('myuser', 'myrepo').issues().filter(
                          title=('~some_title', '!~another_title'))
        self.expect('GET',
                    '/repositories/myuser/myrepo/issues?title=~some_title'
                    '&title=!~another_title')

        self.service.repo('myuser', 'myrepo').issues().get(start='15')
        self.expect('GET', '/repositories/myuser/myrepo/issues',
                    {'start': '15'})

        self.service.repo('myuser', 'myrepo').issues().get(limit='10')
        self.expect('GET', '/repositories/myuser/myrepo/issues',
                    {'limit': '10'})

        self.service.repo('myuser', 'myrepo').issues().get(
                                                        start='15', limit='10')
        self.expect('GET', '/repositories/myuser/myrepo/issues',
                    {'start': '15', 'limit': '10'})

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
        self.service.repo('myuser', 'myrepo').issues().create(data)
        self.expect('POST', '/repositories/myuser/myrepo/issues',
                    json.dumps(data))

        self.service.repo('myuser', 'myrepo').issue(1000).update(data)
        self.expect('PUT', '/repositories/myuser/myrepo/issues/1000',
                    json.dumps(data))

        self.service.repo('myuser', 'myrepo').issue(1000).delete()
        self.expect('DELETE', '/repositories/myuser/myrepo/issues/1000')

    def test_issues_comments(self):
        self.service.repo('myuser', 'myrepo').issue(1000).comments().get()
        self.expect('GET',
            '/repositories/myuser/myrepo/issues/1000/comments')

        self.service.repo('myuser', 'myrepo').issue(1000).comment(75468).get()
        self.expect('GET',
                    '/repositories/myuser/myrepo/issues/1000/comments/75468')

        data = {'content': 'This is my comment content'}
        self.service.repo(
                        'myuser', 'myrepo').issue(1000).comments().create(data)
        self.expect('POST',
                    '/repositories/myuser/myrepo/issues/1000/comments',
                    json.dumps(data)
        )

        self.service.repo(
                    'myuser', 'myrepo').issue(1000).comment(75468).update(data)
        self.expect('PUT',
                    '/repositories/myuser/myrepo/issues/1000/comments/75468',
                    json.dumps(data))

        self.service.repo('myuser', 'myrepo').issue(10).comment(75468).delete()
        self.expect('DELETE',
                    '/repositories/myuser/myrepo/issues/10/comments/75468')

    def test_issues_components(self):
        self.service.repo('myuser', 'myrepo').issues().components().get()
        self.expect('GET', '/repositories/myuser/myrepo/issues/components')

        self.service.repo('myuser', 'myrepo').issues().component(42).get()
        self.expect('GET',
                    '/repositories/myuser/myrepo/issues/components/42')

        data = {'name': 'My new issues component'}
        self.service.repo(
                    'myuser', 'myrepo').issues().components().create(data)
        self.expect('POST', '/repositories/myuser/myrepo/issues/components',
                    json.dumps(data))

        self.service.repo(
                    'myuser', 'myrepo').issues().component(42).update(data)
        self.expect('PUT',
                    '/repositories/myuser/myrepo/issues/components/42',
                    json.dumps(data)
        )

        self.service.repo('myuser', 'myrepo').issues().component(42).delete()
        self.expect('DELETE',
                        '/repositories/myuser/myrepo/issues/components/42')

    def test_issues_milestones(self):
        self.service.repo('myuser', 'myrepo').issues().milestones().get()
        self.expect('GET', '/repositories/myuser/myrepo/issues/milestones')

        self.service.repo('myuser', 'myrepo').issues().milestone(42).get()
        self.expect('GET',
                        '/repositories/myuser/myrepo/issues/milestones/42')

        data = {'name': 'My new issues component'}
        self.service.repo(
            'myuser', 'myrepo').issues().milestones().create(data)
        self.expect('POST', '/repositories/myuser/myrepo/issues/milestones',
                                                            json.dumps(data))

        self.service.repo(
            'myuser', 'myrepo').issues().milestone(42).update(data)
        self.expect('PUT',
            '/repositories/myuser/myrepo/issues/milestones/42',
            json.dumps(data)
        )

        self.service.repo('myuser', 'myrepo').issues().milestone(42).delete()
        self.expect('DELETE',
                        '/repositories/myuser/myrepo/issues/milestones/42')

    def test_issues_versions(self):
        self.service.repo('myuser', 'myrepo').issues().versions().get()
        self.expect('GET', '/repositories/myuser/myrepo/issues/versions')

        self.service.repo('myuser', 'myrepo').issues().version(42).get()
        self.expect('GET',
                        '/repositories/myuser/myrepo/issues/versions/42')

        data = {'name': 'My new issues component'}
        self.service.repo('myuser', 'myrepo').issues().versions().create(data)
        self.expect('POST', '/repositories/myuser/myrepo/issues/versions',
                                                            json.dumps(data))

        self.service.repo('myuser', 'myrepo').issues().version(42).update(data)
        self.expect('PUT',
            '/repositories/myuser/myrepo/issues/versions/42',
            json.dumps(data)
        )

        self.service.repo('myuser', 'myrepo').issues().version(42).delete()
        self.expect('DELETE',
                        '/repositories/myuser/myrepo/issues/versions/42')

    def test_invitation(self):
        self.service.invitations('myuser', 'myrepo').invite(
                                 'invited@example.org', permission='write')
        self.expect('PUT', '/invitations/myuser/myrepo/invited@example.org',
                    json.dumps({'permission': 'write'}))

    def test_emails(self):
        self.service.emails().get()
        self.expect('GET', '/emails')

        self.service.email('myemail@example.org').get()
        self.expect('GET', '/emails/myemail@example.org/')

        self.service.emails().create('myemail@example.org')
        self.expect('PUT', '/emails/myemail@example.org')

        data = {'primary': 'true'}
        self.service.email('myemail@example.org').primary()
        self.expect('POST', '/emails/myemail@example.org/', json.dumps(data))

        self.service.email('myemail@example.org').delete()
        self.expect('DELETE', '/emails/myemail@example.org/')

    def test_changeset(self):
        self.service.repo('myuser', 'myrepo').changesets().get()
        self.expect('GET', '/repositories/myuser/myrepo/changesets')

        self.service.repo('myuser', 'myrepo').changeset('f28d56').get()
        self.expect('GET',
                    '/repositories/myuser/myrepo/changesets/f28d56')

        self.service.repo('myuser', 'myrepo').changeset('f28d56').diffstat()
        self.expect('GET',
                    '/repositories/myuser/myrepo/changesets/f28d56/diffstat')

        self.service.repo('myuser', 'myrepo').changesets().get(limit=20)
        self.expect('GET', '/repositories/myuser/myrepo/changesets',
                    {'start': 'tip', 'limit': 20})

    def test_events(self):
        self.service.user('myuser').events().get()
        self.expect('GET', '/users/myuser/events')

        self.service.user('myuser').events().get(start=10, limit=20)
        self.expect('GET', '/users/myuser/events', {'start': 10, 'limit': 20})

        self.service.repo('myuser', 'myrepo').events().get()
        self.expect('GET', '/repositories/myuser/myrepo/events')

        self.service.repo('myuser', 'myrepo').events().get(
                          start=10, limit=20, etype='issue_comment')
        self.expect('GET', '/repositories/myuser/myrepo/events',
                    {'etype': 'issue_comment', 'start': 10, 'limit': 20})

    def test_followers(self):
        self.service.user('myuser').followers().get()
        self.expect('GET', '/users/myuser/followers')

        self.service.repo('myuser', 'myrepo').followers().get()
        self.expect('GET', '/repositories/myuser/myrepo/followers')

        self.service.repo('myuser', 'myrepo').issue(1245).followers().get()
        self.expect('GET', '/repositories/myuser/myrepo/issues/1245/followers')

        self.service.user().follows()
        self.expect('GET', '/user/follows')

    def test_groups(self):
        self.service.groups('myuser').get()
        self.expect('GET', '/groups/myuser')

        self.service.groups('myuser@example.org').get()
        self.expect('GET', '/groups/myuser@example.org')

        data = {'name': 'my-group'}
        self.service.group('myuser').create(data)
        self.expect('POST', '/groups/myuser', json.dumps(data))

        data = {'name': 'my-other-group', 'auto-add': 'true'}
        self.service.group('myuser', 'my-group').update(data)
        self.expect('PUT', '/groups/myuser/my-group', json.dumps(data))

        self.service.group('myuser', 'my-group').delete()
        self.expect('DELETE', '/groups/myuser/my-group')

        self.service.group('myuser', 'my-group').get()
        self.expect('GET', '/groups/myuser/my-group/members')

        self.service.group('myuser', 'my-group').add('another-user')
        self.expect('PUT', '/groups/myuser/my-group/members/another-user')

        self.service.group('myuser', 'my-group').delete('another-user')
        self.expect('DELETE', '/groups/myuser/my-group/members/another-user')

    def test_groups_privileges(self):
        self.service.group_privileges('myuser', 'myrepo').get()
        self.expect('GET', '/group-privileges/myuser/myrepo/')

        self.service.group_privileges('myuser').get()
        self.expect('GET', '/group-privileges/myuser/')

        self.service.group_privileges('myuser').get(filter='admin')
        self.expect('GET', '/group-privileges/myuser/',
                                        {'filter': 'admin', 'private': False})

        self.service.group_privileges('myuser', 'my-group').grant(
                                                            privilege='read')
        self.expect('PUT', '/group-privileges/myuser/my-group/', '"read"')

    def test_services(self):
        self.service.repo('myuser', 'myrepo').services().get()
        self.expect('GET', '/repositories/myuser/myrepo/services')

        self.service.repo('myuser', 'myrepo').service(1).get()
        self.expect('GET', '/repositories/myuser/myrepo/services/1')

        data = {'type': 'post', 'URL': 'http://test.org/post'}
        self.service.repo('myuser', 'myrepo').services().create(data)
        self.expect('POST', '/repositories/myuser/myrepo/services',
                                                            json.dumps(data))

        self.service.repo('myuser', 'myrepo').service(1).update(data)
        self.expect('PUT', '/repositories/myuser/myrepo/services/1',
                                                            json.dumps(data))

        self.service.repo('myuser', 'myrepo').service(1).delete()
        self.expect('DELETE', '/repositories/myuser/myrepo/services/1')
