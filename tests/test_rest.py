import switchmng
from switchmng import database
from switchmng.schema import *

from switchmng import config
from switchmng.schema.base import Base
from switchmng.database import DatabaseConnection
from switchmng import routes

import json

import unittest

default_headers = {
    'Content-Type': 'application/json',
    'Accept':       'application/json',
}

patch_headers = {
    'Content-Type': 'application/merge-patch+json',
    'Accept':       'application/json',
}

class Test_REST(unittest.TestCase):
    default_headers = default_headers
    patch_headers = patch_headers

    def setUp(self):
        """Helper setUp() function

        Helper setUp() function that sets up basic REST communication and
        should get called by all implementing subclasses in their setUp().
        """

        switchmng.config.parse_arguments([])
        db = DatabaseConnection('sqlite', '', False, Base)
        self.session = db.Session()
        self.app = routes.create_app(db)
        self.client = self.app.test_client()

    def _req(self, func, url, expected_code, data, headers, unpack):
        rv = func(
            url,
            data = data,
            headers = headers)

        self.assertEqual(rv.status_code, expected_code)

        if unpack:
            rv = json.loads(rv.data.decode())
            self.assertEqual(rv['status'], expected_code)

        return rv

    def _options(self, url, expected_code, data = None, headers = default_headers, unpack = False):
        return self._req(self.client.options, url, expected_code, data, headers, unpack)

    def _head(self, url, expected_code, data = None, headers = default_headers, unpack = False):
        return self._req(self.client.head, url, expected_code, data, headers, unpack)

    def _get(self, url, expected_code, data = None, headers = default_headers, unpack = True):
        return self._req(self.client.get, url, expected_code, data, headers, unpack)

    def _delete(self, url, expected_code, data = None, headers = default_headers, unpack = True):
        return self._req(self.client.delete, url, expected_code, data, headers, unpack)

    def _patch(self, url, expected_code, data = None, headers = patch_headers, unpack = True):
        return self._req(self.client.patch, url, expected_code, data, headers, unpack)

    def _put(self, url, expected_code, data = None, headers = default_headers, unpack = True):
        return self._req(self.client.put, url, expected_code, data, headers, unpack)

    def _post(self, url, expected_code, data = None, headers = default_headers, unpack = True):
        return self._req(self.client.post, url, expected_code, data, headers, unpack)

    def setUp_vlans(self):
        """Helper function for extending setUp()"""

        vlans = [
            { 'tag': 1, 'description': 'VLAN_ONE' },
            { 'tag': 2, 'description': 'VLAN_TWO' },
        ]
        for vlan in vlans:
            self._post('/vlans', 201, json.dumps(vlan), self.default_headers, unpack = False)

    def setUp_connectors(self):
        """Helper function for extending setUp()"""

        connectors = [
            { 'name': 'rj11' },
            { 'name': 'rj45' },
        ]
        for connector in connectors:
            self._post('/connectors', 201, json.dumps(connector), self.default_headers, unpack = False)

    def setUp_network_protocols(self):
        """Helper function for extending setUp()"""

        protocols = [
            { 'name': 'proto1', 'speed': 100 },
            { 'name': 'proto2', 'speed': 200 },
        ]
        for protocol in protocols:
            self._post('/network_protocols', 201, json.dumps(protocol), self.default_headers, unpack = False)

    def setUp_switch_models(self):
        """Helper function for extending setUp()"""

        models = [
            {
                'name':  'big_switch',
                'size':  4,
                'ports': [
                    {
                        'name': 'p1',
                        'network_protocols': [ 'proto1', 'proto2' ],
                        'connector': 'rj45'
                    },
                    {
                        'name': 'p2',
                        'network_protocols': [ 'proto1' ],
                        'connector': 'rj45'
                    },
                    {
                        'name': 'p3',
                        'network_protocols': [ 'proto2' ],
                        'connector': 'rj45'
                    },
                    {
                        'name': 'p4',
                        'network_protocols': [ ],
                        'connector': 'rj45'
                    },
                ],
            },
            {
                'name':  'small_switch',
                'size':  1,
                'ports': [
                    {
                        'name': 'p1',
                        'network_protocols': [ 'proto1', 'proto2' ],
                        'connector': 'rj11'
                    },
                ],
            }
        ]

        for model in models:
            self._post('/switch_models', 201, json.dumps(model), self.default_headers, unpack = False)

    def setUp_switches(self):
        """Helper function for extending setUp()"""

        switches = [
            {
                'name':     'switch1',
                'model':    'small_switch',
                'ports':    [
                    {
                        'name':   'p1',
                        'target': 'Saturn',
                        'vlans':  [ 1 ],
                    },
                ],
                'location': 12,
                'ip':       '192.168.0.50',
            },
            {
                'name':     'switch2',
                'model':    'big_switch',
                'ports':    [
                    {
                        'name':   'p1',
                        'target': 'Mars',
                        'vlans':  [ 1, 2 ],
                    },
                    {
                        'name':   'p3',
                        'target': 'Jupiter',
                        'vlans':  [ ],
                    },
                    {
                        'name':   'p4',
                        'target': 'Mercury',
                        'vlans':  [ 2 ],
                    },
                ],
                'location': 5,
                'ip':       '192.168.0.100',
            },
        ]

        for switch in switches:
            self._post('/switches', 201, json.dumps(switch), self.default_headers, unpack = False)
