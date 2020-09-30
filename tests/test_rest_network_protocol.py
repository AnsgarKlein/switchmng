import json

import unittest

from test_rest import Test_REST

class Test_REST_NetworkProtocol(Test_REST):
    """Test class that access network protocol resource as a rest client"""

    example_protocol = {
        'name': 'example_protocol',
        'speed': 150
    }

    def setUp(self):
        super().setUp()

        # Add some default values
        self.setUp_vlans()
        self.setUp_connectors()
        self.setUp_network_protocols()
        self.setUp_switch_models()

        # Add a network protocol
        rv = self._post('/network_protocols', 201, json.dumps(self.example_protocol))
        self.example_protocol = rv['data']

    def test_options1(self):
        """OPTIONS verb for network protocols"""

        rv = self._options('/network_protocols', 200)

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
        """OPTIONS verb for specific network protocol"""

        rv = self._options('/network_protocols/example_protocol', 200)

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
        """HEAD verb for non existing network protocol"""

        self._head('/network_protocols/non_existing_protocol', 404)

    def test_head1(self):
        """HEAD verb for network protocol"""

        # Query
        rv = self._head('/network_protocols/example_protocol', 200)

        # Check
        self.assertEqual(rv.data.decode(), '')

    def test_get_fail(self):
        """GET non existing network protocol"""

        self._get('/network_protocols/non_existing_protocol', 404)

    def test_get(self):
        """GET network protocols"""

        # Query
        rv = self._get('/network_protocols', 200)

        # Check
        ret = rv['data']
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 3)

        self.assertTrue(self.example_protocol in ret)

    def test_delete_fail_inuse(self):
        """DELETE network protocol still in use by port model"""

        # Add network protocol to port model on switch model
        patch = {
            'network_protocols': [ 'example_protocol' ]
        }
        self._patch('/switch_models/small_switch/ports/p1', 200, json.dumps(patch))

        # DELETE
        self._delete('/network_protocols/example_protocol', 400)

        # Remove vlan from port on switch
        patch = {
            'network_protocols': []
        }
        self._patch('/switch_models/small_switch/ports/p1', 200, json.dumps(patch))

        # DELETE
        self._delete('/network_protocols/example_protocol', 200)

    def test_delete_fail_nonexisting(self):
        """DELETE non existing network protocol"""

        self._delete('/network_protocols/non_existing_protocol', 404)

    def test_delete_fail_header(self):
        """DELETE network protocol with missing 'Accept' header"""

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._delete('/network_protocols/example_protocol', 406, None, headers)

    def test_delete(self):
        """DELETE network protocol and check that it is gone"""

        # Query before delete
        self._get('/network_protocols/example_protocol', 200)

        # Delete
        self._delete('/network_protocols/example_protocol', 200)

        # Query after delete
        self._get('/network_protocols/example_protocol', 404)

    def test_patch_fail_nonexisting(self):
        """PATCH non existing network protocol"""

        patch = {}
        self._patch('/network_protocols/non_existing_protocol', 404, json.dumps(patch))

    def test_patch_fail_header1(self):
        """PATCH network protocol with missing 'Accept' header"""

        patch = {}
        headers = self.patch_headers.copy()
        headers.pop('Accept')
        self._patch('/network_protocols/example_protocol', 406, json.dumps(patch), headers)

    def test_patch_fail_header2(self):
        """PATCH network protocol with missing 'Content-Type' header"""

        patch = {}
        headers = self.patch_headers.copy()
        headers.pop('Content-Type')
        self._patch('/network_protocols/example_protocol', 415, json.dumps(patch), headers)

    def test_patch_fail_request1(self):
        """PATCH network protocol with malformed request data"""

        patch = '{ "name": string without quotes }'
        self._patch('/network_protocols/example_protocol', 400, patch)

    def test_patch_fail_request2(self):
        """PATCH network protocol with malformed request data"""

        patch = { 'not a valid field': 'foobar' }
        self._patch('/network_protocols/example_protocol', 400, json.dumps(patch))

    def test_patch1(self):
        """
        PATCH network protocol with same resource identifier.

        Check that PATCHING network protocol does not change attributes
        that are not given in request.
        """

        patch = {
            'speed': 9001
        }

        # Patch
        rv1 = self._patch('/network_protocols/example_protocol', 200, json.dumps(patch))
        rv2 = self._get('/network_protocols/example_protocol', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key in self.example_protocol.keys():
            if key in patch:
                self.assertEqual(ret1[key], patch[key])
            else:
                self.assertEqual(ret1[key], self.example_protocol[key])

    def test_patch2(self):
        """
        PATCH network protocol to different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        patch = {
            'name': 'patched_protocol',
        }

        # Patch
        rv1 = self._patch('/network_protocols/example_protocol', 200, json.dumps(patch))

        # Query (1)
        self._get('/network_protocols/example_protocol', 404)

        # Query (2)
        rv2 = self._get('/network_protocols/patched_protocol', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_fail_header1(self):
        """PUT network protocol with missing 'Accept' header"""

        replacement = {
            'name': 'replacement_protocol'
        }

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._put('/network_protocols/example_protocol', 406, json.dumps(replacement), headers)

    def test_put_fail_header2(self):
        """PUT network protocol with missing 'Content-Type' header"""

        replacement = {
            'name': 'replacement_protocol'
        }

        headers = self.default_headers.copy()
        headers.pop('Content-Type')
        self._put('/network_protocols/example_protocol', 415, json.dumps(replacement), headers)

    def test_put_fail_request1(self):
        """PUT network protocol with malformed request data"""

        replacement = '{ "name": "not closed str }'
        self._put('/network_protocols/example_protocol', 400, json.dumps(replacement))

    def test_put_fail_request2(self):
        """PUT network protocol with invalid request data"""

        replacement = { 'name': 'replacement_protocol', 'not a valid field': 'foobar' }
        self._put('/network_protocols/example_protocol', 400, json.dumps(replacement))

    def test_put1(self):
        """
        PUT network protocol with same resource identifier.

        Check that PUTTING resource changes all attributes to default if
        attributes are not given in request.
        """

        replacement = {
            'name': 'example_protocol'
        }

        # Put
        rv1 = self._put('/network_protocols/example_protocol', 200, json.dumps(replacement))

        # Query
        rv2 = self._get('/network_protocols/example_protocol', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        # Check that all changes from request have been made
        for key in replacement.keys():
            self.assertEqual(replacement[key], ret1[key])

        # Check that previously set attributes that were not
        # present in request are now unset.
        self.assertEqual(ret1['speed'], None)

    def test_put2(self):
        """
        PUT network protocol with different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        replacement = {
            'name': 'replacement_protocol'
        }

        # Put
        rv1 = self._put('/network_protocols/example_protocol', 200, json.dumps(replacement))

        # Query (1)
        self._get('/network_protocols/example_protocol', 404)

        # Query (2)
        rv2 = self._get('/network_protocols/replacement_protocol', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_new(self):
        """PUT new network protocol"""

        new_protocol = {
            'name': 'new_protocol',
            'speed': 9001,
        }

        # Put
        rv1 = self._put('/network_protocols/new_protocol', 200, json.dumps(new_protocol))

        # Query
        rv2 = self._get('/network_protocols/new_protocol', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key in new_protocol.keys():
            self.assertEqual(new_protocol[key], ret1[key])

    def test_post_fail_header1(self):
        """POST network protocol with missing 'Accept' header"""

        new_protocol = {
            'name': 'new_protocol',
            'speed': 9001
        }

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._post('/network_protocols', 406, json.dumps(new_protocol), headers)

    def test_post_fail_header2(self):
        """POST network protocol with missing 'Content-Type' header"""

        new_protocol = {
            'name': 'new_protocol',
            'speed': 9001
        }

        headers = self.default_headers.copy()
        headers.pop('Content-Type')
        self._post('/network_protocols', 415, json.dumps(new_protocol), headers)

    def test_post_fail_request1(self):
        """POST network protocol with malformed request data"""

        new_protocol = '{ "name": "not closed str }'
        self._post('/network_protocols', 400, new_protocol)

    def test_post_fail_request2(self):
        """POST vlan with invalid request data"""

        new_protocol = { 'name': 'new_protocol', 'not a valid field': 'foobar' }
        self._post('/network_protocols', 400, json.dumps(new_protocol))

    def test_post_minimum(self):
        """POST network protocol with minimum configuration"""

        minimum = {
            'name': 'new_protocol'
        }

        # Add
        rv1 = self._post('/network_protocols', 201, json.dumps(minimum))

        # Query
        rv2 = self._get('/network_protocols/new_protocol', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key in minimum.keys():
            self.assertEqual(minimum[key], ret1[key])

    def test_post_maximum(self):
        """POST network protocol with maximum configuration"""

        maximum = {
            'name': 'new_protocol',
            'speed': 9001
        }

        # Add
        rv1 = self._post('/network_protocols', 201, json.dumps(maximum))

        # Query
        rv2 = self._get('/network_protocols/new_protocol', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)
        self.assertEqual(maximum, ret1)

if __name__ == '__main__':
    unittest.main(buffer = True)
