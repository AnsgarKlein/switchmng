from test_rest import Test_REST

import json

import unittest

class Test_REST_SwitchModel(Test_REST):

    example_model = {
        'name':  'example_model',
        'size':  4,
        'ports': [
            {
                'name': 'p1',
                'network_protocols': [ 'proto1', 'proto2' ],
                'connector': 'rj45'
            },
        ],
    }

    def setUp(self):
        super().setUp()

        # Add some default values
        self.setUp_vlans()
        self.setUp_connectors()
        self.setUp_network_protocols()

        # Add a switch model
        rv = self._post('/switch_models', 201, json.dumps(self.example_model))
        self.example_model = rv['data']

    def test_options1(self):
        """OPTIONS verb for switch models"""

        rv = self._options('/switch_models', 200)

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
        """OPTIONS verb for specific switch model"""

        rv = self._options('/switch_models/example_model', 200)

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
        """HEAD verb for non existing switch model"""

        self._head('/switch_models/non-existing', 404)

    def test_head1(self):
        """HEAD verb for switch model"""

        # Query
        rv = self._head('/switch_models/example_model', 200)

        # Check
        self.assertEqual(rv.data.decode(), '')

    def test_get_fail(self):
        """GET non existing switch model"""

        self._get('/switch_models/non-existing-model', 404)

    def test_get(self):
        """GET switch models"""

        # Query
        rv = self._get('/switch_models', 200)

        # Check
        ret = rv['data']
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 1)

        ret = rv['data'][0]
        self.assertTrue(isinstance(ret, dict))

        self.assertEqual(ret, self.example_model)

    def test_delete_fail_inuse(self):
        """DELETE switch model still in use by switch"""

        # Add some values
        self.setUp_switch_models()
        self.setUp_switches()

        # Change switch model of switch
        patch = {
            'model': 'example_model'
        }
        rv = self._patch('/switches/switch1', 200, json.dumps(patch))

        # DELETE
        rv = self._delete('/switch_models/example_model', 400)

        # Change switch model of switch
        patch = {
            'model': 'small_switch'
        }
        rv = self._patch('/switches/switch1', 200, json.dumps(patch))

        # DELETE
        rv = self._delete('/switch_models/example_model', 200)

    def test_delete_fail_nonexisting(self):
        """DELETE non existing switch model"""

        self._delete('/switch_models/non-existing', 404)

    def test_delete_fail_header(self):
        """DELETE switch model with missing 'Accept' header"""

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._delete('/switch_models/example_model', 406, None, headers)

    def test_delete(self):
        """DELETE switch model and check that it is gone"""

        # Query before delete
        self._get('/switch_models/example_model', 200)

        # Delete
        self._delete('/switch_models/example_model', 200)

        # Query after delete
        self._get('/switch_models/example_model', 404)

    def test_patch_fail_nonexisting(self):
        """PATCH non existing switch model"""

        patch = {}
        self._patch('/switch_models/not_existing', 404, json.dumps(patch))

    def test_patch_fail_header1(self):
        """PATCH switch model with missing 'Accept' header"""

        patch = {}
        headers = self.patch_headers.copy()
        headers.pop('Accept')
        self._patch('/switch_models/example_model', 406, json.dumps(patch), headers)

    def test_patch_fail_header2(self):
        """PATCH switch model with missing 'Content-Type' header"""

        patch = {}
        headers = self.patch_headers.copy()
        headers.pop('Content-Type')
        self._patch('/switch_models/example_model', 415, json.dumps(patch), headers)

    def test_patch_fail_request1(self):
        """PATCH switch model with malformed request data"""

        patch = '{ "name": string without quotes }'
        self._patch('/switch_models/example_model', 400, patch)

    def test_patch_fail_request2(self):
        """PATCH switch model with invalid request data"""

        patch = { 'not a valid field': 'foobar' }
        self._patch('/switch_models/example_model', 400, json.dumps(patch))

    def test_patch1(self):
        """
        PATCH switch model with resource identifier.

        Check that PATCHING switch model does not change attributes
        that are not given in request.
        """

        patch = {
            'ports': [
                {
                    'name': 'patched_port1',
                    'network_protocols': [ 'proto1', 'proto2' ],
                }, {
                    'name': 'patched_port2',
                    'network_protocols': [],
                }]
        }

        # Patch
        rv1 = self._patch('/switch_models/example_model', 200, json.dumps(patch))
        rv2 = self._get('/switch_models/example_model', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in self.example_model.items():
            if key in patch:
                pass
            else:
                self.assertEqual(self.example_model[key], ret1[key])

    def test_patch2(self):
        """
        PATCH switch model to different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        patch = {
            'name': 'patched_model',
        }

        # Patch
        rv1 = self._patch('/switch_models/example_model', 200, json.dumps(patch))

        # Query (1)
        self._get('/switch_models/example_model', 404)

        # Query (2)
        rv2 = self._get('/switch_models/patched_model', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_patch3(self):
        """
        PATCH switch model with different ports list.

        This changes ports of switch model. Check that ports of all
        implementing switches change as well.
        """

        # Add some values
        self.setUp_switch_models()
        self.setUp_switches()

        # Check that switch has same ports as switch model
        rv1 = self._get('/switch_models/small_switch', 200)['data']['ports']
        rv2 = self._get('/switches/switch1', 200)['data']['ports']
        rv1 = [ port['name'] for port in rv1 ]
        rv2 = [ port['name'] for port in rv2 ]
        self.assertEqual(set(rv1), set(rv2))

        # Change ports of switch model
        patch = {
            'ports': [
                {
                    'name': 'changed-port1'
                },
                {
                    'name': 'changed-port2'
                }
            ]
        }
        rv = self._patch('/switch_models/small_switch', 200, json.dumps(patch))

        # Check that switch ports have changed as well
        rv3 = self._get('/switches/switch1', 200)['data']['ports']
        rv3 = [ port['name'] for port in rv3 ]
        patch = [ port['name'] for port in patch['ports'] ]
        self.assertEqual(set(patch), set(rv3))

    def test_put_fail_header1(self):
        """PUT switch model with missing 'Accept' header"""

        replacement = {
            'name': 'example_model',
            'size': 1,
        }

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._put('/switch_models/example_model', 406, json.dumps(replacement), headers)

    def test_put_fail_header2(self):
        """PUT switch model with missing 'Content-Type' header"""

        replacement = {
            'name': 'example_model',
            'size': 1,
        }

        headers = self.default_headers.copy()
        headers.pop('Content-Type')
        self._put('/switch_models/example_model', 415, json.dumps(replacement), headers)

    def test_put_fail_request1(self):
        """PUT switch model with malformed request data"""

        replacement = '{ "name": "not closed str, "size": 1, }'
        self._put('/switch_models/example_model', 400, replacement)

    def test_put_fail_request2(self):
        """PUT switch model with invalid request data"""

        replacement = { 'not a valid field': 'foobar' }
        self._put('/switch_models/example_model', 400, replacement)

    def test_put1(self):
        """
        PUT switch model with same resource identifier.

        Check that PUTTING resource changes all attributes to default if
        attributes are not given in request.
        """

        replacement = {
            'name': 'example_model',
            'size': 1,
        }

        # Put
        rv1 = self._put('/switch_models/example_model', 200, json.dumps(replacement))

        # Query
        rv2 = self._get('/switch_models/example_model', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        # Check that all changes from request have been made
        for key, val in replacement.items():
            self.assertEqual(replacement[key], ret1[key])

        # Check that previously set attributes that were not
        # present in request are now unset.
        self.assertEqual(ret1['ports'], [])

    def test_put2(self):
        """
        PUT switch model with different resource identifier.

        This changes resource identifier and makes resource available at
        different endpoint. Check that resource is not available at old
        endpoint but at new endpoint.
        """

        replacement = {
            'name': 'replacement_model',
            'size': 1,
        }

        # Put
        rv1 = self._put('/switch_models/example_model', 200, json.dumps(replacement))

        # Query (1)
        self._get('/switch_models/example_model', 404)

        # Query (2)
        rv2 = self._get('/switch_models/replacement_model', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

    def test_put_new(self):
        """PUT new switch model"""

        new_model = {
            'name': 'new_model',
            'size': 1,
        }

        # Put
        rv1 = self._put('/switch_models/new_model', 200, json.dumps(new_model))

        # Query
        rv2 = self._get('/switch_models/new_model', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in new_model.items():
            self.assertEqual(new_model[key], ret1[key])

    def test_post_fail_header1(self):
        """POST switch model with missing 'Accept' header"""

        new_model = {
            'name': 'new_model',
            'size': 1,
        }

        headers = self.default_headers.copy()
        headers.pop('Accept')
        self._post('/switch_models', 406, json.dumps(new_model), headers)

    def test_post_fail_header2(self):
        """POST switch model with missing 'Content-Type' header"""

        new_model = {
            'name': 'new_model',
            'size': 1,
        }

        headers = self.default_headers.copy()
        headers.pop('Content-Type')
        self._post('/switch_models', 415, json.dumps(new_model), headers)

    def test_post_fail_request1(self):
        """POST switch model with malformed request data"""

        new_model = '{ "name": "not closed str }'
        self._post('/switch_models', 400, new_model)

    def test_post_fail_request2(self):
        """POST switch model with invalid request data"""

        new_model = { "name": "example", 'not a valid field': 'foobar' }
        self._post('/switch_models', 400, new_model)

    def test_post_minimum(self):
        """POST switch model with minimum configuration"""

        minimum = {
            'name':  'minimum_model',
            'ports': [],
        }

        # Add
        rv1 = self._post('/switch_models', 201, json.dumps(minimum))

        # Query
        rv2 = self._get('/switch_models/minimum_model', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)

        for key, val in minimum.items():
            self.assertEqual(minimum[key], ret1[key])

    def test_post_maximum(self):
        """POST switch model with maximum configuration"""

        maximum = {
            'name':  'maximum_model',
            'size':  4,
            'ports': [
                {
                    'name': 'p1',
                    'network_protocols': [ 'proto1', 'proto2' ],
                    'connector': 'rj45'
                }, {
                    'name': 'p2',
                    'network_protocols': [ 'proto2' ],
                    'connector': 'rj45'
                },
            ],
        }

        # Add
        rv1 = self._post('/switch_models', 201, json.dumps(maximum))

        # Query
        rv2 = self._get('/switch_models/maximum_model', 200)

        # Check
        ret1 = rv1['data']
        ret2 = rv2['data']

        self.assertEqual(ret1, ret2)
        self.assertEqual(maximum, ret1)

if __name__ == '__main__':
    unittest.main(buffer = True)
