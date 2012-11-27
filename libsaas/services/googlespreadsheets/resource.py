from libsaas import http, parsers
from libsaas.services import base


def translate_param(val):
    return val.replace('_', '-')


class SpreadsheetsResource(base.RESTResource):

    APIROOT = 'https://spreadsheets.google.com/feeds'

    def __init__(self, *args, **kwargs):
        self.version = None
        return super(SpreadsheetsResource, self).__init__(*args, **kwargs)

    @base.apimethod
    def create(self, obj):
        """
        Create a new resource.

        :var obj: a Python object representing the resource to be created,
            usually in the same as returned from `get`. Refer to the upstream
            documentation for details.
        """
        self.require_collection()
        request = http.Request('POST', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_xml

    @base.apimethod
    def update(self, version, obj):
        """
        Update this resource.

        :var version: the resource version you want to update.
        :vartype version: str
        :var obj: a Python object representing the updated resource, usually in
            the same format as returned from `get`. Refer to the upstream
            documentation for details.
        """
        self.require_item()
        self.version = version
        request = http.Request('PUT', self.get_url(), self.wrap_object(obj))

        return request, parsers.parse_xml

    @base.apimethod
    def delete(self, version):
        """
        Delete this resource.

        :var version: the resource version you want to delete.
        :vartype version: str
        """
        self.require_item()
        self.version = version
        request = http.Request('DELETE', self.get_url())

        return request, parsers.parse_empty


class ListResource(SpreadsheetsResource):

    def get_url(self):
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(
                self.APIROOT,
                self.path,
                self.parent.parent.object_id,
                self.parent.object_id,
                self.parent.visibility,
                self.parent.projection)

        if self.object_id is not None:
            url = '{0}/{1}'.format(url, self.object_id)

        if self.version is not None:
            url = '{0}/{1}'.format(url, self.version)

        return url


class RowResource(ListResource):
    path = 'list'


class Rows(RowResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, reverse=None, orderby=None, sq=None):
        """
        Fetch rows for the worksheet.

        :var reverse: To get rows in reverse order
        :vartype reverse: bool
        :var orderby: To sort the values in ascending order by a
            particular column.
        :vartype orderby: str
        :var sq: Use it to produce a feed with entries that meet
            the specified criteria.
        :vartype sq: str
        """
        params = base.get_params(None, locals())
        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

class Row(RowResource):

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()


class CellResource(ListResource):
    path = 'cells'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Cells(CellResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.apimethod
    def get(self, min_row=None, max_row=None, min_col=None, max_col=None):
        """
        Fetch cells for the worksheet.

        :var min_row: To get cells above the indicated row.
        :vartype min_row: int
        :var max_row: To get cells below the given row.
        :vartype max_row: int
        :var min_col: To get cells from the indicated column.
        :vartype min_col: int
        :var max_col: To get cells to the given column.
        :vartype max_col: int
        """
        params = base.get_params(None, locals(),
                                 translate_param=translate_param)

        request = http.Request('GET', self.get_url(), params)

        return request, parsers.parse_json

class Cell(CellResource):

    pass


class WorksheetResource(SpreadsheetsResource):

    path = 'worksheets'

    def __init__(self, parent, object_id=None,
                visibility='private', projection='full'):
        """
        Worksheet resource constructor.

        :var visibility: private or public object's visibility.
        :vartype visibility: str
        :var projection: full or basic projection, causing the feed
            to return less information (i.e. fewer fields, and only
            the most important data).
        :vartype projection: str
        """
        super(WorksheetResource, self).__init__(parent, object_id)
        self.visibility = visibility
        self.projection = projection

    def get_url(self):
        url = '{0}/{1}/{2}/{3}/{4}'.format(
                    self.parent.get_url(),
                    self.path,
                    self.parent.object_id,
                    self.visibility,
                    self.projection)

        if self.object_id is not None:
            url = '{0}/{1}'.format(url, self.object_id)

        if self.version is not None:
            url = '{0}/{1}'.format(url, self.version)

        return url


class Worksheets(WorksheetResource):

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Worksheet(WorksheetResource):

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(Rows)
    def rows(self):
        """
        Return the resource corresponding to all the rows
        """
        return Rows(self)

    @base.resource(Row)
    def row(self, row_id):
        """
        Return the resource corresponding to a single row
        """
        return Row(self, row_id)

    @base.resource(Cells)
    def cells(self):
        """
        Return the resource corresponding to all the cells
        """
        return Cells(self)

    @base.resource(Cell)
    def cell(self, cell_id):
        """
        Return the resource corresponding to a single cell
        """
        return Cell(self, cell_id)


class Spreadsheets(SpreadsheetsResource):

    path = 'spreadsheets/private/full'

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()


class Spreadsheet(SpreadsheetsResource):

    def get_url(self):
        return self.parent.get_url()

    def get(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def create(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def update(self, *args, **kwargs):
        raise base.MethodNotSupported()

    def delete(self, *args, **kwargs):
        raise base.MethodNotSupported()

    @base.resource(Worksheets)
    def worksheets(self, visibility, projection):
        """
        Return the resource corresponding to all the worksheets
        """
        return Worksheets(self, visibility=visibility, projection=projection)

    @base.resource(Worksheet)
    def worksheet(self, worksheet_id, visibility, projection):
        """
        Return the resource corresponding to a single worksheet
        """
        return Worksheet(self, worksheet_id, visibility, projection)
