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

    example_switch = {
        'name':     'example_switch',
        'model':    'small_switch',
        'ports':    [],
        'location': 5,
        'ip':       '192.168.0.1',
    }

    def setUp(self):
        switchmng.config.parse_arguments([])
        db = DatabaseConnection('sqlite', '', False, Base)
        self.session = db.Session()
        self.app = routes.create_app(db)
        self.client = self.app.test_client()

        # Add some default values
        helper.setUp_vlans(self.client)
        helper.setUp_connectors(self.client)
        helper.setUp_network_protocols(self.client)
        helper.setUp_switch_models(self.client)

        # Add a switch
        rv = self._post('/switches', 201, json.dumps(self.example_switch))
        self.example_switch = rv['data']

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
        """HEAD verb for non existing switch"""

        self._head('/switches/non-existing', 404)

    def test_head1(self):
        """HEAD verb for switch"""

        self._head('/switches/example_switch', 200)

    def test_get_fail(self):
        # Query non existing switch
        self._get('/switches/non-existing', 404)

    def test_get(self):
        # Query
        rv = self._get('/switches', 200)

        # Check
        ret = rv['data']
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 1)

        ret = rv['data'][0]
        self.assertTrue(isinstance(ret, dict))

        self.assertEqual(ret, self.example_switch)

    def test_delete_fail_nonexisting(self):
        """DELETE non existing switch"""

        self._delete('/switches/non-existing', 404)

    def test_delete_fail_header(self):
        """DELETE switch with missing 'Accept' header"""

        headers = default_headers.copy()
        headers.pop('Accept')
        self._delete('/switches/example_switch', 406, None, headers)

    def test_delete(self):
        """DELETE switch and check that it is gone"""

        # Query before delete
        self._get('/switches/example_switch', 200)

        # Delete
        self._delete('/switches/example_switch', 200)

        # Query after delete
        self._get('/switches/example_switch', 404)

    def test_patch_fail(self):
        """PATCH non existing switch"""

        patch = {}
        self._patch('/switches/non-existing', 404, json.dumps(patch))

    def test_patch_fail_header1(self):
        """PATCH switch with missing 'Accept' header"""

        patch = {}
        headers = patch_headers.copy()
        headers.pop('Accept')
        self._patch('/switches/example_switch', 406, json.dumps(patch), headers)

    def test_patch_fail_header1(self):
        """PATCH switch with missing 'Content-Type' header"""

        patch = {}
        headers = patch_headers.copy()
        headers.pop('Content-Type')
        self._patch('/switches/example_switch', 415, json.dumps(patch), headers)

    def test_patch_fail_request1(self):
        """PATCH switch with malformed request data"""

        patch = '{ "description": string without quotes }'
        self._patch('/switches/example_switch', 400, patch)

    def test_patch_fail_request2(self):
        """PATCH switch with invalid request data"""

        patch = { 'not a valid field': 'foobar' }
        self._patch('/switches/example_switch', 400, json.dumps(patch))

    def test_patch1(self):
        """
        PATCH switch with same resource identifier.

        Check that PATCHING switch does not change attributes
        that are not given in request.
        """

        patch = {
            'model': 'big_switch'
        }

        # Patch
        rv1 = self._patch('/switches/example_switch', 200, json.dumps(patch))
        rv2 = self._get('/switches/example_switch', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in patch.items():
            self.assertEqual(patch[key], ret1[key])

    def test_patch2(self):
        """
        PATCH switch to different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        patch = {
            'name': 'patched_switch',
        }

        # Patch
        rv1 = self._patch('/switches/example_switch', 200, json.dumps(patch))

        # Query (1)
        self._get('/switches/example_switch', 404)

        # Query (2)
        rv2 = self._get('/switches/patched_switch', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_fail_header1(self):
        """PUT switch with missing 'Accept' header"""

        replacement = {
            'location': 9,
            'ip': '10.0.0.1',
        }

        headers = default_headers.copy()
        headers.pop('Accept')
        self._put('/switches/example_switch', 406, json.dumps(replacement), headers)

    def test_put_fail_header2(self):
        """PUT switch with missing 'Content-Type' header"""

        replacement = {
            'location': 9,
            'ip': '10.0.0.1',
        }

        headers = default_headers.copy()
        headers.pop('Content-Type')
        self._put('/switches/example_switch', 415, json.dumps(replacement), headers)

    def test_put_fail_request1(self):
        """PUT switch with malformed request data"""

        replacement = {
            'location': 9,
            'ip': '10.0.0.1',
        }

        replacement = '{ "description": "not closed str }'
        self._put('/switches/example_switch', 400, json.dumps(replacement))

    def test_put_fail_request2(self):
        """PUT switch with invalid request data"""

        replacement = {
            'location': 9,
            'ip': '10.0.0.1',
        }

        replacement = { 'not a valid field': 'foobar' }
        self._put('/switches/example_switch', 400, json.dumps(replacement))

    def test_put1(self):
        """
        PUT switch with same resource identifier.

        Check that PUTTING resource changes all attributes to default if
        attributes are not given in request.
        """

        replacement = {
            'name':     'example_switch',
            'model':    'big_switch',
        }

        # Put
        rv1 = self._put('/switches/example_switch', 200, json.dumps(replacement))

        # Query
        rv2 = self._get('/switches/example_switch', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        # Check that all changes from request have been made
        for key, val in replacement.items():
            self.assertEqual(replacement[key], ret1[key])

        # Check that previously set attributes that were not
        # present in request are now unset.
        self.assertEqual(ret1['location'], None)
        self.assertEqual(ret1['ip'], None)

    def test_put2(self):
        """
        PUT switch with different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        replacement = {
            'name':     'replacement_switch',
            'model':    'small_switch',
        }

        # Put
        rv1 = self._put('/switches/example_switch', 200, json.dumps(replacement))

        # Query (1)
        self._get('/switches/example_switch', 404)

        # Query (2)
        rv2 = self._get('/switches/replacement_switch', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_new(self):
        new_switch = {
            'name': 'new_switch',
            'model': 'small_switch',
        }

        # Put
        rv1 = self._put('/switches/new_switch', 200, json.dumps(new_switch))

        # Query
        rv2 = self._get('/switches/new_switch', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in new_switch.items():
            self.assertEqual(new_switch[key], ret1[key])

    def test_post_fail_header1(self):
        """POST switch with missing 'Accept' header"""

        new_switch = {
            'name':     'new_switch',
            'model':    'small_switch',
        }

        headers = default_headers.copy()
        headers.pop('Accept')
        self._post('/switches', 406, json.dumps(new_switch), headers)

    def test_post_fail_header2(self):
        """POST switch with missing 'Content-Type' header"""

        new_switch = {
            'name':     'new_switch',
            'model':    'small_switch',
        }

        headers = default_headers.copy()
        headers.pop('Content-Type')
        self._post('/switches', 415, json.dumps(new_switch), headers)

    def test_post_fail_request1(self):
        """POST switch with malformed request data"""

        new_switch = '{ "name": "new_switch", "model": "small_switch", "ip": "not closed str }'
        self._post('/switches', 400, new_switch)

    def test_post_fail_request2(self):
        """POST switch with invalid request data"""

        new_switch = {
            'name':        'new_switch',
            'model':       'small_switch',
            'not_a_field': 'foobar',
        }

        self._post('/switches', 400, json.dumps(new_switch))

    def test_post_minimum(self):
        minimum = {
            'name':     'new_switch',
            'model':    'small_switch',
        }

        # Add
        rv1 = self._post('/switches', 201, json.dumps(minimum))

        # Query
        rv2 = self._get('/switches/new_switch', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in minimum.items():
            self.assertEqual(minimum[key], ret1[key])

    def test_post_maximum(self):
        maximum = {
            'name':     'new_switch',
            'model':    'small_switch',
            'ports':    [
                {
                    'name':   'p1',
                    'target': 'foo',
                    'vlans':  [ 1, 2 ],
                }],
            'location': 2,
            'ip':       '10.0.0.1',
        }

        # Add
        rv1 = self._post('/switches', 201, json.dumps(maximum))

        # Query
        rv2 = self._get('/switches/new_switch', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)
        self.assertEqual(maximum, ret1)

if __name__ == '__main__':
    unittest.main(buffer = True)
