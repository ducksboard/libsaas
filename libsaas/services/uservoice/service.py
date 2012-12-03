import json

from libsaas import http, parsers, port

from libsaas.filters import auth
from libsaas.services import base

from . import articles, forums, gadgets, streams, notes, custom_fields
from . import comments, faqs, subdomains, suggestions, tickets, topics, users


class UserVoice(base.Resource):
    """
    """
    def __init__(self, subdomain, api_key, api_secret=None,
                 access_token=None, access_token_secret=None):
        """
        Create a UserVoice service.

        :var subdomain: The account-specific part of the UserVoice domain, for
            instance use `mycompany` if your UserVoice domain is
            `mycompany.uservoice.com`.
        :vartype subdomain: str

        :var api_key: The API key.
        :vartype api_key: str

        :var api_secret: Optional API secret. If you leave this as None, all
            requests will be made as unauthenticated requests.
        :vartype api_secret: str or None

        :var access_token: Optional OAuth 1.0a access token. If you leave this
            as None, all requests be made as unauthenticated requests.
        :vartype access_token: str or None

        :var access_token_secret: Optional OAuth 1.0a access token secret. If
            you leave this as None, all requests be made as unauthenticated
            requests.
        :vartype access_token_secret: str or None
        """
        self.api_key = api_key
        self.oauth = None

        if api_secret and access_token and access_token_secret:
            self.oauth = auth.OAuth(access_token, access_token_secret,
                                    api_key, api_secret)

        tmpl = '{0}.uservoice.com/api/v1'
        self.apiroot = http.quote_any(tmpl.format(port.to_u(subdomain)))
        self.apiroot = 'http://' + self.apiroot

        self.add_filter(self.use_json)
        self.add_filter(self.serialize_flatten)
        self.add_filter(self.urlencode_put)
        # authenticate has to be the last filter, because anything that
        # modifies the request after it's signed will make the signature
        # invalid!
        self.add_filter(self.authenticate)

    def get_url(self):
        return self.apiroot

    def authenticate(self, request):
        if not self.oauth:
            # not using OAuth, make an unauthenticated request
            request.params['client'] = self.api_key
        else:
            # using OAuth, sign the request
            self.oauth(request)

    def use_json(self, request):
        request.headers['Accept'] = 'application/json'
        request.uri += '.json'

    def serialize_flatten(self, request):
        # use serialize_flatten to flatten params in POST and PUT
        if request.method.upper() not in http.URLENCODE_METHODS:
            serialized = {}
            for name, value in request.params.items():
                serialized.update(http.serialize_flatten(name, value))
            request.params = serialized

    def urlencode_put(self, request):
        # UserVoice adheres to the OAuth 1.0 specification as published on
        # http://oauth.net/core/1.0/ *NOT* to the final version published as
        # RFC5849.
        #
        # This means that they don't include PUT request body in the base
        # signature string. The requests-oauth library that we're using
        # implements the RFC5849 version of OAuth and so for PUT requests it
        # generates signatures that UserVoice rejects.
        #
        # To work around this, for PUT requests we serialize the parameters to
        # a string before handing it off to the executor, which causes
        # requests-oauth to skip the body when calculating the signature.
        if request.method.upper() == 'PUT':
            request.params = http.urlencode_any(request.params)

    @base.apimethod
    def search(self, page=None, per_page=None, query=None):
        """
        Generic search for all objects.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var query: Search string.
        :vartype query: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'search')

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def instant_answers_search(self, page=None, per_page=None, query=None):
        """
        Search for instant answers.

        :var page: Where should paging start. If left as `None`, the first page
            is returned.
        :vartype page: int

        :var per_page: How many objects sould be returned. If left as `None`,
            10 objects are returned.
        :vartype per_page: int

        :var query: Search string.
        :vartype query: str
        """
        params = base.get_params(None, locals())
        url = '{0}/instant_answers/{1}'.format(self.get_url(), 'search')

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def oembed(self, url):
        """
        Fetch the HTML used to embed a suggestion.

        :var url: URL to the Suggestion you want to embed (ex:
            forums/1/suggestions/1)
        :vartype url: str
        """
        _url = '{0}/oembed'.format(self.get_url())
        return http.Request('GET', _url, {'url': url}), parsers.parse_json

    @base.resource(articles.Article)
    def article(self, article_id):
        """
        Return the resource corresponding to a single article.
        """
        return articles.Article(self, article_id)

    @base.resource(articles.Articles)
    def articles(self):
        """
        Return the resource corresponding to all the articles.
        """
        return articles.Articles(self)

    @base.resource(forums.Forum)
    def forum(self, forum_id):
        """
        Return the resource corresponding to a single forum.
        """
        return forums.Forum(self, forum_id)

    @base.resource(forums.Forums)
    def forums(self):
        """
        Return the resource corresponding to all the forums.
        """
        return forums.Forums(self)

    @base.resource(notes.Notes)
    def notes(self):
        """
        Return the resource corresponding to all the notes.
        """
        return notes.Notes(self)

    @base.resource(gadgets.Gadget)
    def gadget(self, gadget_id):
        """
        Return the resource corresponding to a single gadget.
        """
        return gadgets.Gadget(self, gadget_id)

    @base.resource(gadgets.Gadgets)
    def gadgets(self):
        """
        Return the resource corresponding to all the gadgets.
        """
        return gadgets.Gadgets(self)

    @base.resource(streams.Stream)
    def stream(self):
        """
        Return the resource corresponding to a stream.
        """
        return streams.Stream(self)

    @base.resource(tickets.Ticket)
    def ticket(self, ticket_id):
        """
        Return the resource corresponding to a single ticket.
        """
        return tickets.Ticket(self, ticket_id)

    @base.resource(tickets.Tickets)
    def tickets(self):
        """
        Return the resource corresponding to all the tickets.
        """
        return tickets.Tickets(self)

    @base.resource(subdomains.Subdomain)
    def subdomain(self, subdomain):
        """
        Return the resource corresponding to a UserVoice subdomain.
        """
        return subdomains.Subdomain(self, subdomain)

    @base.resource(suggestions.Suggestion)
    def suggestion(self, suggestion_id):
        """
        Return the resource corresponding to a single suggestion.
        """
        return suggestions.Suggestion(self, suggestion_id)

    @base.resource(suggestions.Suggestions)
    def suggestions(self):
        """
        Return the resource corresponding to all the suggestions.
        """
        return suggestions.Suggestions(self)

    @base.resource(topics.Topic)
    def topic(self, topic_id):
        """
        Return the resource corresponding a single topic.
        """
        return topics.Topic(self, topic_id)

    @base.resource(topics.Topics)
    def topics(self):
        """
        Return the resource corresponding all the topics.
        """
        return topics.Topics(self)

    @base.resource(users.User)
    def user(self, user_id=None):
        """
        Return the resource corresponding to a single user. If user_id is
        `None`, the returned resource is the currently authenticated user,
        otherwise it is the user with the given ID number.
        """
        if user_id is None:
            return users.CurrentUser(self)

        return users.User(self, user_id)

    @base.resource(users.Users)
    def users(self):
        """
        Return the resource corresponding to all the users.
        """
        return users.Users(self)

    @base.resource(comments.Comments)
    def comments(self):
        """
        Return the resource corresponding to all the comments.
        """
        return comments.Comments(self)

    @base.resource(faqs.Faq)
    def faq(self, faq_id):
        """
        Return the resource corresponding to a single FAQ.
        """
        return faqs.Faq(self, faq_id)

    @base.resource(custom_fields.CustomFields)
    def custom_fields(self):
        """
        Return the resource corresponding to custom fields.
        """
        return custom_fields.CustomFields(self)
