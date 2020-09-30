import json

import unittest

from test_rest import Test_REST

class Test_REST_Port(Test_REST):
    """Test class that access port resource as a rest client"""

    example_switch = {
        'name':     'switch1',
        'model':    'big_switch',
        'ports':    [
            {
                'name':   'p1',
                'target': 'Mars',
                'vlans':  [ 1, 2 ],
            },
            {
                'name':   'p2',
                'target': None,
                'vlans':  []
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
    }

    def setUp(self):
        super().setUp()

        # Add some default values
        self.setUp_vlans()
        self.setUp_connectors()
        self.setUp_network_protocols()
        self.setUp_switch_models()

        # Add a switch
        rv = self._post('/switches', 201, json.dumps(self.example_switch))
        self.example_switch = rv['data']

    def test_options1(self):
        """OPTIONS verb for ports"""

        rv = self._options('/switches/switch1/ports', 200)

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
        }

        self.assertEqual(allowed, expected)

    def test_options2(self):
        """OPTIONS verb for specific port"""

        rv = self._options('/switches/switch1/ports/p1', 200)

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
        }

        self.assertEqual(allowed, expected)

    def test_head_fail_nonexisting(self):
        """HEAD verb for non existing port"""

        self._head('/switches/switch1/ports/9001', 404)

    def test_head1(self):
        """HEAD verb for port"""

        # Query
        rv = self._head('/switches/switch1/ports/p1', 200)

        # Check
        self.assertEqual(rv.data.decode(), '')

    def test_get_fail(self):
        """GET verb for non existing port"""

        # Query non existing port
        self._get('/switches/switch1/ports/non-existing', 404)

    def test_get(self):
        """GET verb for switch ports"""

        # Query
        rv = self._get('/switches/switch1/ports', 200)

        # Check
        ret = rv['data']
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 4)

        comparison = self.example_switch.copy()['ports']
        comparison.sort(key = lambda p: p['name'])
        ret.sort(key = lambda p: p['name'])

        self.assertEqual(ret, comparison)

    def test_delete_fail(self):
        """
        DELETE port

        This should not be possible and return an error.
        """

        self._delete('/switches/switch1/ports/p1', 405, unpack = False)

    def test_patch_fail_nonexisting(self):
        """PATCH non existing port"""

        patch = {}
        self._patch('/switches/switch1/ports/non-existing', 404, json.dumps(patch))

    def test_patch_fail_header1(self):
        """PATCH port with missing 'Accept' header"""

        patch = {}
        headers = self.patch_headers.copy()
        headers.pop('Accept')
        self._patch('/switches/switch1/ports/p1', 406, json.dumps(patch), headers)

    def test_patch_fail_header2(self):
        """PATCH port with missing 'Content-Type' header"""

        patch = {}
        headers = self.patch_headers.copy()
        headers.pop('Content-Type')
        self._patch('/switches/switch1/ports/p1', 415, json.dumps(patch), headers)

    def test_patch_fail_request1(self):
        """PATCH port with malformed request data"""

        patch = '{ "description": string without quotes }'
        self._patch('/switches/switch1/ports/p1', 400, patch)

    def test_patch_fail_request2(self):
        """PATCH port with malformed request data"""

        patch = { 'not a valid field': 'foobar' }
        self._patch('/switches/switch1/ports/p1', 400, json.dumps(patch))

    def test_patch1(self):
        """
        PATCH port.

        Check that PATCHING port does not change attributes
        that are not given in request.
        """

        patch = {
            'target': 'Alpha Centauri'
        }

        # Get
        comparison = self._get('/switches/switch1/ports/p3', 200)
        comparison = comparison['data']

        comparison_sw = self._get('/switches/switch1', 200)
        comparison_sw = comparison_sw['data']

        # Patch
        rv1 = self._patch('/switches/switch1/ports/p3', 200, json.dumps(patch))
        rv2 = self._get('/switches/switch1/ports/p3', 200)

        # Check that only attribute in patch changed
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key in comparison.keys():
            if key in patch:
                self.assertEqual(ret1[key], patch[key])
            else:
                self.assertEqual(ret1[key], comparison[key])

        # Check that switch did not change
        ret_sw = self._get('/switches/switch1', 200)
        ret_sw = ret_sw['data']

        for key in comparison_sw.keys():
            if key == 'ports':
                pass
            else:
                self.assertEqual(ret_sw[key], comparison_sw[key])

    def test_patch2(self):
        """
        PATCH port with different resource identifier.

        This should not be possible and return an error.
        """

        patch = {
            'name': 'patched-port'
        }

        # Query
        comparison = self._get('/switches/switch1/ports/p3', 200)

        # Patch
        self._patch('/switches/switch1/ports/p3', 400, json.dumps(patch))

        # Query (1)
        self._get('/switches/switch1/ports/patched-port', 404)

        # Query (2)
        rv = self._get('/switches/switch1/ports/p3', 200)

        # Check
        self.assertEqual(comparison['data'], rv['data'])

    def test_put_fail_header1(self):
        """PUT port with missing 'Accept' header"""

        replacement = {
            'name': 'p3',
        }

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._put('/switches/switch1/ports/p3', 406, json.dumps(replacement), headers)

    def test_put_fail_header2(self):
        """PUT port with missing 'Content-Type' header"""

        replacement = {
            'name': 'p3',
        }

        headers = self.default_headers.copy()
        headers.pop('Content-Type')
        self._put('/switches/switch1/ports/p3', 415, json.dumps(replacement), headers)

    def test_put_fail_request1(self):
        """PUT port with malformed request data"""

        replacement = '{ "name": "not closed str }'
        self._put('/switches/switch1/ports/p3', 400, json.dumps(replacement))

    def test_put_fail_request2(self):
        """PUT port with invalid request data"""

        replacement = { 'not a valid field': 'foobar' }
        self._put('/switches/switch1/ports/p3', 400, json.dumps(replacement))

    def test_put1(self):
        """
        PUT port with same resource identifier.

        Check that PUTTING resource changes all attributes to default if
        attributes are not given in request.
        """

        replacement = {
            'name': 'p3',
        }

        # Put
        rv1 = self._put('/switches/switch1/ports/p3', 200, json.dumps(replacement))

        # Query
        rv2 = self._get('/switches/switch1/ports/p3', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        # Check that all changes from request have been made
        for key in replacement.keys():
            self.assertEqual(replacement[key], ret1[key])

        # Check that previously set attributes that were not
        # present in request are now unset.
        self.assertEqual(ret1['target'], None)
        self.assertEqual(ret1['vlans'], [])

    def test_put2(self):
        """
        PUT port with different resource identifier.

        This should not be possible and return an error.
        """

        replacement = {
            'name': 'patched_port',
        }

        # Query
        comparison = self._get('/switches/switch1/ports/p3', 200)

        # Put
        self._put('/switches/switch1/ports/p3', 400, json.dumps(replacement))

        # Query (1)
        self._get('/switches/switch1/ports/patched_port', 404)

        # Query (2)
        rv = self._get('/switches/switch1/ports/p3', 200)

        # Check
        self.assertEqual(comparison['data'], rv['data'])

    def test_put_new(self):
        """
        PUT new port.

        This should not be possible and return an error.
        """

        new_port = {
            'name': 'new_port',
        }

        # Put
        self._put('/switches/switch1/ports/new_port', 400, json.dumps(new_port))

        # Query
        self._get('/switches/switch1/ports/new_port', 404)

    def test_post_fail1(self):
        """
        POST port

        This should not be possible and return an error"""

        new_port = {
            'name': 'new_port',
        }

        self._post('/switches/switch1/ports/', 405, json.dumps(new_port), unpack = False)

if __name__ == '__main__':
    unittest.main(buffer = True)
