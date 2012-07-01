from libsaas import http, parsers
from libsaas.services import base

from . import resource


class Emails(resource.BitBucketResource):

    path = 'emails'

    @base.apimethod
    def add(self, address):
        """
        Add an email to the user account.
        """
        return http.Request('PUT', '{0}/{1}'.format(
                self.get_url(), address)), parsers.parse_json

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Email(resource.BitBucketResource):

    def __init__(self, parent, email):
        self.parent = parent
        self.email = email

    def get_url(self):
        return '{0}/emails/{1}/'.format(self.parent.get_url(), self.email)

    @base.apimethod
    def primary(self):
        """
        Set this email as de primary email.
        """
        return http.Request('POST', '{0}'.format(self.get_url()),
                self.wrap_object({'primary': 'true'})), parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Delete this email address from the user account
        """
        return http.Request('DELETE', '{0}'.format(
                            self.get_url())), parsers.parse_json
