import json

from libsaas import http, parsers
from libsaas.services import base

from . import activities, currencies, deals, files, filters, goals, notes
from . import organizations, persons, pipelines, products, users


class Pipedrive(base.Resource):
    """
    """
    def __init__(self, api_token):
        """
        Create a Pipedrive service.

        :var api_token: The API token
        :vartype api_token: str
        """
        self.apiroot = 'https://api.pipedrive.com/v1'
        self.api_token = api_token
        self.add_filter(self.add_auth)

    def get_url(self):
        return self.apiroot

    def add_auth(self, request):
        request.headers['Content-Type'] = 'application/json'

        params = {'api_token': self.api_token}

        if request.method.upper() in http.URLENCODE_METHODS:
            request.params.update(params)
        else:
            request.params = json.dumps(request.params)
            request.uri += '?' + http.urlencode_any(params)

    @base.resource(activities.ActivityType)
    def activity_type(self, type_id):
        """
        Return the resource corresponding to a single activity type

        :var type_id: The activity type id
        :vartype type_id: str
        """
        return activities.ActivityType(self, type_id)

    @base.resource(activities.ActivityTypes)
    def activity_types(self):
        """
        Return the resource corresponding to all activity types
        """
        return activities.ActivityTypes(self)

    @base.resource(activities.Activity)
    def activity(self, activity_id):
        """
        Return the resource corresponding to a single activity

        :var activity_id: The activity id
        :vartype activity_id: str
        """
        return activities.Activity(self, activity_id)

    @base.resource(activities.Activities)
    def activities(self):
        """
        Return the resource corresponding to all activities
        """
        return activities.Activities(self)

    @base.resource(users.Authorizations)
    def authorizations(self):
        """
        Return the resource corresponding to the user authorizations
        """
        return users.Authorizations(self)

    @base.resource(users.UserConnections)
    def user_connections(self):
        """
        Return the resource corresponding to the user connections
        """
        return users.UserConnections(self)

    @base.resource(users.User)
    def user(self, user_id):
        """
        Return the resource corresponding to a single user

        :var user_id: The user id
        :vartype user_id: str
        """
        return users.User(self, user_id)

    @base.resource(users.Users)
    def users(self):
        """
        Return the resource corresponding to all users
        """
        return users.Users(self)

    @base.resource(currencies.Currencies)
    def currencies(self):
        """
        Return the resource corresponding to the deals currencies
        """
        return currencies.Currencies(self)

    @base.resource(deals.DealField)
    def deal_field(self, field_id):
        """
        Return the resource corresponding to a single deal field

        :var field_id: The deal field id
        :vartype field_id: str
        """
        return deals.DealField(self, field_id)

    @base.resource(deals.DealFields)
    def deal_fields(self):
        """
        Return the resource corresponding to all deal fields
        """
        return deals.DealFields(self)

    @base.resource(deals.Deal)
    def deal(self, deal_id):
        """
        Return the resource corresponding to a single deal

        :var deal_id: The deal id
        :vartype deal_id: str
        """
        return deals.Deal(self, deal_id)

    @base.resource(deals.Deals)
    def deals(self):
        """
        Return the resource corresponding to all deals
        """
        return deals.Deals(self)

    @base.resource(files.File)
    def file(self, file_id):
        """
        Return the resource corresponding to a single file

        :var file_id: The file id
        :vartype file_id: str
        """
        return files.File(self, file_id)

    @base.resource(files.Files)
    def files(self):
        """
        Return the resource corresponding to all files
        """
        return files.Files(self)

    @base.resource(filters.Filter)
    def condition_filter(self, filter_id):
        """
        Return the resource corresponding to a single filter

        :var filter_id: The filter id
        :vartype filter_id: str
        """
        return filters.Filter(self, filter_id)

    @base.resource(filters.Filters)
    def condition_filters(self):
        """
        Return the resource corresponding to all filters
        """
        return filters.Filters(self)

    @base.resource(notes.Note)
    def note(self, note_id):
        """
        Return the resource corresponding to a single note

        :var note_id: The note id
        :vartype note_id: str
        """
        return notes.Note(self, note_id)

    @base.resource(notes.Notes)
    def notes(self):
        """
        Return the resource corresponding to all notes
        """
        return notes.Notes(self)

    @base.resource(organizations.OrganizationField)
    def organization_field(self, field_id):
        """
        Return the resource corresponding to a single organization field

        :var field_id: The organization field id
        :vartype field_id: str
        """
        return organizations.OrganizationField(self, field_id)

    @base.resource(organizations.OrganizationFields)
    def organization_fields(self):
        """
        Return the resource corresponding to all organization fields
        """
        return organizations.OrganizationFields(self)

    @base.resource(organizations.Organization)
    def organization(self, organization_id):
        """
        Return the resource corresponding to a single organization

        :var organization_id: The organization id
        :vartype organization_id: str
        """
        return organizations.Organization(self, organization_id)

    @base.resource(organizations.Organizations)
    def organizations(self):
        """
        Return the resource corresponding to all organizations
        """
        return organizations.Organizations(self)

    @base.resource(persons.PersonField)
    def person_field(self, field_id):
        """
        Return the resource corresponding to a single person field

        :var field_id: The person field id
        :vartype field_id: str
        """
        return persons.PersonField(self, field_id)

    @base.resource(persons.PersonFields)
    def person_fields(self):
        """
        Return the resource corresponding to all person fields
        """
        return persons.PersonFields(self)

    @base.resource(persons.Person)
    def person(self, person_id):
        """
        Return the resource corresponding to a single person

        :var person_id: The person id
        :vartype person_id: str
        """
        return persons.Person(self, person_id)

    @base.resource(persons.Persons)
    def persons(self):
        """
        Return the resource corresponding to all persons
        """
        return persons.Persons(self)

    @base.resource(pipelines.Stage)
    def stage(self, stage_id):
        """
        Return the resource corresponding to a single stage

        :var stage_id: The stage id
        :vartype stage_id: str
        """
        return pipelines.Stage(self, stage_id)

    @base.resource(pipelines.Stages)
    def stages(self):
        """
        Return the resource corresponding to all stages
        """
        return pipelines.Stages(self)

    @base.resource(pipelines.Pipeline)
    def pipeline(self, pipeline_id):
        """
        Return the resource corresponding to a single pipeline

        :var pipeline_id: The pipeline id
        :vartype pipeline_id: str
        """
        return pipelines.Pipeline(self, pipeline_id)

    @base.resource(pipelines.Pipelines)
    def pipelines(self):
        """
        Return the resource corresponding to all pipelines
        """
        return pipelines.Pipelines(self)

    @base.resource(products.ProductField)
    def product_field(self, field_id):
        """
        Return the resource corresponding to a single product field

        :var field_id: The product field id
        :vartype field_id: str
        """
        return products.ProductField(self, field_id)

    @base.resource(products.ProductFields)
    def product_fields(self):
        """
        Return the resource corresponding to all product fields
        """
        return products.ProductFields(self)

    @base.resource(products.Product)
    def product(self, product_id):
        """
        Return the resource corresponding to a single product

        :var product_id: The product id
        :vartype product_id: str
        """
        return products.Product(self, product_id)

    @base.resource(products.Products)
    def products(self):
        """
        Return the resource corresponding to all products
        """
        return products.Products(self)

    @base.apimethod
    def search(self, term, start=None, limit=None):
        """
        Performs a search across the account and returns SearchResults.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-SearchResults
        """
        params = base.get_params(None, locals())
        url = '{0}/searchResults'.format(self.get_url())
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def settings(self):
        """
        Lists settings of authorized user.

        Upstream documentation:
        https://developers.pipedrive.com/v1#methods-UserSettings
        """
        url = '{0}/userSettings'.format(self.get_url())
        return http.Request('GET', url), parsers.parse_json

    @base.resource(goals.Goal)
    def goal(self, goal_id):
        """
        Return the resource corresponding to a single goal

        :var goal_id: The goal id
        :vartype goal_id: str
        """
        return goals.Goal(self, goal_id)

    @base.resource(goals.Goals)
    def goals(self):
        """
        Return the resource corresponding to all goals
        """
        return goals.Goals(self)
