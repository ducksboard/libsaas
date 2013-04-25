import json

from libsaas.services import base
from libsaas import http

from . import resource


class Fullcontact(base.Resource):
    def __init__(self, api_key):
        """
        Create a Fullcontact service.

        :var api_key: The API key.
        :vartype api_key: str
        """
        self.apiroot = 'https://api.fullcontact.com/v2'

        self.api_key = api_key

        self.add_filter(self.use_json)
        self.add_filter(self.add_api_key)

    def get_url(self):
        return self.apiroot

    def add_api_key(self, request):
        request.params.update({'apiKey': self.api_key})

    def use_json(self, request):
        request.uri += '.json'

    @base.resource(resource.Person)
    def person(self, email=None, emailMD5=None, phone=None,
               twitter=None, facebookUsername=None):
        """
        Return the resource corresponding to a single person
        """
        kwargs = list(
            filter(None, [email, emailMD5, phone, twitter, facebookUsername,]))

        if len(kwargs) != 1:
           raise TypeError(
                'person() must be passed exactly one of '
                'email, emailMD5, phone, twitter or facebookUsername')

        return resource.Person(self, email=email, emailMD5=emailMD5, phone=phone,
                               twitter=twitter, facebookUsername=facebookUsername)

    @base.resource(resource.Enhanced)
    def enhanced(self, email):
        """
        Return the resource corresponding to a single person
        """
        return resource.Enhanced(self, email)

    @base.resource(resource.Name)
    def names(self):
        """
        Return the resource corresponding to all names.
        """
        return resource.Name(self)

    @base.resource(resource.Location)
    def locations(self):
        """
        Return the resource corresponding to all locations.
        """
        return resource.Location(self)
