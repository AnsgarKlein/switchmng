import switchmng
from switchmng import database
from switchmng.schema import *

from switchmng import config
from switchmng.schema.base import Base
from switchmng.database import DatabaseConnection
from switchmng import routes

import helper
from helper import default_headers
from helper import patch_headers

import unittest
from unittest import TestCase

import json

class Test_REST_Vlan(TestCase):

    example_vlan = {
        'tag': 42,
        'description': 'example vlan',
    }

    def setUp(self):
        switchmng.config.parse_arguments([])
        db = DatabaseConnection('sqlite', '', False, Base)
        self.session = db.Session()
        self.app = routes.create_app(db)
        self.client = self.app.test_client()

        # Add a vlan
        rv = self._post('/vlans', 201, json.dumps(self.example_vlan))
        self.example_vlan = rv['data']

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

    def test_options1(self):
        """OPTIONS verb for vlans"""

        rv = self._options('/vlans', 200)

        # Check that 'Content-Length' header is set to 0
        self.assertTrue('Content-Length' in rv.headers)
        self.assertEqual(rv.headers['Content-Length'], '0')

        # Check that body really is empty
        self.assertEqual(rv.data.decode(), '')

        # Check that allowed verbs are exactly as expected
        self.assertTrue('Allow' in rv.headers)
        allowed = rv.headers['Allow']
        allowed = [ i.strip() for i in allowed.split(',') ]
        allowed = set(allowed)

        expected = {
            'OPTIONS',
            'HEAD',
            'GET',
            'POST',
        }

        self.assertEqual(allowed, expected)

    def test_options2(self):
        """OPTIONS verb for specific vlan"""

        rv = self._options('/vlans/42', 200)

        # Check that 'Content-Length' header is set to 0
        self.assertTrue('Content-Length' in rv.headers)
        self.assertEqual(rv.headers['Content-Length'], '0')

        # Check that body really is empty
        self.assertEqual(rv.data.decode(), '')

        # Check that allowed verbs are exactly as expected
        self.assertTrue('Allow' in rv.headers)
        allowed = rv.headers['Allow']
        allowed = [ i.strip() for i in allowed.split(',') ]
        allowed = set(allowed)

        expected = {
            'OPTIONS',
            'HEAD',
            'GET',
            'PUT',
            'PATCH',
            'DELETE',
        }

        self.assertEqual(allowed, expected)

    def test_head_fail_nonexisting(self):
        """HEAD verb for non existing vlan"""

        self._head('/vlans/43', 404)

    def test_head1(self):
        """HEAD verb for vlan"""

        self._head('/vlans/42', 200)

    def test_get_fail(self):
        # Query non existing vlan
        self._get('/vlans/43', 404)

    def test_get(self):
        # Query
        rv = self._get('/vlans', 200)

        # Check
        ret = rv['data']
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 1)

        ret = rv['data'][0]
        self.assertTrue(isinstance(ret, dict))

        self.assertEqual(ret, self.example_vlan)

    def test_delete_fail_inuse(self):
        """DELETE vlan still in use by port"""

        # Add some values
        helper.setUp_vlans(self.client)
        helper.setUp_connectors(self.client)
        helper.setUp_network_protocols(self.client)
        helper.setUp_switch_models(self.client)
        helper.setUp_switches(self.client)

        # Add vlan to port on switch
        patch = {
            'vlans': [ 42 ]
        }
        rv = self._patch('/switches/switch1/ports/p1', 200, json.dumps(patch))

        # DELETE
        rv = self._delete('/vlans/42', 400)

        # Remove vlan from port on switch
        patch = {
            'vlans': []
        }
        rv = self._patch('/switches/switch1/ports/p1', 200, json.dumps(patch))

        # DELETE
        rv = self._delete('/vlans/42', 200)

    def test_delete_fail_nonexisting(self):
        """DELETE non existing vlan"""

        self._delete('/vlans/43', 404)

    def test_delete_fail_header(self):
        """DELETE vlan with missing 'Accept' header"""

        headers = default_headers.copy()
        headers.pop('Accept')
        self._delete('/vlans/42', 406, None, headers)

    def test_delete(self):
        """DELETE vlan and check that it is gone"""

        # Query before delete
        self._get('/vlans/42', 200)

        # Delete
        self._delete('/vlans/42', 200)

        # Query after delete
        self._get('/vlans/42', 404)

    def test_patch_fail_nonexisting(self):
        """PATCH non existing vlan"""

        patch = {}
        self._patch('/vlans/43', 404, json.dumps(patch))

    def test_patch_fail_header1(self):
        """PATCH vlan with missing 'Accept' header"""

        patch = {}
        headers = patch_headers.copy()
        headers.pop('Accept')
        self._patch('/vlans/42', 406, json.dumps(patch), headers)

    def test_patch_fail_header2(self):
        """PATCH vlan with missing 'Content-Type' header"""

        patch = {}
        headers = patch_headers.copy()
        headers.pop('Content-Type')
        self._patch('/vlans/42', 415, json.dumps(patch), headers)

    def test_patch_fail_request1(self):
        """PATCH vlan with malformed request data"""

        patch = '{ "description": string without quotes }'
        self._patch('/vlans/42', 400, patch)

    def test_patch_fail_request2(self):
        """PATCH vlan with malformed request data"""

        patch = { 'not a valid field': 'foobar' }
        self._patch('/vlans/42', 400, json.dumps(patch))

    def test_patch1(self):
        """
        PATCH vlan with same resource identifier.

        Check that PATCHING vlan does not change attributes
        that are not given in request.
        """

        patch = {
            'description': 'patched description'
        }

        # Patch
        rv1 = self._patch('/vlans/42', 200, json.dumps(patch))
        rv2 = self._get('/vlans/42', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in self.example_vlan.items():
            if key in patch:
                pass
            else:
                self.assertEqual(self.example_vlan[key], ret1[key])

        for key, val in patch.items():
            self.assertEqual(patch[key], ret1[key])

    def test_patch2(self):
        """
        PATCH vlan to different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        patch = {
            'tag': 43,
        }

        # Patch
        rv1 = self._patch('/vlans/42', 200, json.dumps(patch))

        # Query (1)
        self._get('/vlans/42', 404)

        # Query (2)
        rv2 = self._get('/vlans/43', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_fail_header1(self):
        """PUT vlan with missing 'Accept' header"""

        replacement = {
            'tag': 42,
            'description': 'replacement_vlan',
        }

        headers = default_headers.copy()
        headers.pop('Accept')
        self._put('/vlans/42', 406, json.dumps(replacement), headers)

    def test_put_fail_header2(self):
        """PUT vlan with missing 'Content-Type' header"""

        replacement = {
            'tag': 42,
            'description': 'replacement_vlan',
        }

        headers = default_headers.copy()
        headers.pop('Content-Type')
        self._put('/vlans/42', 415, json.dumps(replacement), headers)

    def test_put_fail_request1(self):
        """PUT vlan with malformed request data"""

        replacement = '{ "description": "not closed str }'
        self._put('/vlans/42', 400, json.dumps(replacement))

    def test_put_fail_request2(self):
        """PUT vlan with invalid request data"""

        replacement = { 'not a valid field': 'foobar' }
        self._put('/vlans/42', 400, json.dumps(replacement))

    def test_put1(self):
        """
        PUT vlan with same resource identifier.

        Check that PUTTING resource changes all attributes to default if
        attributes are not given in request.
        """

        replacement = {
            'tag': 42,
        }

        # Put
        rv1 = self._put('/vlans/42', 200, json.dumps(replacement))

        # Query
        rv2 = self._get('/vlans/42', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        # Check that all changes from request have been made
        for key, val in replacement.items():
            self.assertEqual(replacement[key], ret1[key])

        # Check that previously set attributes that were not
        # present in request are now unset.
        self.assertEqual(ret1['description'], None)

    def test_put2(self):
        """
        PUT vlan with different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        replacement = {
            'tag': 43,
            'description': 'replacement vlan',
        }

        # Put
        rv1 = self._put('/vlans/42', 200, json.dumps(replacement))

        # Query (1)
        self._get('/vlans/42', 404)

        # Query (2)
        rv2 = self._get('/vlans/43', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_new(self):
        new_vlan = {
            'tag': 43,
            'description': 'newly added vlan',
        }

        # Put
        rv1 = self._put('/vlans/43', 200, json.dumps(new_vlan))

        # Query
        rv2 = self._get('/vlans/43', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in new_vlan.items():
            self.assertEqual(new_vlan[key], ret1[key])

    def test_post_fail_header1(self):
        """POST vlan with missing 'Accept' header"""

        new_vlan = {
            'tag': 43,
            'description': 'newly added vlan',
        }

        headers = default_headers.copy()
        headers.pop('Accept')
        self._post('/vlans', 406, json.dumps(new_vlan), headers)

    def test_post_fail_header2(self):
        """POST vlan with missing 'Content-Type' header"""

        new_vlan = {
            'tag': 43,
            'description': 'newly added vlan',
        }

        headers = default_headers.copy()
        headers.pop('Content-Type')
        self._post('/vlans', 415, json.dumps(new_vlan), headers)

    def test_post_fail_request1(self):
        """POST vlan with malformed request data"""

        new_vlan = '{ "tag": 43, "description": "not closed str }'
        self._post('/vlans', 400, new_vlan)

    def test_post_fail_request2(self):
        """POST vlan with invalid request data"""

        new_vlan = { "tag": 43, 'not a valid field': 'foobar' }
        self._post('/vlans', 400, json.dumps(new_vlan))

    def test_post_minimum(self):
        minimum = {
            'tag': 43,
        }

        # Add
        rv1 = self._post('/vlans', 201, json.dumps(minimum))

        # Query
        rv2 = self._get('/vlans/43', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in minimum.items():
            self.assertEqual(minimum[key], ret1[key])

    def test_post_maximum(self):
        maximum = {
            'tag': 43,
            'description':  'newly added vlan',
        }

        # Add
        rv1 = self._post('/vlans', 201, json.dumps(maximum))

        # Query
        rv2 = self._get('/vlans/43', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)
        self.assertEqual(maximum, ret1)

if __name__ == '__main__':
    unittest.main(buffer = True)