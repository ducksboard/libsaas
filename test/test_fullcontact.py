import unittest

from libsaas.executors import test_executor
from libsaas.services import fullcontact
from libsaas import port


class FullcontactTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = fullcontact.Fullcontact('my-api-key')

    def expect(self, method=None, uri=None, params={}):
        if method:
            self.assertEqual(method, self.executor.request.method)

        if uri:
            self.assertEqual(
                self.executor.request.uri,
                'https://api.fullcontact.com/v2' + uri)

        if params:
            params.update({'apiKey': 'my-api-key'})
            self.assertEqual(self.executor.request.params, params)

    def test_persons(self):
        self.service.person(email='email').get()
        self.expect('GET', '/person.json', {'email': 'email'})
        self.service.person(twitter='twitter').get()
        self.expect('GET', '/person.json', {'twitter': 'twitter'})

        with port.assertRaises(TypeError):
            self.service.person(email='email', facebookUsername='fb').get()

        self.service.person(email='email').get(queue=1)
        self.expect('GET', '/person.json', {
            'email': 'email',
            'queue': 1,
        })
        self.service.person(twitter='twitter').get(prettyPrint='dictionary')
        self.expect('GET', '/person.json', {
            'twitter': 'twitter',
            'prettyPrint': 'dictionary',
        })

    def test_enhanced(self):
        self.service.enhanced(email='email').get()
        self.expect('GET', '/enhanced.json', {'email': 'email'})

    def test_names(self):
        with port.assertRaises(TypeError):
            self.service.names().normalizer()

        self.service.names().normalizer('name')
        self.expect('GET', '/name/normalizer.json', {'q': 'name'})
        self.service.names().normalizer('name', 'lowercase')
        self.expect('GET', '/name/normalizer.json', {
            'q': 'name',
            'casing': 'lowercase'
        })

        with port.assertRaises(TypeError):
            self.service.names().deducer()
            self.service.names().deducer('email', 'username')

        self.service.names().deducer(email='email')
        self.expect('GET', '/name/deducer.json', {'email': 'email'})

        with port.assertRaises(TypeError):
            self.service.names().similarity()

        self.service.names().similarity('q1', 'q2')
        self.expect('GET', '/name/similarity.json', {'q1': 'q1', 'q2': 'q2'})
        self.service.names().similarity('q1', 'q2', 'titlecase')
        self.expect('GET', '/name/similarity.json', {
            'q1': 'q1',
            'q2': 'q2',
            'casing': 'titlecase'
        })

        with port.assertRaises(TypeError):
            self.service.names().stats()
            self.service.names().stats('name', 'givenName')

        self.service.names().stats('name')
        self.expect('GET', '/name/stats.json', {'name': 'name'})
        self.service.names().stats(givenName='name')
        self.expect('GET', '/name/stats.json', {'givenName': 'name'})
        self.service.names().stats(givenName='name', familyName='name')
        self.expect('GET', '/name/stats.json', {
            'givenName': 'name',
            'familyName': 'name',
        })

        with port.assertRaises(TypeError):
            self.service.names().parser()

        self.service.names().parser('name')
        self.expect('GET', '/name/parser.json', {'q': 'name'})
        self.service.names().parser('name', 'lowercase')
        self.expect('GET', '/name/parser.json', {
            'q': 'name',
            'casing': 'lowercase'
        })

    def test_locations(self):
        with port.assertRaises(TypeError):
            self.service.locations().normalizer()

        self.service.locations().normalizer('location')
        self.expect('GET', '/address/locationNormalizer.json', {
            'place': 'location',
            'includeZeroPopulation': 'false'
        })
        self.service.locations().normalizer('location', True)
        self.expect('GET', '/address/locationNormalizer.json', {
            'place': 'location',
            'includeZeroPopulation': 'true'
        })
        self.service.locations().normalizer('location', casing='lowercase')
        self.expect('GET', '/address/locationNormalizer.json', {
            'place': 'location',
            'includeZeroPopulation': 'false',
            'casing': 'lowercase'
        })

        with port.assertRaises(TypeError):
            self.service.locations().enrichment()

        self.service.locations().enrichment('location')
        self.expect('GET', '/address/locationEnrichment.json', {
            'place': 'location',
            'includeZeroPopulation': 'false'
        })
        self.service.locations().enrichment('location', True)
        self.expect('GET', '/address/locationEnrichment.json', {
            'place': 'location',
            'includeZeroPopulation': 'true'
        })
        self.service.locations().enrichment('location', casing='lowercase')
        self.expect('GET', '/address/locationEnrichment.json', {
            'place': 'location',
            'includeZeroPopulation': 'false',
            'casing': 'lowercase'
        })
