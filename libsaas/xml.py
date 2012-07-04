"""
XML utilities.
"""
from __future__ import absolute_import

import collections
import os

from libsaas import http, port


# check for explicit request to use a specific library
_library = os.getenv("LIBSAAS_XML_LIBRARY")

if _library == "lxml":
    from lxml import etree
elif _library == "cElementTree":
    from xml.etree import cElementTree as etree
elif _library == "ElementTree":
    from xml.etree import ElementTree as etree
else:
    # try various implementations until one works
    try:
        from lxml import etree
    except ImportError:
        try:
            from xml.etree import cElementTree as etree
        except ImportError:
            from xml.etree import ElementTree as etree

del _library


class XMLParserException(Exception):
    """
    XML document not well formed
    """
    def __str__(self):
        return self.__doc__


def value_for_element(elem):
    # We want to have tag attributes
    elem_dict = dict(
        ('@{0}'.format(attrib), value)
        for attrib, value in elem.attrib.items() if attrib != 'type'
    )

    elem_text = elem.text and elem.text.strip()
    elem_type = elem.attrib.get('type', None)

    if elem_type == 'integer':
        value = int(elem_text)
    elif elem_type == 'float':
        value = float(elem_text)
    elif elem_type == 'boolean':
        value = elem_text.lower() == 'true'
    elif elem_type == 'array':
        tags = set([child.tag for child in elem])

        if not tags:
            return []

        if len(tags) > 1:
            raise XMLParserException()

        value = {
            tags.pop(): [value_for_element(child) for child in elem]
        }
    else:
        value = elem_text

    if not value:
        d = collections.defaultdict(list)
        for child in elem:
            d[child.tag].append(value_for_element(child))

        for key, value in d.items():
            if len(value) == 1:
                elem_dict[key] = value[0]
            else:
                elem_dict[key] = value

        return elem_dict or None

    if elem_dict:
        elem_dict.update({elem.tag: value})
        return elem_dict
    else:
        return value


def parse_xml(body, code, headers):
    """
    Return a dictionary.

    Transformation is done assuming:
    1.  If a tag indicates its value type, we'll try to cast it.
    2.  Siblings with the same tag name, become a list.
    3.  Attributes become a dict key starting with '@'.

    <duck>
        <name>Donald</name>
        <birth_date type="datetime">1934-06-04T00:00:00</birth_date>
        <first_film/>
        <last_film></last_film>
        <species href="http://en.wikipedia.org/wiki/Pekin_duck"/>
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
    </duck>

    {'duck': {'birth_date': '1934-06-04T00:00:00',
              'created_by': {'@href': 'http://en.wikipedia.org/wiki/Disney',
                             'cryopreserved': True,
                             'name': 'Walt Disney'},
              'family': {'nephew': [{'name': 'Huey'},
                                    {'name': 'Dewey'},
                                    {'name': 'Louie'}],
                         'children': [],
                         'uncles': {'uncle': [{'name': 'Scrooge McDuck'},
                                              {'name': 'Ludwig Von Drake'}]}},
              'first_film': None,
              'last_film': None,
              'name': 'Donald',
              'species': {'@href': 'http://en.wikipedia.org/wiki/Pekin_duck'}}
    }
    """
    if not 200 <= code < 300:
        raise http.HTTPError(body, code, headers)

    root_elem = etree.fromstring(body)
    return {
        root_elem.tag: value_for_element(root_elem)
    }


def element_for_value(obj, parent):
    for key, value in obj.items():
        if isinstance(value, dict):
            node = etree.SubElement(parent, key)
            element_for_value(value, node)
        elif isinstance(value, list):
            if not value:
                node = etree.SubElement(parent, key)

            for item in value:
                node = etree.SubElement(parent, key)
                element_for_value(item, node)
        else:
            if key.startswith('@'):
                parent.set(key.lstrip('@'), value)
            else:
                node = etree.SubElement(parent, key)
                node.text = (port.to_u(value)
                             if value is not None else port.to_u(''))


def dict_to_xml(obj):
    """
    Return a xml representation of the given dictionary:
    1.  keys of the dictionary become sublements.
    2.  if a value is a list, then key is a set of sublements.
    3.  keys starting with '@' became an attribute.

    {'duck': {'birth_date': '1934-06-04T00:00:00',
              'created_by': {'@href': 'http://en.wikipedia.org/wiki/Disney',
                             'cryopreserved': True,
                             'name': 'Walt Disney'},
              'family': {'nephew': [{'name': 'Huey'},
                                    {'name': 'Dewey'},
                                    {'name': 'Louie'}],
                         'children': [],
                         'uncles': {'uncle': [{'name': 'Scrooge McDuck'},
                                              {'name': 'Ludwig Von Drake'}]}},
              'first_film': None,
              'last_film': None,
              'name': 'Donald',
              'species': {'@href': 'http://en.wikipedia.org/wiki/Pekin_duck'}}
    }

    <?xml version="1.0" encoding="UTF-8"?>
    <duck>
        <name>Donald</name>
        <family>
            <children />
            <nephew><name>Huey</name></nephew>
            <nephew><name>Dewey</name></nephew>
            <nephew><name>Louie</name></nephew>
            <uncles>
                <uncle><name>Scrooge McDuck</name></uncle>
                <uncle><name>Ludwig Von Drake</name></uncle>
            </uncles>
        </family>
        <last_film />
        <first_film />
        <created_by href="http://en.wikipedia.org/wiki/Disney">
            <cryopreserved>True</cryopreserved>
            <name>Walt Disney</name>
        </created_by>
        <birth_date>1934-06-04T00:00:00</birth_date>
        <species href="http://en.wikipedia.org/wiki/Pekin_duck" />
    </duck>
    """
    if not obj:
        return

    # top level dictionary must contain a single entry
    # corresponding to the root element
    key, value = obj.popitem()

    root = etree.Element(key)
    element_for_value(value, root)
    return (b'<?xml version="1.0" encoding="UTF-8"?>' +
                etree.tostring(root, encoding='utf-8'))
