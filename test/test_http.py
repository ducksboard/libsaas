import unittest

from libsaas import http


class SerializeFlattenTestCase(unittest.TestCase):

    def test_flatten(self):
        s = http.serialize_flatten('p1', ['v1', 'v2', 'v3'])
        self.assertEqual(s, {'p1[0]': 'v1', 'p1[1]': 'v2', 'p1[2]': 'v3'})

        s = http.serialize_flatten('p1', [{'k1': 'v1', 'k2': True},
                                          {'k1': 'v2', 'k2': False}])
        self.assertEqual(s, {'p1[0][k1]': 'v1', 'p1[0][k2]': 'true',
                             'p1[1][k1]': 'v2', 'p1[1][k2]': 'false'})
