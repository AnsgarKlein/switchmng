import json

import unittest

from test_rest import Test_REST

class Test_REST_Switch(Test_REST):
    """Test class that access switch resource as a rest client"""

    example_switch = {
        'name':     'example_switch',
        'model':    'small_switch',
        'ports':    [],
        'location': 5,
        'ip':       '192.168.0.1',
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
        """OPTIONS verb for switches"""

        rv = self._options('/switches', 200)

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
        """OPTIONS verb for specific switch"""

        rv = self._options('/switches/example_switch', 200)

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

        # Query
        rv = self._head('/switches/example_switch', 200)

        # Check
        self.assertEqual(rv.data.decode(), '')

    def test_get_fail(self):
        """GET non existing switch"""

        self._get('/switches/non-existing', 404)

    def test_get(self):
        """GET switches"""

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

        headers = self.default_headers.copy()
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
        headers = self.patch_headers.copy()
        headers.pop('Accept')
        self._patch('/switches/example_switch', 406, json.dumps(patch), headers)

    def test_patch_fail_header2(self):
        """PATCH switch with missing 'Content-Type' header"""

        patch = {}
        headers = self.patch_headers.copy()
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

        for key in patch.keys():
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

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._put('/switches/example_switch', 406, json.dumps(replacement), headers)

    def test_put_fail_header2(self):
        """PUT switch with missing 'Content-Type' header"""

        replacement = {
            'location': 9,
            'ip': '10.0.0.1',
        }

        headers = self.default_headers.copy()
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
            'name':  'example_switch',
            'model': 'big_switch',
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
        for key in replacement.keys():
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
            'name':  'replacement_switch',
            'model': 'small_switch',
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
        """PUT new switch"""

        new_switch = {
            'name':  'new_switch',
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

        for key in new_switch.keys():
            self.assertEqual(new_switch[key], ret1[key])

    def test_post_fail_header1(self):
        """POST switch with missing 'Accept' header"""

        new_switch = {
            'name':  'new_switch',
            'model': 'small_switch',
        }

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._post('/switches', 406, json.dumps(new_switch), headers)

    def test_post_fail_header2(self):
        """POST switch with missing 'Content-Type' header"""

        new_switch = {
            'name':  'new_switch',
            'model': 'small_switch',
        }

        headers = self.default_headers.copy()
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

    def test_post_fail_request3(self):
        """POST switch with invalid name"""

        new_switch = {
            'name': '',
            'model': 'small_switch'
        }

        # Add
        self._post('/switches', 400, json.dumps(new_switch))

    def test_post_fail_request4(self):
        """POST switch with missing model"""

        new_switch = {
            'name': 'new_switch'
        }

        # Add
        self._post('/switches', 400, json.dumps(new_switch))

    def test_post_minimum(self):
        """POST switch with minimum configuration"""

        minimum = {
            'name':  'new_switch',
            'model': 'small_switch',
        }

        # Add
        rv1 = self._post('/switches', 201, json.dumps(minimum))

        # Query
        rv2 = self._get('/switches/new_switch', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key in minimum.keys():
            self.assertEqual(minimum[key], ret1[key])

    def test_post_maximum(self):
        """POST switch with maximum configuration"""

        maximum = {
            'name':  'new_switch',
            'model': 'small_switch',
            'ports': [
                {
                    'name':   'p1',
                    'target': 'foo',
                    'vlans':  [ 1, 2 ],
                }],
            'location': 2,
            'ip': '10.0.0.1',
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
