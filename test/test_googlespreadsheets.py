import unittest

from libsaas import xml
from libsaas.executors import test_executor
from libsaas.services import googlespreadsheets
from libsaas.services.base import MethodNotSupported


class GoogleSpreadsheetsTestCase(unittest.TestCase):

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://spreadsheets.google.com' + uri)

        self.assertEqual(self.executor.request.params, params)

        if headers:
            self.assertEqual(self.executor.request.headers, headers)

class GoogleSpreadsheetsXMLTestCase(GoogleSpreadsheetsTestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(
            b'<?xml version="1.0" encoding="UTF-8"?><root/>', 200, {})
        self.service = googlespreadsheets.GoogleSpreadsheets('my-token')

    def test_worksheets(self):
        create = {
            'entry': {
                '@xmlns': 'http://www.w3.org/2005/Atom',
                '@xmlns:gs': 'http://schemas.google.com/spreadsheets/2006',
                'title': 'testing',
                'gs:rowCount': 50,
                'gs:colCount': 10
            }
        }
        (self.service.spreadsheet('key').worksheets('v', 'p')
                                        .create(create.copy()))
        self.expect('POST', '/feeds/worksheets/key/v/p',
                    params=xml.dict_to_xml(create))

        update = {
            'entry': {
                '@xmlns': 'http://www.w3.org/2005/Atom',
                '@xmlns:gs': 'http://schemas.google.com/spreadsheets/2006',
                'title': 'updated',
                'gs:rowCount': 40,
                'gs:colCount': 15
            }
        }
        (self.service.spreadsheet('key').worksheet('id', 'v', 'p')
                                        .update('v1', update.copy()))
        self.expect('PUT', '/feeds/worksheets/key/v/p/id/v1',
                    params=xml.dict_to_xml(update))

        (self.service.spreadsheet('key').worksheet('id', 'v', 'p')
                                        .delete('v2'))
        self.expect('DELETE', '/feeds/worksheets/key/v/p/id/v2', None)

    def test_rows(self):
        create = {
            'entry': {
                '@xmlns': 'http://www.w3.org/2005/Atom',
                '@xmlns:gsx': 'http://schemas.google.com/spreadsheets/2006',
                'gsx:a': 7,
                'gsx:b': 'G'
            }
        }
        (self.service.spreadsheet('key').worksheet('id', 'v', 'p').rows()
                                        .create(create.copy()))
        self.expect('POST', '/feeds/list/key/id/v/p',
                    params=xml.dict_to_xml(create))

        update = {
            'entry': {
                '@xmlns': 'http://www.w3.org/2005/Atom',
                '@xmlns:gsx': 'http://schemas.google.com/spreadsheets/2006',
                'gsx:a': 10,
                'gsx:b': 'G',
                'gsx:c': 14
            }
        }
        (self.service.spreadsheet('key').worksheet('id', 'v', 'p').row('row')
                                        .update('v1', update.copy()))
        self.expect('PUT', '/feeds/list/key/id/v/p/row/v1',
                    params=xml.dict_to_xml(update))

        (self.service.spreadsheet('key').worksheet('id', 'v', 'p').row('row')
                                        .delete('v2'))
        self.expect('DELETE', '/feeds/list/key/id/v/p/row/v2', None)

    def test_cells(self):
        with self.assertRaises(MethodNotSupported):
            (self.service.spreadsheet('key').worksheet('id', 'v', 'p').cells()
                                            .create({}))
            (self.service.spreadsheet('key').worksheet('id', 'v', 'p')\
                                            .cell('cell').delete('v1'))

        cell = {
            'entry': {
                '@xmlns': 'http://www.w3.org/2005/Atom',
                '@xmlns:gs': 'http://schemas.google.com/spreadsheets/2006',
                'gs:cell': {
                    '@inputValue': '=SUM(A2:A3)',
                    '@row': '5',
                    '@col': '1'
                }
            }
        }
        (self.service.spreadsheet('key').worksheet('id', 'v', 'p').cell('R5C1')
                                        .update('v1', cell.copy()))
        self.expect('PUT', '/feeds/cells/key/id/v/p/R5C1/v1',
                    params=xml.dict_to_xml(cell))


class GoogleSpreadsheetsJSONTestCase(GoogleSpreadsheetsTestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})
        self.service = googlespreadsheets.GoogleSpreadsheets('my-token')

    def test_spreadsheets(self):
        self.service.spreadsheets().get()
        self.expect('GET', '/feeds/spreadsheets/private/full',
                    {'alt': 'json'})

        with self.assertRaises(MethodNotSupported):
            self.service.spreadsheet('key').get()

        self.service.spreadsheet('key').worksheets('v', 'p').get()
        self.expect('GET', '/feeds/worksheets/key/v/p',
                    {'alt': 'json'})

        self.service.spreadsheet('key').worksheet('id', 'v', 'p').get()
        self.expect('GET', '/feeds/worksheets/key/v/p/id',
                    {'alt': 'json'})

        self.service.spreadsheet('key').worksheet('id', 'v', 'p').rows().get()
        self.expect('GET', '/feeds/list/key/id/v/p',
                    {'alt': 'json'})

        (self.service.spreadsheet('key').worksheet('id', 'v', 'p')
                                        .rows().get(reverse=True))
        self.expect('GET', '/feeds/list/key/id/v/p',
                    {'alt': 'json', 'reverse': 'true'})

        (self.service.spreadsheet('key').worksheet('id', 'v', 'p')
                                        .rows().get(sq='height>100'))
        self.expect('GET', '/feeds/list/key/id/v/p',
                    {'alt': 'json', 'sq': 'height>100'})

        with self.assertRaises(MethodNotSupported):
            (self.service.spreadsheet('key').worksheet('id', 'v', 'p')
                                            .row('row').get())

        self.service.spreadsheet('key').worksheet('id', 'v', 'p').cells().get()
        self.expect('GET', '/feeds/cells/key/id/v/p',
                    {'alt': 'json'})

        (self.service.spreadsheet('key').worksheet('id', 'v', 'p')
                                        .cells().get(min_col=2, max_col=4))
        self.expect('GET', '/feeds/cells/key/id/v/p',
                    {'alt': 'json', 'min-col': 2, 'max-col': 4})

        (self.service.spreadsheet('key').worksheet('id', 'v', 'p')
                                        .cells().get(min_row=2, max_row=4))
        self.expect('GET', '/feeds/cells/key/id/v/p',
                    {'alt': 'json', 'min-row': 2, 'max-row': 4})

        (self.service.spreadsheet('key').worksheet('id', 'v', 'p')
                                        .cell('cell').get())
        self.expect('GET', '/feeds/cells/key/id/v/p/cell',
                    {'alt': 'json'})
