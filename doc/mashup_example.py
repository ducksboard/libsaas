from datetime import datetime, timedelta

from libsaas.services import mailchimp, zendesk

# create Zendesk and Mailchimp services
zd = zendesk.Zendesk('mycompany', 'username', 'password')
mc = mailchimp.Mailchimp('8ac789caf98879caf897a678fa76daf-us2')

# get tickets solved yesterday
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
tickets = zd.search('updated>{0} status:solved type:ticket'.format(yesterday))

# get emails of users who requested those tickets
user_ids = [ticket['requester_id'] for ticket in tickets['results']]
emails = [zd.user(user_id).get()['user']['email'] for user_id in user_ids]

# grab the ID of the "Users" list
lists = mc.lists(filters={'list_name': 'Users'})
list_id = lists['data'][0]['id']

# set the SOLVED variable for those users in Mailchimp to yesterday
batch = [{'EMAIL': email, 'SOLVED': yesterday} for email in emails]
mc.listBatchSubscribe(list_id, batch, double_optin=False, update_existing=True)
