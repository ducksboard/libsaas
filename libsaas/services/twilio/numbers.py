from libsaas import http, parsers
from libsaas.services import base

from libsaas.services.twilio import resource


class AvailablePhoneNumbersBase(resource.TwilioResource):

    path = '{0}'

    def get_url(self):
        path = self.path.format(self.object_id)
        return '{0}/{1}'.format(self.parent.get_url(), path)

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class AvailablePhoneNumbersLocal(AvailablePhoneNumbersBase):

    path = '{0}/Local'

    @base.apimethod
    def get(self, AreaCode=None, Contains=None, InRegion=None,
            InPostalCode=None, NearLatLong=None, NearNumber=None, InLata=None,
            InRateCenter=None, Distance=None):
        """
        Fetch available local phone numbers for an account.

        :var AreaCode: Find phone numbers in the specified area code.
        :vartype AreaCode: str

        :var Contains: A pattern to match phone numbers on.
            Valid characters are `*` and [0-9a-zA-Z].
            The `*` character will match any single digit.
        :vartype Contains: str

        :var InRegion: Limit results to a particular region (State/Province).
            Given a phone number, search within the same Region as that number.
            (US and Canada only)
        :vartype InRegion: str

        :var InPostalCode: Limit results to a particular postal code.
            Given a phone number, search within the same postal code as
            that number. (US and Canada only)
        :vartype InPostalCode: str

        :var NearLatLong: Given a latitude/longitude pair lat,long find
            geographically close numbers within Distance miles.
            (US and Canada only)
        :vartype NearLatLong: str

        :var NearNumber: Given a phone number, find a geographically close
            number within Distance miles. Distance defaults to 25 miles.
            (US and Canada only)
        :vartype NearNumber: str

        :var InLata: Limit results to a specific Local access and transport
            area (LATA). Given a phone number, search within the same LATA
            as that number.
            (US and Canada only)
        :vartype InLata: str

        :var InRateCenter: Limit results to a specific rate center,
            or given a phone number search within the same rate center as
            that number. Requires InLata to be set as well.
            (US and Canada only)
        :vartype InRateCenter: str

        :var InDistance: Specifies the search radius for a Near- query in miles.
            If not specified this defaults to 25 miles.
            (US and Canada only)
        :vartype InDistance: int
        """
        params = resource.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class AvailablePhoneNumbersTollFree(AvailablePhoneNumbersBase):

    path = '{0}/TollFree'

    @base.apimethod
    def get(self, AreaCode=None, Contains=None):
        """
        Fetch available toll-free phone numbers for an account.

        :var AreaCode: Find phone numbers in the specified area code.
        :vartype AreaCode: str

        :var Contains: A pattern to match phone numbers on.
            Valid characters are `*` and [0-9a-zA-Z].
            The `*` character will match any single digit.
        :vartype Contains: str
        """
        params = resource.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json


class AvailablePhoneNumbers(AvailablePhoneNumbersBase):

    path = 'AvailablePhoneNumbers'

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(AvailablePhoneNumbersLocal)
    def local(self, country_code):
        """
        Return a list of local AvailablePhoneNumber resource representations
        that match the specified filters, each representing a phone number
        that is currently available for provisioning within this account.
        """
        return AvailablePhoneNumbersLocal(self, country_code)

    @base.resource(AvailablePhoneNumbersTollFree)
    def toll_free(self, country_code):
        """
        Return a list of toll-free AvailablePhoneNumber resource
        representations that match the specified filters, each representing
        a phone number that is currently available for provisioning within
        this account.
        """
        return AvailablePhoneNumbersTollFree(self, country_code)


class IncomingPhoneNumbersBase(resource.TwilioResource):

    path = 'IncomingPhoneNumbers'


class IncomingPhoneNumber(IncomingPhoneNumbersBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class IncomingPhoneNumbersMixin(IncomingPhoneNumbersBase):

    @base.apimethod
    def get(self, PhoneNumber=None, FriendlyName=None,
            Page=None, PageSize=None, AfterSid=None):
        """
        Fetch incoming phone numbers list for an account.

        :var PhoneNumber: Only show the incoming phone number resources
            that match this pattern. You can specify partial numbers and
            use `*` as a wildcard for any digit.
        :vartype PhoneNumber: str

        :var FriendlyName: Only show the incoming phone number resources
            with friendly names that exactly match this name.
        :vartype FriendlyName: str

        :var Page: The current page number. Zero-indexed, so the first page
            is 0.
        :vartype Page: int

        :var PageSize: How many resources to return in each list page.
            The default is 50, and the maximum is 1000.
        :vartype PageSize: int

        :var AfterSid: The last Sid returned in the previous page, used to
            avoid listing duplicated resources if new ones are created while
            paging.
        :vartype AfterSid: str
        """
        params = resource.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class IncomingPhoneNumbersLocal(IncomingPhoneNumbersMixin):

    path = 'Local'


class IncomingPhoneNumbersTollFree(IncomingPhoneNumbersMixin):

    path = 'TollFree'


class IncomingPhoneNumbers(IncomingPhoneNumbersMixin):

    @base.resource(IncomingPhoneNumbersLocal)
    def local(self):
        return IncomingPhoneNumbersLocal(self)

    @base.resource(IncomingPhoneNumbersTollFree)
    def toll_free(self):
        return IncomingPhoneNumbersTollFree(self)


class OutgoingCallerIdsBase(resource.TwilioResource):

    path = 'OutgoingCallerIds'


class OutgoingCallerId(OutgoingCallerIdsBase):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class OutgoingCallerIds(OutgoingCallerIdsBase):

    @base.apimethod
    def get(self, PhoneNumber=None, FriendlyName=None,
            Page=None, PageSize=None, AfterSid=None):
        """
        Fetch outgoing caller ids for an account.

        :var PhoneNumber: Only show the incoming phone number resources
            that match this pattern. You can specify partial numbers and
            use `*` as a wildcard for any digit.
        :vartype PhoneNumber: str

        :var FriendlyName: Only show the incoming phone number resources
            with friendly names that exactly match this name.
        :vartype FriendlyName: str

        :var Page: The current page number. Zero-indexed, so the first page
            is 0.
        :vartype Page: int

        :var PageSize: How many resources to return in each list page.
            The default is 50, and the maximum is 1000.
        :vartype PageSize: int

        :var AfterSid: The last Sid returned in the previous page, used to
            avoid listing duplicated resources if new ones are created while
            paging.
        :vartype AfterSid: str
        """
        params = resource.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()
