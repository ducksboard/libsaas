import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import base, github


class GithubTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = github.GitHub('my-token')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://api.github.com' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_auth(self):
        service = github.GitHub('a-token')
        service.user().get()
        self.expect('GET', '/user', {}, {'Authorization': 'token a-token'})

        service = github.GitHub('user', 'password')
        service.user().get()
        self.expect('GET', '/user', {}, {'Authorization':
                                             'Basic dXNlcjpwYXNzd29yZA=='})

    def test_gists(self):
        self.service.gists().get()
        self.expect('GET', '/gists')

        self.service.gists().public()
        self.expect('GET', '/gists/public')

        self.service.gists().starred()
        self.expect('GET', '/gists/starred')

        self.service.gist('12345678').get()
        self.expect('GET', '/gists/12345678')

        data = {'x': 'x'}
        self.service.gists().create(data)
        self.expect('POST', '/gists', json.dumps(data))

        self.service.gist('12345678').update(data)
        self.expect('PATCH', '/gists/12345678', json.dumps(data))

        self.service.gist('12345678').star()
        self.expect('PUT', '/gists/12345678/star')
        self.assertTrue(self.executor.request.params)

        self.service.gist('12345678').unstar()
        self.expect('DELETE', '/gists/12345678/star')

        self.executor.set_response(b'', 204, {})
        res = self.service.gist('12345678').is_starred()
        self.expect('GET', '/gists/12345678/star')
        self.assertTrue(res)

        self.executor.set_response(b'', 404, {})
        res = self.service.gist('12345678').is_starred()
        self.assertFalse(res)

        self.executor.set_response(b'{}', 200, {})
        self.service.gist('12345678').fork()
        self.expect('POST', '/gists/12345678/fork')

        self.service.gist('12345678').delete()
        self.expect('DELETE', '/gists/12345678')

    def test_gist_comments(self):
        self.service.gist('12345678').comments().get()
        self.expect('GET', '/gists/12345678/comments')

        self.service.gists().comment('123').get()
        self.expect('GET', '/gists/comments/123')

        self.service.gists().comment('123').get('html')
        self.expect('GET', '/gists/comments/123',
                    headers={'Accept': 'application/vnd.github.v3.html+json',
                             'Authorization': 'token my-token'})

        self.service.gist('12345678').comments().create('yo')
        self.expect('POST', '/gists/12345678/comments',
                    json.dumps({'body': 'yo'}))

        self.service.gists().comment('123').update('yo')
        self.expect('PATCH', '/gists/comments/123',
                    json.dumps({'body': 'yo'}))

        self.service.gists().comment('123').delete()
        self.expect('DELETE', '/gists/comments/123')

    def test_issues(self):
        self.service.issues().get(filter='mentioned',
                                  sort='updated', format='text')
        params = {'filter': 'mentioned', 'state': 'open',
                  'sort': 'updated', 'direction': 'desc'}
        headers = {'Accept': 'application/vnd.github.v3.text+json',
                   'Authorization': 'token my-token'}
        self.expect('GET', '/issues', params, headers)

    def test_repos(self):
        self.service.repos().get()
        self.expect('GET', '/user/repos', {'type': 'all'})

        self.service.repos().get(type='owner')
        self.expect('GET', '/user/repos', {'type': 'owner'})

        self.service.repo('myuser', 'myrepo').get()
        self.expect('GET', '/repos/myuser/myrepo')

        self.service.repo('myuser', 'myrepo').update({'x': 'x'})
        self.expect('PATCH', '/repos/myuser/myrepo', json.dumps({'x': 'x'}))

        self.service.repos().create({'x': 'x'})
        self.expect('POST', '/user/repos', json.dumps({'x': 'x'}))

        self.service.repo('myuser', 'myrepo').contributors(anon=True)
        self.expect('GET', '/repos/myuser/myrepo/contributors',
                    {'anon': 'true'})

        self.service.repo('myuser', 'myrepo').languages()
        self.expect('GET', '/repos/myuser/myrepo/languages')

        self.service.repo('myuser', 'myrepo').teams()
        self.expect('GET', '/repos/myuser/myrepo/teams')

        self.service.repo('myuser', 'myrepo').tags()
        self.expect('GET', '/repos/myuser/myrepo/tags')

        self.service.repo('myuser', 'myrepo').branches()
        self.expect('GET', '/repos/myuser/myrepo/branches')

    def test_repo_issues(self):
        self.service.repo('myuser', 'myrepo').issues().get()
        self.expect('GET', '/repos/myuser/myrepo/issues')

        params = {'state': 'open', 'mentioned': 'foo',
                  'sort': 'created', 'direction': 'desc'}
        self.service.repo('myuser', 'myrepo').issues().get(mentioned='foo')
        self.expect('GET', '/repos/myuser/myrepo/issues', params)

        self.service.repo('myuser', 'myrepo').issues().get()
        self.expect('GET', '/repos/myuser/myrepo/issues')

        self.service.repo('myuser', 'myrepo').issue(4).get()
        self.expect('GET', '/repos/myuser/myrepo/issues/4')

        self.service.repo('myuser', 'myrepo').issues().create({'x': 'x'})
        self.expect('POST', '/repos/myuser/myrepo/issues',
                    json.dumps({'x': 'x'}))

        self.service.repo('myuser', 'myrepo').issue(4).update({'x': 'x'})
        self.expect('PATCH', '/repos/myuser/myrepo/issues/4',
                    json.dumps({'x': 'x'}))

    def test_issue_comments(self):
        self.service.repo('myuser', 'myrepo').issue(4).comments().get()
        self.expect('GET', '/repos/myuser/myrepo/issues/4/comments')

        self.service.repo('myuser', 'myrepo').issue(4).comment(5).get()
        self.expect('GET', '/repos/myuser/myrepo/issues/4/comments/5')

        (self.service.repo('myuser', 'myrepo')
         .issue(5).comments()
         .create('comment text'))
        self.expect('POST', '/repos/myuser/myrepo/issues/5/comments',
                    json.dumps({'body': 'comment text'}))

        (self.service.repo('myuser', 'myrepo')
         .issue(5).comment(6)
         .update('comment text'))
        self.expect('PATCH', '/repos/myuser/myrepo/issues/5/comments/6',
                    json.dumps({'body': 'comment text'}))

        (self.service.repo('myuser', 'myrepo')
         .issue(5).comment(6)
         .delete())
        self.expect('DELETE', '/repos/myuser/myrepo/issues/5/comments/6')

    def test_issue_events(self):
        self.service.repo('myuser', 'myrepo').issue(4).events().get()
        self.expect('GET', '/repos/myuser/myrepo/issues/4/events')

        self.service.repo('myuser', 'myrepo').issues().events().get()
        self.expect('GET', '/repos/myuser/myrepo/issues/events')

        self.service.repo('myuser', 'myrepo').issue(4).event(5).get()
        self.expect('GET', '/repos/myuser/myrepo/issues/4/events/5')

    def test_labels(self):
        self.service.repo('myuser', 'myrepo').labels().get()
        self.expect('GET', '/repos/myuser/myrepo/labels')

        self.service.repo('myuser', 'myrepo').label('l').get()
        self.expect('GET', '/repos/myuser/myrepo/labels/l')

        self.service.repo('myuser', 'myrepo').labels().create(
            {'name': 'l', 'color': 'ffffff'})
        self.expect('POST', '/repos/myuser/myrepo/labels',
                    json.dumps({'name': 'l', 'color': 'ffffff'}))

        self.service.repo('myuser', 'myrepo').label('l').update({'name': 'l2'})
        self.expect('PATCH', '/repos/myuser/myrepo/labels/l',
                    json.dumps({'name': 'l2'}))

        self.service.repo('myuser', 'myrepo').label('l').delete()
        self.expect('DELETE', '/repos/myuser/myrepo/labels/l')

        self.service.repo('myuser', 'myrepo').issue(4).labels().get()
        self.expect('GET', '/repos/myuser/myrepo/issues/4/labels')

        (self.service.repo('myuser', 'myrepo').issue(4)
         .labels().create(['l1', 'l2']))
        self.expect('POST', '/repos/myuser/myrepo/issues/4/labels',
                    json.dumps(['l1', 'l2']))

        self.service.repo('myuser', 'myrepo').issue(4).label('l').delete()
        self.expect('DELETE', '/repos/myuser/myrepo/issues/4/labels/l')

        (self.service.repo('myuser', 'myrepo').issue(4)
         .labels().replace(['l1', 'l2']))
        self.expect('PUT', '/repos/myuser/myrepo/issues/4/labels')

        self.service.repo('myuser', 'myrepo').issue(4).labels().delete()
        self.expect('DELETE', '/repos/myuser/myrepo/issues/4/labels')

    def test_milestones(self):
        params = {'state': 'open', 'sort': 'due_date',
                  'direction': 'asc', 'page': 2}
        self.service.repo('myuser', 'myrepo').milestones().get(
            direction='asc', page=2)
        self.expect('GET', '/repos/myuser/myrepo/milestones', params)

        self.service.repo('myuser', 'myrepo').milestone(2).get()
        self.expect('GET', '/repos/myuser/myrepo/milestones/2')

        self.service.repo('myuser', 'myrepo').milestones().create({'x': 'x'})
        self.expect('POST', '/repos/myuser/myrepo/milestones',
                    json.dumps({'x': 'x'}))

        self.service.repo('myuser', 'myrepo').milestone(3).update({'x': 'x'})
        self.expect('PATCH', '/repos/myuser/myrepo/milestones/3',
                    json.dumps({'x': 'x'}))

        self.service.repo('myuser', 'myrepo').milestone(3).delete()
        self.expect('DELETE', '/repos/myuser/myrepo/milestones/3')

        self.service.repo('myuser', 'myrepo').milestone(3).labels().get()
        self.expect('GET', '/repos/myuser/myrepo/milestones/3/labels')

    def test_collaborators(self):
        self.service.repo('myuser', 'myrepo').collaborators().get(page=2)
        self.expect('GET', '/repos/myuser/myrepo/collaborators', {'page': 2})

        self.service.repo('myuser', 'myrepo').collaborators().add('foo')
        self.expect('PUT', '/repos/myuser/myrepo/collaborators/foo')

        self.service.repo('myuser', 'myrepo').collaborators().remove('foo')
        self.expect('DELETE', '/repos/myuser/myrepo/collaborators/foo')

        self.executor.set_response(b'', 204, {})
        res = (self.service.repo('myuser', 'myrepo').collaborators()
         .is_collaborator('foo'))
        self.expect('GET', '/repos/myuser/myrepo/collaborators/foo')
        self.assertTrue(res)

    def test_repo_commits(self):
        self.service.repo('myuser', 'myrepo').commits().get(sha='x', page=2)
        self.expect('GET', '/repos/myuser/myrepo/commits',
                    {'sha': 'x', 'page': 2})

        self.service.repo('myuser', 'myrepo').commit('x').get()
        self.expect('GET', '/repos/myuser/myrepo/commits/x')

        self.service.repo('myuser', 'myrepo').commits().comments().get(page=2)
        self.expect('GET', '/repos/myuser/myrepo/comments', {'page': 2})

        self.service.repo('myuser', 'myrepo').commit('x').comments().get(
            format='html', page=2)
        self.expect('GET', '/repos/myuser/myrepo/commits/x/comments',
                    {'page': 2},
                    headers={'Accept': 'application/vnd.github.v3.html+json',
                             'Authorization': 'token my-token'})

        self.service.repo('myuser', 'myrepo').commit('x').comments().create(
            {'x': 'x'})
        self.expect('POST', '/repos/myuser/myrepo/commits/x/comments',
                    json.dumps({'x': 'x'}))

        self.service.repo('myuser', 'myrepo').commits().comment(3).get()
        self.expect('GET', '/repos/myuser/myrepo/comments/3')

        (self.service.repo('myuser', 'myrepo').commits()
         .comment(3).update('comment text'))
        self.expect('PATCH', '/repos/myuser/myrepo/comments/3',
                    json.dumps({'body': 'comment text'}))

        self.service.repo('myuser', 'myrepo').commits().compare('c1', 'c2')
        self.expect('GET', '/repos/myuser/myrepo/compare/c1...c2')

        self.service.repo('myuser', 'myrepo').commits().comment(2).delete()
        self.expect('DELETE', '/repos/myuser/myrepo/comments/2')

    def test_downloads(self):
        self.service.repo('myuser', 'myrepo').downloads().get(page=2)
        self.expect('GET', '/repos/myuser/myrepo/downloads', {'page': 2})

        self.service.repo('myuser', 'myrepo').download(1).get()
        self.expect('GET', '/repos/myuser/myrepo/downloads/1')

        self.service.repo('myuser', 'myrepo').downloads().create({'x': 'x'})
        self.expect('POST', '/repos/myuser/myrepo/downloads',
                    json.dumps({'x': 'x'}))

        self.service.repo('myuser', 'myrepo').download(1).delete()
        self.expect('DELETE', '/repos/myuser/myrepo/downloads/1')

        self.assertRaises(base.MethodNotSupported,
                          self.service.repo('myuser', 'myrepo')
                          .download(1).update, {'x': 'x'})

    def test_forks(self):
        self.service.repo('myuser', 'myrepo').forks().get(per_page=3)
        self.expect('GET', '/repos/myuser/myrepo/forks',
                    {'sort': 'newest', 'per_page': 3})

        self.service.repo('myuser', 'myrepo').forks().create()
        self.expect('POST', '/repos/myuser/myrepo/forks')

    def test_users(self):
        self.service.user().get()
        self.expect('GET', '/user')

        self.service.user().update({'x': 'x'})
        self.expect('PATCH', '/user', json.dumps({'x': 'x'}))

        self.assertRaises(base.MethodNotSupported,
                          self.service.user().delete)

        self.assertRaises(base.MethodNotSupported,
                          self.service.user().create, {'x': 'x'})

        self.service.user('name').get()
        self.expect('GET', '/users/name')

        self.service.user().emails().get()
        self.expect('GET', '/user/emails')

        self.service.user().emails().add('u@example.org')
        self.expect('POST', '/user/emails', json.dumps('u@example.org'))

        self.service.user().emails().remove(['u@example.org', 'x@example.org'])
        self.expect('DELETE', '/user/emails')

    def test_followers(self):
        self.service.user().followers()
        self.expect('GET', '/user/followers')

        self.service.user('foo').followers(page=3)
        self.expect('GET', '/users/foo/followers', {'page': 3})

        self.service.user().following()
        self.expect('GET', '/user/following')

        self.service.user('foo').following(page=3)
        self.expect('GET', '/users/foo/following', {'page': 3})

        self.service.user().follow('name')
        self.expect('PUT', '/user/following/name')

        self.service.user().unfollow('name')
        self.expect('DELETE', '/user/following/name')

        self.executor.set_response(b'', 204, {})
        res = self.service.user().follows('name')
        self.expect('GET', '/user/following/name')
        self.assertTrue(res)

        self.executor.set_response(b'', 404, {})
        res = self.service.user().follows('name')
        self.expect('GET', '/user/following/name')
        self.assertFalse(res)

    def test_user_repos(self):
        self.service.user('foo').repos().get(page=2)
        self.expect('GET', '/users/foo/repos', {'page': 2, 'type': 'all'})

        self.assertRaises(base.MethodNotSupported,
                          self.service.user('foo').repos().create)

        self.assertRaises(base.MethodNotSupported,
                          self.service.user('foo').repos().update, 'x')

    def test_authorizations(self):
        self.service.authorizations().get()
        self.expect('GET', '/authorizations')

        self.service.authorization(1).get()
        self.expect('GET', '/authorizations/1')

        self.service.authorizations().create({'x': 'x'})
        self.expect('POST', '/authorizations', json.dumps({'x': 'x'}))

        self.service.authorization(1).update({'x': 'x'})
        self.expect('PATCH', '/authorizations/1', json.dumps({'x': 'x'}))

        self.service.authorization(1).delete()
        self.expect('DELETE', '/authorizations/1')

    def test_unicode(self):
        # try an unicode name
        self.service.repo('myuser', b'\xce\xbb'.decode('utf-8')).get()
        self.expect('GET', '/repos/myuser/%CE%BB')

        # try an binary name (that's not valid Unicode)
        self.service.repo('myuser', b'\xa4\xff').get()
        self.expect('GET', '/repos/myuser/%A4%FF')

        # try a unicode parameter
        self.service.gists().comment('123').update(b'\xce\xbb'.decode('utf-8'))
        self.expect('PATCH', '/gists/comments/123', r'{"body": "\u03bb"}')
