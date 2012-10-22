import unittest

from libsaas.executors import test_executor
from libsaas.services import base, twilio


class TwilioTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = twilio.Twilio('my-sid', 'my-token')
        self.account = self.service.account('foo')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method is not None:
            self.assertEqual(method, self.executor.request.method)
        if uri is not None:
            self.assertEqual(self.executor.request.uri,
                             'https://api.twilio.com/2010-04-01/' + uri)
        if params is not None:
            self.assertEqual(self.executor.request.params, params)
        if headers is not None:
            self.assertEqual(self.executor.request.headers, headers)

    def test_translate_inequality(self):
        self.assertEqual('NothingToDo',
                         twilio.resource.translate_inequality('NothingToDo'))

        self.assertEqual('Greater>',
                         twilio.resource.translate_inequality('GreaterGT'))

        self.assertEqual('Lower<',
                         twilio.resource.translate_inequality('LowerLT'))

    def test_auth(self):
        service = twilio.Twilio('a-sid', 'a-token')
        service.accounts().get()
        self.expect('GET', 'Accounts.json', {},
                    {'Authorization': 'Basic YS1zaWQ6YS10b2tlbg=='})

    def test_accounts(self):
        # Account resource
        self.assertRaises(TypeError, self.service.account)

        self.account.get()
        self.expect('GET', 'Accounts/foo.json')

        update_account_data = {'FriendlyName': 'updated-account'}
        self.account.update(update_account_data)
        self.expect('POST', 'Accounts/foo.json', update_account_data)

        self.assertRaises(base.MethodNotSupported, self.account.create)
        self.assertRaises(base.MethodNotSupported, self.account.delete)

        # Accounts resource
        accounts = self.service.accounts()

        accounts.get()
        self.expect('GET', 'Accounts.json')

        accounts.get(FriendlyName='an-account')
        self.expect('GET', 'Accounts.json', {'FriendlyName': 'an-account'})

        new_account_data = {'FriendlyName': 'foo'}
        accounts.create(new_account_data)
        self.expect('POST', 'Accounts.json', new_account_data)

        self.assertRaises(base.MethodNotSupported, accounts.update)
        self.assertRaises(base.MethodNotSupported, accounts.delete)

    def test_numbers(self):
        # AvailablePhoneNumbers resource
        available_phone_numbers = self.account.available_phone_numbers()

        self.assertRaises(base.MethodNotSupported,
                          available_phone_numbers.get)
        self.assertRaises(base.MethodNotSupported,
                          available_phone_numbers.create)
        self.assertRaises(base.MethodNotSupported,
                          available_phone_numbers.update)
        self.assertRaises(base.MethodNotSupported,
                          available_phone_numbers.delete)

        # Local AvailablePhoneNumbers resource
        local_us = available_phone_numbers.local('US')

        self.assertRaises(TypeError, available_phone_numbers.local)

        local_us.get()
        self.expect('GET', 'Accounts/foo/AvailablePhoneNumbers/US/Local.json')

        local_us.get(Contains='510555****')
        self.expect('GET', 'Accounts/foo/AvailablePhoneNumbers/US/Local.json',
                    {'Contains': '510555****'})

        self.assertRaises(base.MethodNotSupported, local_us.create)
        self.assertRaises(base.MethodNotSupported, local_us.update)
        self.assertRaises(base.MethodNotSupported, local_us.delete)

        # Toll-Free AvailablePhoneNumbers resource
        toll_free_us = available_phone_numbers.toll_free('US')

        self.assertRaises(TypeError, available_phone_numbers.toll_free)

        toll_free_us.get()
        self.expect('GET', 'Accounts/foo/AvailablePhoneNumbers/US/TollFree.json')

        toll_free_us.get(Contains='510555****')
        self.expect('GET', 'Accounts/foo/AvailablePhoneNumbers/US/TollFree.json',
                    {'Contains': '510555****'})

        self.assertRaises(base.MethodNotSupported, toll_free_us.create)
        self.assertRaises(base.MethodNotSupported, toll_free_us.update)
        self.assertRaises(base.MethodNotSupported, toll_free_us.delete)

        # OutgoingCallerId resource
        caller_id = self.account.outgoing_caller_id('a-caller')

        caller_id.get()
        self.expect('GET', 'Accounts/foo/OutgoingCallerIds/a-caller.json')

        update_outgoing_data = {'FriendlyName': 'foo'}
        caller_id.update(update_outgoing_data)
        self.expect('POST', 'Accounts/foo/OutgoingCallerIds/a-caller.json',
                    update_outgoing_data)

        caller_id.delete()
        self.expect('DELETE', 'Accounts/foo/OutgoingCallerIds/a-caller.json')

        self.assertRaises(base.MethodNotSupported, caller_id.create)

        # OutgoingCallerIds resource
        caller_ids = self.account.outgoing_caller_ids()

        caller_ids.get()
        self.expect('GET', 'Accounts/foo/OutgoingCallerIds.json')

        caller_ids.get(FriendlyName='a-caller')
        self.expect('GET', 'Accounts/foo/OutgoingCallerIds.json',
                    {'FriendlyName': 'a-caller'})

        new_outgoing_data = {'PhoneNumber': 555, 'Extension': 123}
        caller_ids.create(new_outgoing_data)
        self.expect('POST', 'Accounts/foo/OutgoingCallerIds.json',
                    new_outgoing_data)

        self.assertRaises(base.MethodNotSupported, caller_ids.update)
        self.assertRaises(base.MethodNotSupported, caller_ids.delete)

        # IncomingPhoneNumber resource
        number = self.account.incoming_phone_number('55510')

        number.get()
        self.expect('GET', 'Accounts/foo/IncomingPhoneNumbers/55510.json')

        update_number_data = {'FriendlyName': 'foo'}
        number.update(update_number_data)
        self.expect('POST', 'Accounts/foo/IncomingPhoneNumbers/55510.json',
                    update_number_data)

        number.delete()
        self.expect('DELETE', 'Accounts/foo/IncomingPhoneNumbers/55510.json')

        self.assertRaises(base.MethodNotSupported, number.create)

        # IncomingPhoneNumbers resource
        numbers = self.account.incoming_phone_numbers()

        numbers.get()
        self.expect('GET', 'Accounts/foo/IncomingPhoneNumbers.json')

        numbers.get(FriendlyName='a-number')
        self.expect('GET', 'Accounts/foo/IncomingPhoneNumbers.json',
                    {'FriendlyName': 'a-number'})

        new_number_data = {'PhoneNumber': 555, 'AreaCode': 123}
        numbers.create(new_number_data)
        self.expect('POST', 'Accounts/foo/IncomingPhoneNumbers.json',
                    new_number_data)

        self.assertRaises(base.MethodNotSupported, numbers.update)
        self.assertRaises(base.MethodNotSupported, numbers.delete)

        # Local IncomingPhoneNumbers resource
        local_numbers = self.account.incoming_phone_numbers().local()

        local_numbers.get()
        self.expect('GET', 'Accounts/foo/IncomingPhoneNumbers/Local.json')

        local_numbers.get(FriendlyName='a-number')
        self.expect('GET', 'Accounts/foo/IncomingPhoneNumbers/Local.json',
                    {'FriendlyName': 'a-number'})

        new_number_data = {'PhoneNumber': 555}
        local_numbers.create(new_number_data)
        self.expect('POST', 'Accounts/foo/IncomingPhoneNumbers/Local.json',
                    new_number_data)

        self.assertRaises(base.MethodNotSupported, local_numbers.update)
        self.assertRaises(base.MethodNotSupported, local_numbers.delete)

        # Toll-Free IncomingPhoneNumbers resource
        toll_free_numbers = self.account.incoming_phone_numbers().toll_free()

        toll_free_numbers.get()
        self.expect('GET', 'Accounts/foo/IncomingPhoneNumbers/TollFree.json')

        toll_free_numbers.get(FriendlyName='number')
        self.expect('GET', 'Accounts/foo/IncomingPhoneNumbers/TollFree.json',
                    {'FriendlyName': 'number'})

        new_number_data = {'PhoneNumber': 555}
        toll_free_numbers.create(new_number_data)
        self.expect('POST', 'Accounts/foo/IncomingPhoneNumbers/TollFree.json',
                    new_number_data)

        self.assertRaises(base.MethodNotSupported, toll_free_numbers.update)
        self.assertRaises(base.MethodNotSupported, toll_free_numbers.delete)

    def test_applications(self):
        # ConnectApp resource
        connect_app = self.account.connect_app('app')

        self.assertRaises(TypeError, self.account.connect_app)

        connect_app.get()
        self.expect('GET', 'Accounts/foo/ConnectApps/app.json')

        update_app_data = {'FriendlyName': 'foo'}
        connect_app.update(update_app_data)
        self.expect('POST', 'Accounts/foo/ConnectApps/app.json',
                    update_app_data)

        self.assertRaises(base.MethodNotSupported, connect_app.create)
        self.assertRaises(base.MethodNotSupported, connect_app.delete)

        # ConnectApps resource
        connect_apps = self.account.connect_apps()

        connect_apps.get()
        self.expect('GET', 'Accounts/foo/ConnectApps.json')

        self.assertRaises(base.MethodNotSupported, connect_apps.create)
        self.assertRaises(base.MethodNotSupported, connect_apps.update)
        self.assertRaises(base.MethodNotSupported, connect_apps.delete)

        # AuthorizedConnectApp resource
        authorized_connect_app = self.account.authorized_connect_app('app')

        self.assertRaises(TypeError, self.account.authorized_connect_app)

        authorized_connect_app.get()
        self.expect('GET', 'Accounts/foo/AuthorizedConnectApps/app.json')

        self.assertRaises(base.MethodNotSupported,
                          authorized_connect_app.create)
        self.assertRaises(base.MethodNotSupported,
                          authorized_connect_app.update)
        self.assertRaises(base.MethodNotSupported,
                          authorized_connect_app.delete)

        # AuthorizedConnectApps resource
        authorized_connect_apps = self.account.authorized_connect_apps()

        authorized_connect_apps.get()
        self.expect('GET', 'Accounts/foo/AuthorizedConnectApps.json')

        self.assertRaises(base.MethodNotSupported,
                          authorized_connect_apps.create)
        self.assertRaises(base.MethodNotSupported,
                          authorized_connect_apps.update)
        self.assertRaises(base.MethodNotSupported,
                          authorized_connect_apps.delete)

        # Application resource
        application = self.account.application('app')

        self.assertRaises(TypeError, self.account.application)

        application.get()
        self.expect('GET', 'Accounts/foo/Applications/app.json')

        update_app_data = {'FriendlyName': 'foo', 'VoiceUrl': 'http://bar/'}
        application.update(update_app_data)
        self.expect('POST', 'Accounts/foo/Applications/app.json',
                    update_app_data)

        application.delete()
        self.expect('DELETE', 'Accounts/foo/Applications/app.json')

        self.assertRaises(base.MethodNotSupported, application.create)

        # Applications resource
        applications = self.account.applications()

        applications.get()
        self.expect('GET', 'Accounts/foo/Applications.json')

        applications.get(FriendlyName='foo')
        self.expect('GET', 'Accounts/foo/Applications.json',
                    {'FriendlyName': 'foo'})

        new_app_data = {'FriendlyName': 'foo'}
        applications.create(new_app_data)
        self.expect('POST', 'Accounts/foo/Applications.json', new_app_data)

        self.assertRaises(base.MethodNotSupported, applications.update)
        self.assertRaises(base.MethodNotSupported, applications.delete)

    def test_calls(self):
        # Call resource
        call = self.account.call('a-call')

        self.assertRaises(TypeError, self.account.call)

        call.get()
        self.expect('GET', 'Accounts/foo/Calls/a-call.json')

        update_call_data = {'Url': 'http://bar/', 'Status': 'completed'}
        call.update(update_call_data)
        self.expect('POST', 'Accounts/foo/Calls/a-call.json', update_call_data)

        self.assertRaises(base.MethodNotSupported, call.create)
        self.assertRaises(base.MethodNotSupported, call.delete)

        # Call Notifications resource
        call_notifications = call.notifications()

        call_notifications.get()
        self.expect('GET', 'Accounts/foo/Calls/a-call/Notifications.json')

        call_notifications.get(MessageDateGT='2012-06-06')
        self.expect('GET', 'Accounts/foo/Calls/a-call/Notifications.json',
                    {'MessageDate>': '2012-06-06'})

        self.assertRaises(base.MethodNotSupported, call_notifications.create)
        self.assertRaises(base.MethodNotSupported, call_notifications.update)
        self.assertRaises(base.MethodNotSupported, call_notifications.delete)

        # Call Recordings resource
        call_recordings = call.recordings()

        call_recordings.get()
        self.expect('GET', 'Accounts/foo/Calls/a-call/Recordings.json')

        call_recordings.get(DateCreatedLT='2012-06-06')
        self.expect('GET', 'Accounts/foo/Calls/a-call/Recordings.json',
                    {'DateCreated<': '2012-06-06'})

        self.assertRaises(base.MethodNotSupported, call_recordings.create)
        self.assertRaises(base.MethodNotSupported, call_recordings.update)
        self.assertRaises(base.MethodNotSupported, call_recordings.delete)

        # Calls resource
        calls = self.account.calls()

        calls.get()
        self.expect('GET', 'Accounts/foo/Calls.json')

        calls.get(StartTimeGT='2012-06-06')
        self.expect('GET', 'Accounts/foo/Calls.json',
                    {'StartTime>': '2012-06-06'})

        new_call_data = {'Url': 'http://bar/'}
        calls.create(new_call_data)
        self.expect('POST', 'Accounts/foo/Calls.json', new_call_data)

        self.assertRaises(base.MethodNotSupported, calls.update)
        self.assertRaises(base.MethodNotSupported, calls.delete)

    def test_conferences(self):
        # Conference resource
        conference = self.account.conference('conf')

        self.assertRaises(TypeError, self.account.conference)

        conference.get()
        self.expect('GET', 'Accounts/foo/Conferences/conf.json')

        self.assertRaises(base.MethodNotSupported, conference.create)
        self.assertRaises(base.MethodNotSupported, conference.update)
        self.assertRaises(base.MethodNotSupported, conference.delete)

        # Conference participant resource
        participant = conference.participant('guy')

        participant.get()
        self.expect('GET',
                    'Accounts/foo/Conferences/conf/Participants/guy.json')

        update_participant_data = {'Muted': True}
        participant.update(update_participant_data)
        self.expect('POST',
                    'Accounts/foo/Conferences/conf/Participants/guy.json',
                    update_participant_data)

        participant.delete()
        self.expect('DELETE',
                    'Accounts/foo/Conferences/conf/Participants/guy.json')

        self.assertRaises(base.MethodNotSupported, participant.create)

        # Conference participants resource
        participants = conference.participants()

        participants.get()
        self.expect('GET', 'Accounts/foo/Conferences/conf/Participants.json')

        participants.get(Muted=True)
        self.expect('GET', 'Accounts/foo/Conferences/conf/Participants.json',
                    {'Muted': 'true'})

        self.assertRaises(base.MethodNotSupported, participants.create)
        self.assertRaises(base.MethodNotSupported, participants.update)
        self.assertRaises(base.MethodNotSupported, participants.delete)

        # Conference resource
        conferences = self.account.conferences()

        conferences.get()
        self.expect('GET', 'Accounts/foo/Conferences.json')

        conferences.get(DateUpdatedGT='2012-06-06')
        self.expect('GET', 'Accounts/foo/Conferences.json',
                    {'DateUpdated>': '2012-06-06'})

        self.assertRaises(base.MethodNotSupported, conferences.create)
        self.assertRaises(base.MethodNotSupported, conferences.update)
        self.assertRaises(base.MethodNotSupported, conferences.delete)

    def test_queues(self):
        # Queue resource
        queue = self.account.queue('queue')

        self.assertRaises(TypeError, self.account.queue)

        queue.get()
        self.expect('GET', 'Accounts/foo/Queues/queue.json')

        update_queue_data = {'CurrentSize': 16}
        queue.update(update_queue_data)
        self.expect('POST', 'Accounts/foo/Queues/queue.json',
                    update_queue_data)

        queue.delete()
        self.expect('DELETE', 'Accounts/foo/Queues/queue.json')

        self.assertRaises(base.MethodNotSupported, queue.create)

        # Queue Member resource
        member = queue.member('member')

        member.get()
        self.expect('GET', 'Accounts/foo/Queues/queue/Members/member.json')

        update_member_data = {'Url': 'http://bar/'}
        member.update(update_member_data)
        self.expect('POST', 'Accounts/foo/Queues/queue/Members/member.json',
                    update_member_data)

        self.assertRaises(base.MethodNotSupported, member.create)
        self.assertRaises(base.MethodNotSupported, member.delete)

        # Queue Members resource
        members = queue.members()

        members.get()
        self.expect('GET', 'Accounts/foo/Queues/queue/Members.json')

        self.assertRaises(base.MethodNotSupported, members.create)
        self.assertRaises(base.MethodNotSupported, members.update)
        self.assertRaises(base.MethodNotSupported, members.delete)

        # Queues resource
        queues = self.account.queues()

        queues.get()
        self.expect('GET', 'Accounts/foo/Queues.json')

        new_queue_data = {'FriendlyName': 'foo', 'MaxSize': 12}
        queues.create(new_queue_data)
        self.expect('POST', 'Accounts/foo/Queues.json', new_queue_data)

        self.assertRaises(base.MethodNotSupported, queues.update)
        self.assertRaises(base.MethodNotSupported, queues.delete)

    def test_sms(self):
        # SMS resource
        sms = self.account.sms()

        self.assertRaises(base.MethodNotSupported, sms.get)
        self.assertRaises(base.MethodNotSupported, sms.create)
        self.assertRaises(base.MethodNotSupported, sms.update)
        self.assertRaises(base.MethodNotSupported, sms.delete)

        # SMS Message resource
        message = sms.message('message')

        self.assertRaises(TypeError, sms.message)

        message.get()
        self.expect('GET', 'Accounts/foo/SMS/Messages/message.json')

        self.assertRaises(base.MethodNotSupported, message.create)
        self.assertRaises(base.MethodNotSupported, message.update)
        self.assertRaises(base.MethodNotSupported, message.delete)

        # SMS Messages resource
        messages = sms.messages()

        messages.get()
        self.expect('GET', 'Accounts/foo/SMS/Messages.json')

        messages.get(DateSentLT='2012-06-06')
        self.expect('GET', 'Accounts/foo/SMS/Messages.json',
                    {'DateSent<': '2012-06-06'})

        new_message_data = {'To': '55510', 'Body': 'foo bar baz'}
        messages.create(new_message_data)
        self.expect('POST', 'Accounts/foo/SMS/Messages.json',
                    new_message_data)

        self.assertRaises(base.MethodNotSupported, messages.update)
        self.assertRaises(base.MethodNotSupported, messages.delete)

        # ShortCode resource
        short_code = sms.short_code('55510')

        self.assertRaises(TypeError, sms.short_code)

        short_code.get()
        self.expect('GET', 'Accounts/foo/SMS/ShortCodes/55510.json')

        update_code_data = {'FriendlyName': 'foo'}
        short_code.update(update_code_data)
        self.expect('POST', 'Accounts/foo/SMS/ShortCodes/55510.json',
                    update_code_data)

        self.assertRaises(base.MethodNotSupported, short_code.create)
        self.assertRaises(base.MethodNotSupported, short_code.delete)

        # ShortCodes resource
        short_codes = sms.short_codes()

        short_codes.get()
        self.expect('GET', 'Accounts/foo/SMS/ShortCodes.json')

        short_codes.get(ShortCode='55510')
        self.expect('GET', 'Accounts/foo/SMS/ShortCodes.json',
                    {'ShortCode': '55510'})

        self.assertRaises(base.MethodNotSupported, short_codes.create)
        self.assertRaises(base.MethodNotSupported, short_codes.update)
        self.assertRaises(base.MethodNotSupported, short_codes.delete)

    def test_recordings(self):
        # Recording resource
        recording = self.account.recording('rec')

        self.assertRaises(TypeError, self.account.recording)

        recording.get()
        self.expect('GET', 'Accounts/foo/Recordings/rec.json')

        recording.delete()
        self.expect('DELETE', 'Accounts/foo/Recordings/rec.json')

        self.assertRaises(base.MethodNotSupported, recording.create)
        self.assertRaises(base.MethodNotSupported, recording.update)

        # Recording Transcriptions resource
        record_trans = recording.transcriptions()

        record_trans.get()
        self.expect('GET', 'Accounts/foo/Recordings/rec/Transcriptions.json')

        self.assertRaises(base.MethodNotSupported, record_trans.create)
        self.assertRaises(base.MethodNotSupported, record_trans.update)
        self.assertRaises(base.MethodNotSupported, record_trans.delete)

        # Recordings resource
        recordings = self.account.recordings()

        recordings.get()
        self.expect('GET', 'Accounts/foo/Recordings.json')

        recordings.get(DateCreatedGT='2012-06-06')
        self.expect('GET', 'Accounts/foo/Recordings.json',
                    {'DateCreated>': '2012-06-06'})

        self.assertRaises(base.MethodNotSupported, recordings.create)
        self.assertRaises(base.MethodNotSupported, recordings.update)
        self.assertRaises(base.MethodNotSupported, recordings.delete)

        # Transcription resource
        transcription = self.account.transcription('trans')

        self.assertRaises(TypeError, self.account.transcription)

        transcription.get()
        self.expect('GET', 'Accounts/foo/Transcriptions/trans.json')

        self.assertRaises(base.MethodNotSupported, transcription.create)
        self.assertRaises(base.MethodNotSupported, transcription.update)
        self.assertRaises(base.MethodNotSupported, transcription.delete)

        # Transcriptions resource
        transcriptions = self.account.transcriptions()

        transcriptions.get()
        self.expect('GET', 'Accounts/foo/Transcriptions.json')

        self.assertRaises(base.MethodNotSupported, transcriptions.create)
        self.assertRaises(base.MethodNotSupported, transcriptions.update)
        self.assertRaises(base.MethodNotSupported, transcriptions.delete)

    def test_notifications(self):
        # Notification resource
        notification = self.account.notification('noti')

        self.assertRaises(TypeError, self.account.notification)

        notification.get()
        self.expect('GET', 'Accounts/foo/Notifications/noti.json')

        notification.delete()
        self.expect('DELETE', 'Accounts/foo/Notifications/noti.json')

        self.assertRaises(base.MethodNotSupported, notification.create)
        self.assertRaises(base.MethodNotSupported, notification.update)

        # Notifications resource
        notifications = self.account.notifications()

        notifications.get()
        self.expect('GET', 'Accounts/foo/Notifications.json')

        notifications.get(MessageDateGT='2012-06-06')
        self.expect('GET', 'Accounts/foo/Notifications.json',
                    {'MessageDate>': '2012-06-06'})

        self.assertRaises(base.MethodNotSupported, notifications.create)
        self.assertRaises(base.MethodNotSupported, notifications.update)
        self.assertRaises(base.MethodNotSupported, notifications.delete)

    def test_usage(self):
        # Usage resource
        usage = self.account.usage()

        self.assertRaises(base.MethodNotSupported, usage.get)
        self.assertRaises(base.MethodNotSupported, usage.create)
        self.assertRaises(base.MethodNotSupported, usage.update)
        self.assertRaises(base.MethodNotSupported, usage.delete)

        # Records resource
        records = usage.records()

        records.get()
        self.expect('GET', 'Accounts/foo/Usage/Records.json')

        records.get(Category='calls', StartDate='-30days', Page=3)
        self.expect('GET', 'Accounts/foo/Usage/Records.json',
                    {'Category': 'calls', 'StartDate': '-30days',
                     'Page': 3})

        self.assertRaises(base.MethodNotSupported, records.create)
        self.assertRaises(base.MethodNotSupported, records.update)
        self.assertRaises(base.MethodNotSupported, records.delete)

        # Records sub-resources
        subresources = [
            ('daily', 'Daily'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('all_time', 'AllTime'),
            ('today', 'Today'),
            ('yesterday', 'Yesterday'),
            ('this_month', 'ThisMonth'),
            ('last_month', 'LastMonth')
        ]

        for subresource in subresources:
            resource = getattr(records, subresource[0])()
            url = 'Accounts/foo/Usage/Records/{0}.json'.format(subresource[1])

            resource.get()
            self.expect('GET', url)

            resource.get(Category='calls', StartDate='-30days', Page=3)
            self.expect('GET', url, {'Category': 'calls',
                                     'StartDate': '-30days',
                                     'Page': 3})

            self.assertRaises(base.MethodNotSupported, resource.create)
            self.assertRaises(base.MethodNotSupported, resource.update)
            self.assertRaises(base.MethodNotSupported, resource.delete)

        # Trigger resource
        trigger = usage.trigger('trigger')

        self.assertRaises(TypeError, self.account.usage().trigger)

        trigger.get()
        self.expect('GET', 'Accounts/foo/Usage/Triggers/trigger.json')

        update_trigger_data = {'CallbackUrl': 'http://foo/bar/'}
        trigger.update(update_trigger_data)
        self.expect('POST', 'Accounts/foo/Usage/Triggers/trigger.json',
                    update_trigger_data)

        trigger.delete()
        self.expect('DELETE', 'Accounts/foo/Usage/Triggers/trigger.json')

        self.assertRaises(base.MethodNotSupported, trigger.create)

        # Triggers resource
        triggers = usage.triggers()

        triggers.get()
        self.expect('GET', 'Accounts/foo/Usage/Triggers.json')

        triggers.get(UsageCategory='calls', Page=3)
        self.expect('GET', 'Accounts/foo/Usage/Triggers.json',
                    {'UsageCategory': 'calls', 'Page': 3})

        new_trigger_data = {'UsageCategory': 'calls', 'TriggerValue': '+30'}
        triggers.create(new_trigger_data)
        self.expect('POST', 'Accounts/foo/Usage/Triggers.json',
                    new_trigger_data)

        self.assertRaises(base.MethodNotSupported, triggers.update)
        self.assertRaises(base.MethodNotSupported, triggers.delete)
