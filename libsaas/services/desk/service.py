from libsaas import http, port

from libsaas.services import base
from libsaas.filters import auth

from . import cases, customers, interactions, users, contents, macros


class Desk(base.Resource):
    """
    """
    def __init__(self, subdomain, api_key, api_secret=None,
                 access_token=None, access_token_secret=None):
        """
        Create a Desk service.

        :var subdomain: The account-specific part of the Desk domain, for
            instance use `mycompany` if your Zendesk domain is
            `mycompany.desk.com`.
        :vartype subdomain: str

        :var api_key: The API key.
        :vartype api_key: str

        :var api_secret: API secret.
        :vartype api_secret: str

        :var access_token: OAuth 1.0a access token.
        :vartype access_token: str

        :var access_token_secret: OAuth 1.0a access token secret.
            requests.
        :vartype access_token_secret: str
        """
        tmpl = '{0}.desk.com/api/v1'
        self.apiroot = http.quote_any(tmpl.format(port.to_u(subdomain)))
        self.apiroot = 'https://' + self.apiroot

        self.oauth = auth.OAuth(access_token, access_token_secret,
                                api_key, api_secret)

        self.add_filter(self.use_json)
        # authenticate has to be the last filter, because anything that
        # modifies the request after it's signed will make the signature
        # invalid!
        self.add_filter(self.authenticate)

    def get_url(self):
        return self.apiroot

    def authenticate(self, request):
        self.oauth(request)

    def use_json(self, request):
        request.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        request.headers['Accept'] = '*/*'

        request.uri += '.json'

    @base.resource(cases.Case)
    def case(self, case_id, is_external=False):
        """
        Return the resource corresponding to a single case.

        :var case_id: The case id
        :vartype case_id: str

        :var is_external: Use the external id
        :vartype case_id: bool

        """
        return cases.Case(self, case_id, is_external)

    @base.resource(cases.Cases)
    def cases(self):
        """
        Return the resource corresponding to all the cases.
        """
        return cases.Cases(self)

    @base.resource(customers.Customer)
    def customer(self, customer_id=None):
        """
        Return the resource corresponding to a single customer.
        """
        return customers.Customer(self, customer_id)

    @base.resource(customers.Customers)
    def customers(self):
        """
        Return the resource corresponding to all customers.
        """
        return customers.Customers(self)

    @base.resource(interactions.Interactions)
    def interactions(self):
        """
        Return the resource corresponding to all interactions.
        """
        return interactions.Interactions(self)

    @base.resource(users.Group)
    def group(self, group_id):
        """
        Return the resource corresponding to a single group.
        """
        return users.Group(self, group_id)

    @base.resource(users.Groups)
    def groups(self):
        """
        Return the resource corresponding to all groups.
        """
        return users.Groups(self)

    @base.resource(users.Account)
    def account(self):
        """
        Return the resource corresponding to a single user.
        """
        return users.Account(self)

    @base.resource(users.User)
    def user(self, user_id):
        """
        Return the resource corresponding to a single user.
        """
        return users.User(self, user_id)

    @base.resource(users.Users)
    def users(self):
        """
        Return the resource corresponding to all users.
        """
        return users.Users(self)

    @base.resource(contents.Topic)
    def topic(self, topic_id):
        """
        Return the resource corresponding to a single topic.
        """
        return contents.Topic(self, topic_id)

    @base.resource(contents.Topics)
    def topics(self):
        """
        Return the resource corresponding to all topics.
        """
        return contents.Topics(self)

    @base.resource(contents.Article)
    def article(self, article_id):
        """
        Return the resource corresponding to a single article.
        """
        return contents.Article(self, article_id)

    @base.resource(macros.Macro)
    def macro(self, macro_id):
        """
        Return the resource corresponding to a single macro.
        """
        return macros.Macro(self, macro_id)

    @base.resource(macros.Macros)
    def macros(self):
        """
        Return the resource corresponding to all macros.
        """
        return macros.Macros(self)
