from libsaas import http, parsers
from libsaas.services import base


class Person(base.Resource):
    path = 'person'

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.lookup = {}
        for k, v in kwargs.items():
            if v is not None:
                self.lookup[k] = v
                break

    def get_url(self):
        return '{0}/{1}'.format(self.parent.get_url(), self.path)

    @base.apimethod
    def get(self, queue=None, style=None, prettyPrint=None, countryCode=None):
        """
        Fetch a single object.

        :var queue: Using this parameter notifies FullContact that the
                    query in question will be called later.
        :vartype queue: int

        :var style: The style parameter can be used to control the document
                    structure returned. Only available for email lookups.
        :vartype style: str

        :var prettyPrint: Used to disable prettyprint formatting response
        :vartype prettyPrint: str

        :var countryCode: For phone lookups, it must be passed when using
                          non US/Canada based numbers. Use the ISO-3166
                          two-digit country code. It defaults to US.
        :vartype countryCode: str
        """
        params = base.get_params(None, locals())
        params.update(self.lookup)

        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class Enhanced(base.Resource):
    path = 'enhanced'

    def __init__(self, parent, email):
        self.parent = parent
        self.email = email

    def get_url(self):
        return '{0}/{1}'.format(self.parent.get_url(), self.path)

    @base.apimethod
    def get(self):
        """
        Fetch a single object.
        """
        request = http.Request('GET', self.get_url(), {'email': self.email})

        return request, parsers.parse_json


class Name(base.HierarchicalResource):
    path = 'name'

    @base.apimethod
    def normalizer(self, q, casing=None):
        """
        Take quasi-structured name data provided as a string and
        outputs the data in a structured manner.

        :var q: Name you would like to be normalized.
        :vartype q: str

        :var casing: One of: uppercase, lowercase or titlecase.
        :vartype casing: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'normalizer')

        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def deducer(self, email=None, username=None, casing=None):
        """
        Take a username or email address provided as a string and
        attempts to deduce a structured name.

        :var email: It allows you to pass an email address.
        :vartype email: str

        :var username: It allows you to pass a username.
        :vartype username: str

        :var casing: One of: uppercase, lowercase or titlecase.
        :vartype casing: str
        """
        if ((email is None and username is None) or
            (email is not None and username is not None)):
           raise TypeError('deducer() must be passed just one '
                           'of email or username.')

        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'deducer')

        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def similarity(self, q1, q2, casing=None):
        """
        Return a score indicating how two names are similar.

        :var q1: First name to compare.
        :vartype q1: str

        :var q2: Second name to compare.
        :vartype q2: str

        :var casing: One of: uppercase, lowercase or titlecase.
        :vartype casing: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'similarity')

        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def stats(self, name=None, givenName=None, familyName=None, casing=None):
        """
        Determine more about a name.

        :var name: It can be used when you only know a single name and
                   you are uncertain whether it is the given name
                   or family name.
        :vartype name: str

        :var givenName: It can be used when you know that the name
                        is a first name.
        :vartype givenName: str

        :var familyName: It can be used when you know that the name
                         is a last name.
        :vartype familyName: str

        :var casing: One of: uppercase, lowercase or titlecase.
        :vartype casing: str
        """
        if ((name is None and givenName is None and familyName is None) or
            (name is not None and (
                givenName is not None or familyName is not None))):
           raise TypeError('stats() must be passed just one '
                           'of email, givenName or familyName.')

        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'stats')

        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def parser(self, q, casing=None):
        """
        Determine what the given name and family name for a ambiguious name.

        :var q: Name you would like to be parsed.
        :vartype q: str

        :var casing: One of: uppercase, lowercase or titlecase.
        :vartype casing: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'parser')

        request = http.Request('GET', url, params)

        return request, parsers.parse_json


class Location(base.HierarchicalResource):
    path = 'address'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def normalizer(self, place, includeZeroPopulation=False, casing=None):
        """
        Return structured location data for a indicated place.

        :var place: The place you are interested in.
        :vartype place: str

        :var includeZeroPopulation: Will include 0 population census locations.
        :vartype includeZeroPopulation: bool

        :var casing: One of: uppercase, lowercase or titlecase.
        :vartype casing: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'locationNormalizer')

        request = http.Request('GET', url, params)

        return request, parsers.parse_json

    @base.apimethod
    def enrichment(self, place, includeZeroPopulation=False, casing=None):
        """
        Return a collection of lostructured location data for a indicated place.

        :var place: The place you are interested in.
        :vartype place: str

        :var includeZeroPopulation: Will include 0 population census locations.
        :vartype includeZeroPopulation: bool

        :var casing: One of: uppercase, lowercase or titlecase.
        :vartype casing: str
        """
        params = base.get_params(None, locals())
        url = '{0}/{1}'.format(self.get_url(), 'locationEnrichment')

        request = http.Request('GET', url, params)

        return request, parsers.parse_json
