import unittest

from libsaas import xml


class XMLParserTestCase(unittest.TestCase):

    xml_header = b'<?xml version="1.0" encoding="UTF-8"?>'
    xml_duck = b'''<duck>
                    <article href="http://en.wikipedia.org/wiki/Donald_Duck"/>
                    <name>Donald</name>
                    <birth_date type="datetime">1934-06-04</birth_date>
                    <first_film/>
                    <last_film></last_film>
                    <species href="http://en.wikipedia.org/wiki/Pekin_duck">
                        Pekin duck
                    </species>
                    <created_by href="http://en.wikipedia.org/wiki/Disney">
                        <name>Walt Disney</name>
                        <cryopreserved type="boolean">true</cryopreserved>
                    </created_by>
                    <family>
                        <children type="array"></children>
                        <uncles type="array">
                            <uncle><name>Scrooge McDuck</name></uncle>
                            <uncle><name>Ludwig Von Drake</name></uncle>
                        </uncles>
                        <nephew><name>Huey</name></nephew>
                        <nephew><name>Dewey</name></nephew>
                        <nephew><name>Louie</name></nephew>
                    </family>
                </duck>'''

    def check_duck(self, duck):
        """
        Checks the given dict representing the above xml duck is ok
        """
        self.assertEqual(duck['name'], 'Donald')
        self.assertEqual(duck['first_film'], None)
        self.assertTrue('@href' in duck['article'])
        self.assertTrue('@href' in duck['species'])
        self.assertTrue(duck['species']['species'], 'Pekin duck')
        self.assertEqual(duck['created_by']['name'], 'Walt Disney')
        self.assertTrue(duck['created_by']['cryopreserved'])

        family = duck['family']
        self.assertEqual(len(family['uncles']['uncle']), 2)
        self.assertEqual(len(family['nephew']), 3)
        self.assertFalse(family['children'])

    def test_encoding(self):
        u_test = (b'<?xml version="1.0" encoding="latin1"?>'
                  b'<team><boolean>True</boolean>'
                  b'<name>Bar\xe7a</name>'
                  b'<nil />'
                  b'<number>1234</number></team>')
        resp = xml.parse_xml(u_test, 200, None)
        self.assertEqual(resp['team']['name'], b'Bar\xe7a'.decode('latin1'))

        u_test = (b'<?xml version="1.0" encoding="UTF-8"?>'
                  b'<team><boolean>True</boolean>'
                  b'<name>Bar\xc3\xa7a</name>'
                  b'<nil />'
                  b'<number>1234</number></team>')
        resp = xml.parse_xml(u_test, 200, None)
        self.assertEqual(resp['team']['name'], b'Bar\xc3\xa7a'.decode('utf-8'))

        resp = xml.dict_to_xml({'team': {
            'name': b'Bar\xc3\xa7a'.decode('utf-8'),
            'boolean': True,
            'number': 1234,
            'nil': None
        }})
        self.assertEqual(resp, u_test)

    def test_syntax_error(self):
        wrong_xml = (b'<?xml version="1.0" encoding="UTF-8"?>'
                     b'<ducks type="array"><duck/><pig/></ducks>')
        self.assertRaises(xml.XMLParserException,
                          xml.parse_xml, wrong_xml, 200, None)

    def test_basic_usage(self):
        resp1 = xml.parse_xml(self.xml_header + self.xml_duck, 200, None)
        duck1 = resp1['duck']
        self.check_duck(duck1)

        # From generated xml: generate a dict; then, parse it again
        # It must be exactly the same than the very first dict
        resp2 = xml.parse_xml(xml.dict_to_xml(resp1), 200, None)
        duck2 = resp2['duck']
        self.check_duck(duck2)

        # Now, let's test an array...
        xml_doc = self.xml_header
        xml_doc += b'<ducks>'
        xml_doc += self.xml_duck
        xml_doc += self.xml_duck
        xml_doc += b'</ducks>'
        resp3 = xml.parse_xml(xml_doc, 200, None)
        ducks = resp3['ducks']['duck']
        for duck in ducks:
            self.check_duck(duck)
