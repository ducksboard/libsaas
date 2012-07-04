import json

from libsaas import http, parsers, port

from libsaas.filters import auth
from libsaas.services import base

from . import resources


class Zendesk(base.Resource):
    """
    """
    def __init__(self, subdomain, username, password):
        """
        Create a Zendesk service.

        :var subdomain: The account-specific part of the Zendesk domain, for
            instance use `mycompany` if your Zendesk domain is
            `mycompany.zendesk.com`.
        :vartype subdomain: str

        :var username: The email of the authenticated agent.
        :vartype username: str

        :var password: The password of the authenticated agent.
        :vartype password: str
        """
        tmpl = '{0}.zendesk.com/api/v2'
        self.apiroot = http.quote_any(tmpl.format(port.to_u(subdomain)))
        self.apiroot = 'https://' + self.apiroot

        self.add_filter(auth.BasicAuth(username, password))
        self.add_filter(self.use_json)

    def get_url(self):
        return self.apiroot

    def use_json(self, request):
        request.headers['Content-Type'] = 'application/json'
        request.headers['Accept'] = 'application/json'

        request.uri += '.json'

        if request.method.upper() not in http.URLENCODE_METHODS:
            request.params = json.dumps(request.params)

    @base.resource(resources.Tickets)
    def tickets(self):
        """
        Return the resource corresponding to all the tickets.
        """
        return resources.Tickets(self)

    @base.resource(resources.Ticket)
    def ticket(self, ticket_id):
        """
        Return the resource corresponding to a single ticket.
        """
        return resources.Ticket(self, ticket_id)

    @base.resource(resources.Users)
    def users(self):
        """
        Return the resource corresponding to all users.
        """
        return resources.Users(self)

    @base.resource(resources.User, resources.CurrentUser)
    def user(self, user_id=None):
        """
        Return the resource corresponding to a single user. If `user_id` is
        `None` the returned resource is the currently authenticated user,
        otherwise it is the user with the given ID number.
        """
        if user_id is None:
            return resources.CurrentUser(self)
        return resources.User(self, user_id)

    @base.resource(resources.Groups)
    def groups(self):
        """
        Return the resource corresponding to all groups.
        """
        return resources.Groups(self)

    @base.resource(resources.Group)
    def group(self, group_id):
        """
        Return the resource corresponding to a single group.
        """
        return resources.Group(self, group_id)

    @base.resource(resources.Activities)
    def activities(self):
        """
        Return the resource corresponding to all activities.
        """
        return resources.Activities(self)

    @base.resource(resources.Activity)
    def activity(self, activity_id):
        """
        Return the resource corresponding to a single activity.
        """
        return resources.Activity(self, activity_id)

    @base.resource(resources.SatisfactionRatings)
    def satisfaction_ratings(self):
        """
        Return the resource corresponding to all satisfaction ratings.
        """
        return resources.SatisfactionRatings(self)

    @base.resource(resources.SatisfactionRating)
    def satisfaction_rating(self, rating_id):
        """
        Return the resource corresponding to a single satisfaction rating.
        """
        return resources.SatisfactionRating(self, rating_id)

    @base.apimethod
    def search(self, query, sort_order=None,
               sort_by=None, page=None, per_page=None):
        """
        Fetch the results of a search on your Zendesk account. For details on
        searching, see
        http://developer.zendesk.com/documentation/rest_api/search.html

        :var query: A free-form search term.
        :vartype query: str

        :var sort_order: Optional order in which to sort the results.
        :vartype query: str

        :var sort_by: Optional term by which to sort the results.
        :vartype sort_by: str
        """
        url = '{0}/{1}'.format(self.get_url(), 'search')
        params = base.get_params(('query', 'sort_order', 'sort_by',
                                  'page', 'per_page'), locals())

        return http.Request('GET', url, params), parsers.parse_json

    @base.resource(resources.Views)
    def views(self):
        """
        Return the resource corresponding to all views.
        """
        return resources.Views(self)

    @base.resource(resources.View)
    def view(self, view_id):
        """
        Return the resource corresponding to a single view.
        """
        return resources.View(self, view_id)

    @base.resource(resources.Exports)
    def exports(self):
        """
        Return the resource corresponding to exports.
        """
        return resources.Exports(self)
