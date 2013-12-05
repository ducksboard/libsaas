import json
import unittest

from libsaas.executors import test_executor
from libsaas.services import trello


class TrelloTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = trello.Trello('my-key','my-token')

    def expect(self, method=None, uri=None, params={}):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if method != 'GET':
            uri += '?token=my-token&key=my-key'

        self.assertEqual(
            self.executor.request.uri,
            'https://api.trello.com/1' + uri)

        if method == 'GET':
            params.update({'token': 'my-token', 'key': 'my-key'})

        if params:
            self.assertEqual(self.executor.request.params, params)

    def test_actions(self):
        self.service.action('1234').get()
        self.expect('GET', '/actions/1234', {})
        self.service.action('1234').get(fields=['id'])
        self.expect('GET', '/actions/1234', {'fields': 'id'})
        self.service.action('1234').get(fields=['id', 'name'])
        self.expect('GET', '/actions/1234', {'fields': 'id,name'})
        self.service.action('1234').get(member=True)
        self.expect('GET', '/actions/1234', {'member': 'true'})
        self.service.action('1234').field('name')
        self.expect('GET', '/actions/1234/name', {})

        self.service.action('1234').board().get()
        self.expect('GET', '/actions/1234/board', {})
        self.service.action('1234').board().get(fields=['id', 'name'])
        self.expect('GET', '/actions/1234/board', {'fields': 'id,name'})
        self.service.action('1234').board().field('name')
        self.expect('GET', '/actions/1234/board/name', {})

        self.service.action('1234').card().get()
        self.expect('GET', '/actions/1234/card', {})
        self.service.action('1234').card().get(fields=['id', 'name'])
        self.expect('GET', '/actions/1234/card', {'fields': 'id,name'})
        self.service.action('1234').card().field('name')
        self.expect('GET', '/actions/1234/card/name', {})

        self.service.action('1234').list().get()
        self.expect('GET', '/actions/1234/list', {})
        self.service.action('1234').list().get(fields=['id', 'name'])
        self.expect('GET', '/actions/1234/list', {'fields': 'id,name'})
        self.service.action('1234').list().field('name')
        self.expect('GET', '/actions/1234/list/name', {})

        self.service.action('1234').member().get()
        self.expect('GET', '/actions/1234/member', {})
        self.service.action('1234').member().get(fields=['id', 'name'])
        self.expect('GET', '/actions/1234/member', {'fields': 'id,name'})
        self.service.action('1234').member().field('name')
        self.expect('GET', '/actions/1234/member/name', {})

        self.service.action('1234').creator().get()
        self.expect('GET', '/actions/1234/memberCreator', {})
        self.service.action('1234').creator().get(fields=['id', 'name'])
        self.expect('GET', '/actions/1234/memberCreator', {'fields': 'id,name'})
        self.service.action('1234').creator().field('name')
        self.expect('GET', '/actions/1234/memberCreator/name', {})

        self.service.action('1234').organization().get()
        self.expect('GET', '/actions/1234/organization', {})
        self.service.action('1234').organization().get(fields=['id', 'name'])
        self.expect('GET', '/actions/1234/organization', {'fields': 'id,name'})
        self.service.action('1234').organization().field('name')
        self.expect('GET', '/actions/1234/organization/name', {})

        obj = {'foo': 'bar'}
        self.service.action('1234').update(obj)
        self.expect('PUT', '/actions/1234', json.dumps(obj))

        self.service.action('1234').delete()
        self.expect('DELETE', '/actions/1234')

    def test_boards(self):
        self.service.board('1234').get()
        self.expect('GET', '/boards/1234', {})
        self.service.board('1234').get(fields=['id'])
        self.expect('GET', '/boards/1234', {'fields': 'id'})
        self.service.board('1234').get(fields=['id', 'name'])
        self.expect('GET', '/boards/1234', {'fields': 'id,name'})
        self.service.board('1234').get(action_member=True)
        self.expect('GET', '/boards/1234', {'action_member': 'true'})
        self.service.board('1234').field('name')
        self.expect('GET', '/boards/1234/name', {})

        self.service.board('1234').actions().get()
        self.expect('GET', '/boards/1234/actions', {})
        self.service.board('1234').actions().get(limit=10)
        self.expect('GET', '/boards/1234/actions', {'limit': 10})

        self.service.board('1234').cards().get()
        self.expect('GET', '/boards/1234/cards', {})
        self.service.board('1234').cards().get(limit=10)
        self.expect('GET', '/boards/1234/cards', {'limit': 10})
        self.service.board('1234').cards().filter('open')
        self.expect('GET', '/boards/1234/cards/open', {})

        self.service.board('1234').card('1234').get()
        self.expect('GET', '/boards/1234/cards/1234', {})
        self.service.board('1234').card('1234').get(fields=['id'])
        self.expect('GET', '/boards/1234/cards/1234', {'fields': 'id'})

        self.service.board('1234').checklists().get()
        self.expect('GET', '/boards/1234/checklists', {})
        self.service.board('1234').checklists().get(limit=10)
        self.expect('GET', '/boards/1234/checklists', {'limit': 10})

        self.service.board('1234').lists().get()
        self.expect('GET', '/boards/1234/lists', {})
        self.service.board('1234').lists().get(limit=10)
        self.expect('GET', '/boards/1234/lists', {'limit': 10})
        self.service.board('1234').lists().filter('open')
        self.expect('GET', '/boards/1234/lists/open', {})

        self.service.board('1234').members().get()
        self.expect('GET', '/boards/1234/members', {})
        self.service.board('1234').members().get(limit=10)
        self.expect('GET', '/boards/1234/members', {'limit': 10})
        self.service.board('1234').members().filter('normal')
        self.expect('GET', '/boards/1234/members/normal', {})

        self.service.board('1234').members_invited().get()
        self.expect('GET', '/boards/1234/membersInvited', {})
        self.service.board('1234').members_invited().get(fields=['id'])
        self.expect('GET', '/boards/1234/membersInvited', {'fields': 'id'})

        self.service.board('1234').memberships().get()
        self.expect('GET', '/boards/1234/memberships', {})
        self.service.board('1234').memberships().get(limit=10)
        self.expect('GET', '/boards/1234/memberships', {'limit': 10})

        self.service.board('1234').membership('1234').get()
        self.expect('GET', '/boards/1234/memberships/1234', {})
        self.service.board('1234').membership('1234').get(fields=['id'])
        self.expect('GET', '/boards/1234/memberships/1234', {'fields': 'id'})

        self.service.board('1234').organization().get()
        self.expect('GET', '/boards/1234/organization', {})
        self.service.board('1234').organization().get(fields=['id'])
        self.expect('GET', '/boards/1234/organization', {'fields': 'id'})
        self.service.board('1234').organization().field('id')
        self.expect('GET', '/boards/1234/organization/id', {})

        obj = {'foo': 'bar'}

        self.service.boards().create(obj)
        self.expect('POST', '/boards', json.dumps(obj))

        self.service.board('1234').calendar_key()
        self.expect('POST', '/boards/1234/calendarKey/generate')

        self.service.board('1234').mark_as_viewed()
        self.expect('POST', '/boards/1234/markAsViewed')

        self.service.board('1234').email_key()
        self.expect('POST', '/boards/1234/emailKey/generate')

        self.service.board('1234').checklists().create(obj)
        self.expect('POST', '/boards/1234/checklists', json.dumps(obj))

        self.service.board('1234').lists().create(obj)
        self.expect('POST', '/boards/1234/lists', json.dumps(obj))

        self.service.board('1234').update(obj)
        self.expect('PUT', '/boards/1234', json.dumps(obj))

        self.service.board('1234').member('1234').update(obj)
        self.expect('PUT', '/boards/1234/members/1234', json.dumps(obj))

        self.service.board('1234').membership('1234').update(obj)
        self.expect('PUT', '/boards/1234/memberships/1234', json.dumps(obj))

        self.service.board('1234').member('1234').delete()
        self.expect('DELETE', '/boards/1234/members/1234')

    def test_cards(self):
        self.service.card('1234').get()
        self.expect('GET', '/cards/1234', {})
        self.service.card('1234').get(fields=['id'])
        self.expect('GET', '/cards/1234', {'fields': 'id'})
        self.service.card('1234').get(fields=['id', 'name'])
        self.expect('GET', '/cards/1234', {'fields': 'id,name'})
        self.service.card('1234').get(attachments=True)
        self.expect('GET', '/cards/1234', {'attachments': 'true'})
        self.service.card('1234').field('name')
        self.expect('GET', '/cards/1234/name', {})

        self.service.card('1234').actions().get()
        self.expect('GET', '/cards/1234/actions', {})
        self.service.card('1234').actions().get(limit=10)
        self.expect('GET', '/cards/1234/actions', {'limit': 10})

        self.service.card('1234').attachments().get()
        self.expect('GET', '/cards/1234/attachments', {})
        self.service.card('1234').attachments().get(limit=10)
        self.expect('GET', '/cards/1234/attachments', {'limit': 10})

        self.service.card('1234').attachment('1234').get()
        self.expect('GET', '/cards/1234/attachments/1234', {})
        self.service.card('1234').attachment('1234').get(fields=['id'])
        self.expect('GET', '/cards/1234/attachments/1234', {'fields': 'id'})

        self.service.card('1234').board().get()
        self.expect('GET', '/cards/1234/board', {})
        self.service.card('1234').board().get(fields=['id', 'name'])
        self.expect('GET', '/cards/1234/board', {'fields': 'id,name'})
        self.service.card('1234').board().field('name')
        self.expect('GET', '/cards/1234/board/name', {})

        self.service.card('1234').checkitem_states().get()
        self.expect('GET', '/cards/1234/checkItemStates', {})
        self.service.card('1234').checkitem_states().get(limit=10)
        self.expect('GET', '/cards/1234/checkItemStates', {'limit': 10})

        self.service.card('1234').checklists().get()
        self.expect('GET', '/cards/1234/checklists', {})
        self.service.card('1234').checklists().get(limit=10)
        self.expect('GET', '/cards/1234/checklists', {'limit': 10})

        self.service.card('1234').list().get()
        self.expect('GET', '/cards/1234/list', {})
        self.service.card('1234').list().get(fields=['id', 'name'])
        self.expect('GET', '/cards/1234/list', {'fields': 'id,name'})
        self.service.card('1234').list().field('name')
        self.expect('GET', '/cards/1234/list/name', {})

        self.service.card('1234').members().get()
        self.expect('GET', '/cards/1234/members', {})
        self.service.card('1234').members().get(limit=10)
        self.expect('GET', '/cards/1234/members', {'limit': 10})

        self.service.card('1234').members_voted().get()
        self.expect('GET', '/cards/1234/membersVoted', {})
        self.service.card('1234').members_voted().get(fields=['id'])
        self.expect('GET', '/cards/1234/membersVoted', {'fields': 'id'})

        self.service.card('1234').stickers().get()
        self.expect('GET', '/cards/1234/stickers', {})
        self.service.card('1234').stickers().get(limit=10)
        self.expect('GET', '/cards/1234/stickers', {'limit': 10})

        self.service.card('1234').sticker('1234').get()
        self.expect('GET', '/cards/1234/stickers/1234', {})
        self.service.card('1234').sticker('1234').get(fields=['id'])
        self.expect('GET', '/cards/1234/stickers/1234', {'fields': 'id'})

        obj = {'foo': 'bar'}

        self.service.cards().create(obj)
        self.expect('POST', '/cards', json.dumps(obj))

        self.service.card('1234').actions().comments().create(obj)
        self.expect('POST', '/cards/1234/actions/comments', json.dumps(obj))

        self.service.card('1234').attachments().create(obj)
        self.expect('POST', '/cards/1234/attachments', json.dumps(obj))

        self.service.card('1234').checklists().create(obj)
        self.expect('POST', '/cards/1234/checklists', json.dumps(obj))

        self.service.card('1').checklist('2').checkitems().create(obj)
        self.expect('POST', '/cards/1/checklist/2/checkItem', json.dumps(obj))

        self.service.card('1').checklist('2').checkitem('3').convert_to_card()
        self.expect(
            'POST', '/cards/1/checklist/2/checkItem/3/convertToCard',
            json.dumps({}))

        self.service.card('1234').labels().create(obj)
        self.expect('POST', '/cards/1234/labels', json.dumps(obj))

        self.service.card('1234').members_voted().create(obj)
        self.expect('POST', '/cards/1234/membersVoted', json.dumps(obj))

        self.service.card('1234').update(obj)
        self.expect('PUT', '/cards/1234', json.dumps(obj))

        self.service.card('1234').actions().comments().update(obj)
        self.expect('PUT', '/cards/1234/actions/comments', json.dumps(obj))

        self.service.card('1').checklist('2').checkitem('3').update(obj)
        self.expect('PUT', '/cards/1/checklist/2/checkItem/3', json.dumps(obj))

        self.service.card('1').sticker('2').update(obj)
        self.expect('PUT', '/cards/1/stickers/2', json.dumps(obj))

        self.service.card('1').attachment('2').delete()
        self.expect('DELETE', '/cards/1/attachments/2')

        self.service.card('1234').actions().comments().delete()
        self.expect('DELETE', '/cards/1234/actions/comments')

        self.service.card('1').checklist('2').checkitem('3').delete()
        self.expect('DELETE', '/cards/1/checklist/2/checkItem/3')

        self.service.card('1').sticker('2').delete()
        self.expect('DELETE', '/cards/1/stickers/2')

        self.service.card('1').label('2').delete()
        self.expect('DELETE', '/cards/1/labels/2')

    def test_checklists(self):
        self.service.checklist('1234').get()
        self.expect('GET', '/checklists/1234', {})
        self.service.checklist('1234').get(fields=['id'])
        self.expect('GET', '/checklists/1234', {'fields': 'id'})
        self.service.checklist('1234').get(fields=['id', 'name'])
        self.expect('GET', '/checklists/1234', {'fields': 'id,name'})
        self.service.checklist('1234').get(member=True)
        self.expect('GET', '/checklists/1234', {'member': 'true'})
        self.service.checklist('1234').field('name')
        self.expect('GET', '/checklists/1234/name', {})

        self.service.checklist('1234').board().get()
        self.expect('GET', '/checklists/1234/board', {})
        self.service.checklist('1234').board().get(fields=['id', 'name'])
        self.expect('GET', '/checklists/1234/board', {'fields': 'id,name'})
        self.service.checklist('1234').board().field('name')
        self.expect('GET', '/checklists/1234/board/name', {})

        self.service.checklist('1234').cards().get()
        self.expect('GET', '/checklists/1234/cards', {})
        self.service.checklist('1234').cards().get(limit=10)
        self.expect('GET', '/checklists/1234/cards', {'limit': 10})
        self.service.checklist('1234').cards().filter('closed')
        self.expect('GET', '/checklists/1234/cards/closed', {})

        self.service.checklist('1234').checkitems().get()
        self.expect('GET', '/checklists/1234/checkItems', {})
        self.service.checklist('1234').checkitems().get(limit=10)
        self.expect('GET', '/checklists/1234/checkItems', {'limit': 10})

        self.service.checklist('1234').checkitem('1234').get()
        self.expect('GET', '/checklists/1234/checkItems/1234', {})
        self.service.checklist('1234').checkitem('1234').get(fields=['id'])
        self.expect('GET', '/checklists/1234/checkItems/1234', {'fields': 'id'})

        obj = {'foo': 'bar'}

        self.service.checklists().create(obj)
        self.expect('POST', '/checklists', json.dumps(obj))

        self.service.checklist('1234').checkitems().create(obj)
        self.expect('POST', '/checklists/1234/checkItems', json.dumps(obj))

        self.service.checklist('1234').update(obj)
        self.expect('PUT', '/checklists/1234', json.dumps(obj))

        self.service.checklist('1234').delete()
        self.expect('DELETE', '/checklists/1234')

    def test_lists(self):
        self.service.list('1234').get()
        self.expect('GET', '/lists/1234', {})
        self.service.list('1234').get(fields=['id'])
        self.expect('GET', '/lists/1234', {'fields': 'id'})
        self.service.list('1234').get(fields=['id', 'name'])
        self.expect('GET', '/lists/1234', {'fields': 'id,name'})
        self.service.list('1234').get(member=True)
        self.expect('GET', '/lists/1234', {'member': 'true'})
        self.service.list('1234').field('name')
        self.expect('GET', '/lists/1234/name', {})

        self.service.list('1234').actions().get()
        self.expect('GET', '/lists/1234/actions', {})
        self.service.list('1234').actions().get(limit=10)
        self.expect('GET', '/lists/1234/actions', {'limit': 10})

        self.service.list('1234').board().get()
        self.expect('GET', '/lists/1234/board', {})
        self.service.list('1234').board().get(fields=['id', 'name'])
        self.expect('GET', '/lists/1234/board', {'fields': 'id,name'})
        self.service.list('1234').board().field('name')
        self.expect('GET', '/lists/1234/board/name', {})

        self.service.list('1234').cards().get()
        self.expect('GET', '/lists/1234/cards', {})
        self.service.list('1234').cards().get(limit=10)
        self.expect('GET', '/lists/1234/cards', {'limit': 10})
        self.service.list('1234').cards().filter('closed')
        self.expect('GET', '/lists/1234/cards/closed', {})

        obj = {'foo': 'bar'}

        self.service.lists().create(obj)
        self.expect('POST', '/lists', json.dumps(obj))

        self.service.list('1234').archive_all_cards()
        self.expect('POST', '/lists/1234/archiveAllCards')

        self.service.list('1234').update(obj)
        self.expect('PUT', '/lists/1234', json.dumps(obj))


    def test_members(self):
        self.service.member('1234').get()
        self.expect('GET', '/members/1234', {})
        self.service.member('1234').get(fields=['id'])
        self.expect('GET', '/members/1234', {'fields': 'id'})
        self.service.member('1234').get(fields=['id', 'name'])
        self.expect('GET', '/members/1234', {'fields': 'id,name'})
        self.service.member('1234').get(member=True)
        self.expect('GET', '/members/1234', {'member': 'true'})
        self.service.member('1234').field('name')
        self.expect('GET', '/members/1234/name', {})

        self.service.member('1234').actions().get()
        self.expect('GET', '/members/1234/actions', {})
        self.service.member('1234').actions().get(limit=10)
        self.expect('GET', '/members/1234/actions', {'limit': 10})

        self.service.member('1234').board_backgrounds().get()
        self.expect('GET', '/members/1234/boardBackgrounds', {})
        self.service.member('1234').board_backgrounds().get(limit=10)
        self.expect('GET', '/members/1234/boardBackgrounds', {'limit': 10})

        self.service.member('1234').board_background('1234').get()
        self.expect('GET', '/members/1234/boardBackgrounds/1234', {})
        self.service.member('1').board_background('2').get(fields=['id'])
        self.expect('GET', '/members/1/boardBackgrounds/2', {'fields': 'id'})

        self.service.member('1234').board_stars().get()
        self.expect('GET', '/members/1234/boardStars', {})

        self.service.member('1234').boards().get()
        self.expect('GET', '/members/1234/boards', {})
        self.service.member('1234').boards().get(fields=['id', 'name'])
        self.expect('GET', '/members/1234/boards', {'fields': 'id,name'})
        self.service.member('1234').boards().filter('closed')
        self.expect('GET', '/members/1234/boards/closed', {})

        self.service.member('1234').cards().get()
        self.expect('GET', '/members/1234/cards', {})
        self.service.member('1234').cards().get(limit=10)
        self.expect('GET', '/members/1234/cards', {'limit': 10})
        self.service.member('1234').cards().filter('closed')
        self.expect('GET', '/members/1234/cards/closed', {})

        self.service.member('1234').custom_board_backgrounds().get()
        self.expect('GET', '/members/1234/customBoardBackgrounds', {})
        self.service.member('1').custom_board_backgrounds().get(limit=10)
        self.expect('GET', '/members/1/customBoardBackgrounds', {'limit': 10})

        self.service.member('1234').custom_board_background('1234').get()
        self.expect('GET', '/members/1234/customBoardBackgrounds/1234', {})
        self.service.member('1').custom_board_background('2').get(
            fields=['id'])
        self.expect('GET', '/members/1/customBoardBackgrounds/2',
            {'fields': 'id'})

        self.service.member('1234').custom_stickers().get()
        self.expect('GET', '/members/1234/customStickers', {})
        self.service.member('1234').custom_stickers().get(limit=10)
        self.expect('GET', '/members/1234/customStickers', {'limit': 10})

        self.service.member('1234').custom_sticker('1234').get()
        self.expect('GET', '/members/1234/customStickers/1234', {})
        self.service.member('1').custom_sticker('2').get(fields=['id'])
        self.expect('GET', '/members/1/customStickers/2', {'fields': 'id'})

        self.service.member('1234').notifications().get()
        self.expect('GET', '/members/1234/notifications', {})
        self.service.member('1234').notifications().get(limit=10)
        self.expect('GET', '/members/1234/notifications', {'limit': 10})
        self.service.member('1234').notifications().filter('closed')
        self.expect('GET', '/members/1234/notifications/closed', {})

        self.service.member('1234').organizations().get()
        self.expect('GET', '/members/1234/organizations', {})
        self.service.member('1234').organizations().get(limit=10)
        self.expect('GET', '/members/1234/organizations', {'limit': 10})
        self.service.member('1234').organizations().filter('closed')
        self.expect('GET', '/members/1234/organizations/closed', {})

        self.service.member('1234').tokens().get()
        self.expect('GET', '/members/1234/tokens', {})
        self.service.member('1234').tokens().get(limit=10)
        self.expect('GET', '/members/1234/tokens', {'limit': 10})

        self.service.member('1234').sessions().get()
        self.expect('GET', '/members/1234/sessions', {})
        self.service.member('1234').sessions().get(limit=10)
        self.expect('GET', '/members/1234/sessions', {'limit': 10})

        obj = {'foo': 'bar'}

        self.service.member('1').board_backgrounds().create(obj)
        self.expect('POST', '/members/1/boardBackgrounds', json.dumps(obj))

        self.service.member('1').custom_board_backgrounds().create(obj)
        self.expect('POST', '/members/1/customBoardBackgrounds',
            json.dumps(obj))

        self.service.member('1').board_stars().create(obj)
        self.expect('POST', '/members/1/boardStars', json.dumps(obj))

        self.service.member('1').custom_stickers().create(obj)
        self.expect('POST', '/members/1/customStickers', json.dumps(obj))

        self.service.member('1234').update(obj)
        self.expect('PUT', '/members/1234', json.dumps(obj))

        self.service.member('1').board_background('2').update(obj)
        self.expect('PUT', '/members/1/boardBackgrounds/2', json.dumps(obj))

        self.service.member('1').custom_board_background('2').update(obj)
        self.expect('PUT', '/members/1/customBoardBackgrounds/2',
            json.dumps(obj))

        self.service.member('1').board_star('2').update(obj)
        self.expect('PUT', '/members/1/boardStars/2', json.dumps(obj))

        self.service.member('1').board_background('2').delete()
        self.expect('DELETE', '/members/1/boardBackgrounds/2')

        self.service.member('1').custom_board_background('2').delete()
        self.expect('DELETE', '/members/1/customBoardBackgrounds/2')

        self.service.member('1').board_star('2').delete()
        self.expect('DELETE', '/members/1/boardStars/2')

    def test_notifications(self):
        self.service.notification('1234').get()
        self.expect('GET', '/notifications/1234', {})
        self.service.notification('1234').get(fields=['id'])
        self.expect('GET', '/notifications/1234', {'fields': 'id'})
        self.service.notification('1234').get(fields=['id', 'name'])
        self.expect('GET', '/notifications/1234', {'fields': 'id,name'})
        self.service.notification('1234').get(member=True)
        self.expect('GET', '/notifications/1234', {'member': 'true'})
        self.service.notification('1234').field('name')
        self.expect('GET', '/notifications/1234/name', {})

        self.service.notification('1234').board().get()
        self.expect('GET', '/notifications/1234/board', {})
        self.service.notification('1234').board().get(fields=['id', 'name'])
        self.expect('GET', '/notifications/1234/board', {'fields': 'id,name'})
        self.service.notification('1234').board().field('name')
        self.expect('GET', '/notifications/1234/board/name', {})

        self.service.notification('1234').card().get()
        self.expect('GET', '/notifications/1234/card', {})
        self.service.notification('1234').card().get(fields=['id', 'name'])
        self.expect('GET', '/notifications/1234/card', {'fields': 'id,name'})
        self.service.notification('1234').card().field('name')
        self.expect('GET', '/notifications/1234/card/name', {})

        self.service.notification('1234').list().get()
        self.expect('GET', '/notifications/1234/list', {})
        self.service.notification('1234').list().get(fields=['id', 'name'])
        self.expect('GET', '/notifications/1234/list', {'fields': 'id,name'})
        self.service.notification('1234').list().field('name')
        self.expect('GET', '/notifications/1234/list/name', {})

        self.service.notification('1234').member().get()
        self.expect('GET', '/notifications/1234/member', {})
        self.service.notification('1234').member().get(fields=['id', 'name'])
        self.expect('GET', '/notifications/1234/member', {'fields': 'id,name'})
        self.service.notification('1234').member().field('name')
        self.expect('GET', '/notifications/1234/member/name', {})

        self.service.notification('1234').creator().get()
        self.expect('GET', '/notifications/1234/memberCreator', {})
        self.service.notification('1').creator().get(fields=['id'])
        self.expect('GET', '/notifications/1/memberCreator', {'fields': 'id'})
        self.service.notification('1234').creator().field('name')
        self.expect('GET', '/notifications/1234/memberCreator/name', {})

        self.service.notification('1234').organization().get()
        self.expect('GET', '/notifications/1234/organization', {})
        self.service.notification('1').organization().get(fields=['id'])
        self.expect('GET', '/notifications/1/organization', {'fields': 'id'})
        self.service.notification('1234').organization().field('name')
        self.expect('GET', '/notifications/1234/organization/name', {})

        obj = {'foo': 'bar'}
        self.service.notification('1234').update(obj)
        self.expect('PUT', '/notifications/1234', json.dumps(obj))

    def test_organizations(self):
        self.service.organization('1234').get()
        self.expect('GET', '/organizations/1234', {})
        self.service.organization('1234').get(fields=['id'])
        self.expect('GET', '/organizations/1234', {'fields': 'id'})
        self.service.organization('1234').get(fields=['id', 'name'])
        self.expect('GET', '/organizations/1234', {'fields': 'id,name'})
        self.service.organization('1234').get(member=True)
        self.expect('GET', '/organizations/1234', {'member': 'true'})
        self.service.organization('1234').field('name')
        self.expect('GET', '/organizations/1234/name', {})

        self.service.organization('1234').actions().get()
        self.expect('GET', '/organizations/1234/actions', {})
        self.service.organization('1234').actions().get(limit=10)
        self.expect('GET', '/organizations/1234/actions', {'limit': 10})

        self.service.organization('1234').boards().get()
        self.expect('GET', '/organizations/1234/boards', {})
        self.service.organization('1234').boards().get(limit=10)
        self.expect('GET', '/organizations/1234/boards', {'limit': 10})
        self.service.organization('1234').boards().filter('closed')
        self.expect('GET', '/organizations/1234/boards/closed', {})

        self.service.organization('1234').members().get()
        self.expect('GET', '/organizations/1234/members', {})
        self.service.organization('1234').members().get(limit=10)
        self.expect('GET', '/organizations/1234/members', {'limit': 10})
        self.service.organization('1234').members().filter('normal')
        self.expect('GET', '/organizations/1234/members/normal', {})

        self.service.organization('1234').members_invited().get()
        self.expect('GET', '/organizations/1234/membersInvited', {})
        self.service.organization('1').members_invited().get(fields=['id'])
        self.expect('GET', '/organizations/1/membersInvited', {'fields': 'id'})

        self.service.organization('1234').memberships().get()
        self.expect('GET', '/organizations/1234/memberships', {})
        self.service.organization('1234').memberships().get(limit=10)
        self.expect('GET', '/organizations/1234/memberships', {'limit': 10})

        self.service.organization('1234').membership('1234').get()
        self.expect('GET', '/organizations/1234/memberships/1234', {})

        obj = {'foo': 'bar'}

        self.service.organizations().create(obj)
        self.expect('POST', '/organizations', json.dumps(obj))

        self.service.organization('1234').update(obj)
        self.expect('PUT', '/organizations/1234', json.dumps(obj))

        self.service.organization('1234').member('1234').update(obj)
        self.expect('PUT', '/organizations/1234/members/1234', json.dumps(obj))

        self.service.organization('1').membership('2').update(obj)
        self.expect('PUT', '/organizations/1/memberships/2', json.dumps(obj))

        self.service.organization('1234').delete()
        self.expect('DELETE', '/organizations/1234')

        self.service.organization('1234').member('1234').delete()
        self.expect('DELETE', '/organizations/1234/members/1234')

        self.service.organization('1234').membership('1234').delete()
        self.expect('DELETE', '/organizations/1234/memberships/1234')
