import json

import unittest

from test_rest import Test_REST

class Test_REST_Connector(Test_REST):
    """Test class that access connector resource as a rest client"""

    example_connector = {
        'name': 'example_connector',
    }

    def setUp(self):
        super().setUp()

        # Add some default values
        self.setUp_vlans()
        self.setUp_connectors()
        self.setUp_network_protocols()
        self.setUp_switch_models()

        # Add a connector
        rv = self._post('/connectors', 201, json.dumps(self.example_connector))
        self.example_connector = rv['data']

    def test_options1(self):
        """OPTIONS verb for connectors"""

        rv = self._options('/connectors', 200)

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
        """OPTIONS verb for specific connector"""

        rv = self._options('/connectors/example_connector', 200)

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
        """HEAD verb for non existing connector"""

        self._head('/connectors/non_existing_connector', 404)

    def test_head1(self):
        """HEAD verb for connector"""

        # Query
        rv = self._head('/connectors/example_connector', 200)

        # Check
        self.assertEqual(rv.data.decode(), '')

    def test_get_fail(self):
        """GET non existing connector"""

        self._get('/connectors/non_existing_connector', 404)

    def test_get(self):
        """GET connectors"""

        # Query
        rv = self._get('/connectors', 200)

        # Check
        ret = rv['data']
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 3)

        self.assertTrue(self.example_connector in ret)

    def test_delete_fail_inuse(self):
        """DELETE connector still in use by port model"""

        # Add connector to port model on switch model
        patch = {
            'connector': 'example_connector'
        }
        self._patch('/switch_models/small_switch/ports/p1', 200, json.dumps(patch))

        # DELETE connector (should fail)
        self._delete('/connectors/example_connector', 400)

        # Remove connector from port on switch model
        patch = {
            'connector': None
        }
        self._patch('/switch_models/small_switch/ports/p1', 200, json.dumps(patch))

        # DELETE connector (should succeed)
        self._delete('/connectors/example_connector', 200)

    def test_delete_fail_nonexisting(self):
        """DELETE non existing connector"""

        self._delete('/connectors/non_existing_connector', 404)

    def test_delete_fail_header(self):
        """DELETE connector with missing 'Accept' header"""

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._delete('/connectors/example_connector', 406, None, headers)

    def test_delete(self):
        """DELETE connector and check that it is gone"""

        # Query before delete
        self._get('/connectors/example_connector', 200)

        # Delete
        self._delete('/connectors/example_connector', 200)

        # Query after delete
        self._get('/connectors/example_connector', 404)

    def test_patch_fail_nonexisting(self):
        """PATCH non existing connector"""

        patch = {}
        self._patch('/connectors/non_existing_connector', 404, json.dumps(patch))

    def test_patch_fail_header1(self):
        """PATCH connector with missing 'Accept' header"""

        patch = {}
        headers = self.patch_headers.copy()
        headers.pop('Accept')
        self._patch('/connectors/example_connector', 406, json.dumps(patch), headers)

    def test_patch_fail_header2(self):
        """PATCH connector with missing 'Content-Type' header"""

        patch = {}
        headers = self.patch_headers.copy()
        headers.pop('Content-Type')
        self._patch('/connectors/example_connector', 415, json.dumps(patch), headers)

    def test_patch_fail_request1(self):
        """PATCH connector with malformed request data"""

        patch = '{ "description": string without quotes }'
        self._patch('/connectors/example_connector', 400, patch)

    def test_patch_fail_request2(self):
        """PATCH connector with malformed request data"""

        patch = { 'not a valid field': 'foobar' }
        self._patch('/connectors/example_connector', 400, json.dumps(patch))

    def test_patch1(self):
        """
        PATCH connector with same resource identifier.

        Check that PATCHING connector does not change attributes
        that are not given in request.
        """

        # Not currently possible to test because connector only has
        # one attribute.

        pass

    def test_patch2(self):
        """
        PATCH connector to different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        patch = {
            'name': 'patched_connector',
        }

        # Patch
        rv1 = self._patch('/connectors/example_connector', 200, json.dumps(patch))

        # Query (1)
        self._get('/connectors/example_connector', 404)

        # Query (2)
        rv2 = self._get('/connectors/patched_connector', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_fail_header1(self):
        """PUT connector with missing 'Accept' header"""

        replacement = {
            'name': 'replacement_connector'
        }

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._put('/connectors/example_connector', 406, json.dumps(replacement), headers)

    def test_put_fail_header2(self):
        """PUT connector with missing 'Content-Type' header"""

        replacement = {
            'name': 'replacement_connector'
        }

        headers = self.default_headers.copy()
        headers.pop('Content-Type')
        self._put('/connectors/example_connector', 415, json.dumps(replacement), headers)

    def test_put_fail_request1(self):
        """PUT connector with malformed request data"""

        replacement = '{ "name": "not closed str }'
        self._put('/connectors/example_connector', 400, json.dumps(replacement))

    def test_put_fail_request2(self):
        """PUT connector with invalid request data"""

        replacement = { 'name': 'example_connector', 'not a valid field': 'foobar' }
        self._put('/connectors/example_connectors', 400, json.dumps(replacement))

    def test_put1(self):
        """
        PUT connector with same resource identifier.

        Check that PUTTING resource changes all attributes to default if
        attributes are not given in request.
        """

        # Not currently possible to test because connector only has
        # one attribute.

        pass

    def test_put2(self):
        """
        PUT connector with different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        replacement = {
            'name': 'replacement_connector'
        }

        # Put
        rv1 = self._put('/connectors/example_connector', 200, json.dumps(replacement))

        # Query (1)
        self._get('/connectors/example_connector', 404)

        # Query (2)
        rv2 = self._get('/connectors/replacement_connector', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_new(self):
        """PUT new connector"""

        new_connector = {
            'name': 'new_connector',
        }

        # Put
        rv1 = self._put('/connectors/new_connector', 200, json.dumps(new_connector))

        # Query
        rv2 = self._get('/connectors/new_connector', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key in new_connector.keys():
            self.assertEqual(new_connector[key], ret1[key])

    def test_post_fail_header1(self):
        """POST connector with missing 'Accept' header"""

        new_connector = {
            'name': 'new_connector'
        }

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._post('/connectors', 406, json.dumps(new_connector), headers)

    def test_post_fail_header2(self):
        """POST connector with missing 'Content-Type' header"""

        new_connector = {
            'name': 'new_connector'
        }

        headers = self.default_headers.copy()
        headers.pop('Content-Type')
        self._post('/connectors', 415, json.dumps(new_connector), headers)

    def test_post_fail_request1(self):
        """POST connector with malformed request data"""

        new_connector = '{ "name": "not closed str }'
        self._post('/connectors', 400, new_connector)

    def test_post_fail_request2(self):
        """POST connector with invalid request data"""

        new_connector = { "name": "new_connector", 'not a valid field': 'foobar' }
        self._post('/connectors', 400, json.dumps(new_connector))

    def test_post_fail_request3(self):
        """POST connector with invalid name"""

        new_connector = {
            'name': ''
        }

        # Add
        self._post('/connectors', 400, json.dumps(new_connector))

    def test_post_minimum(self):
        """POST connector with minimum configuration"""

        minimum = {
            'name': 'new_connector'
        }

        # Add
        rv1 = self._post('/connectors', 201, json.dumps(minimum))

        # Query
        rv2 = self._get('/connectors/new_connector', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key in minimum.keys():
            self.assertEqual(minimum[key], ret1[key])

    def test_post_maximum(self):
        """POST connector with maximum configuration"""

        # Not currently possible to test because connector only has
        # one attribute.

        pass

if __name__ == '__main__':
    unittest.main(buffer = True)
