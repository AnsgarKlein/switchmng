import switchmng
from switchmng.schema import *

import unittest

class Test_Resource_SwitchModel(unittest.TestCase):

    def setUp(self):
        ports = [
            {
                'name': 'port1',
            },
            {
                'name': 'port2',
            },
        ]
        ports = [ PortModel(**p) for p in ports ]

        self.example_switch = {
            'name': 'example',
            'ports': ports,
            'size': 5,
        }

    def test_switch(self):
        """Create switch object"""

        sm1 = SwitchModel(**self.example_switch)
        self.assertTrue(isinstance(sm1, SwitchModel))

        self.example_switch['size'] = None
        sm2 = SwitchModel(**self.example_switch)
        self.assertTrue(isinstance(sm2, SwitchModel))

    def test_switch_fail_invalid(self):
        """Create switch object with additional invalid attribute"""

        self.example_switch['non-existent'] = None
        with self.assertRaises(TypeError):
            SwitchModel(**self.example_switch)

    def test_fail_name1(self):
        """Create switch object with invalid 'name' attribute"""

        self.example_switch['name'] = 123
        with self.assertRaises(TypeError):
            SwitchModel(**self.example_switch)

    def test_fail_name2(self):
        """Create switch object with invalid 'name' attribute"""

        self.example_switch['name'] = ''
        with self.assertRaises(ValueError):
            SwitchModel(**self.example_switch)

    def test_fail_ports1(self):
        """Create switch object with invalid 'ports' attribute"""

        self.example_switch['ports'] = 'foo bar'
        with self.assertRaises(TypeError):
            SwitchModel(**self.example_switch)

    def test_fail_ports2(self):
        """Create switch object with invalid 'ports' attribute"""

        self.example_switch['ports'] = [ 'foo', 'bar' ]
        with self.assertRaises(TypeError):
            SwitchModel(**self.example_switch)

    def test_fail_size1(self):
        """Create switch object with invalid 'size' attribute"""

        self.example_switch['size'] = 'huge'
        with self.assertRaises(TypeError):
            SwitchModel(**self.example_switch)

    def test_fail_size2(self):
        """Create switch object with invalid 'size' attribute"""

        self.example_switch['size'] = 0
        with self.assertRaises(ValueError):
            SwitchModel(**self.example_switch)

    def test_fail_size3(self):
        """Create switch object with invalid 'size' attribute"""

        self.example_switch['size'] = -1
        with self.assertRaises(ValueError):
            SwitchModel(**self.example_switch)

if __name__ == '__main__':
    unittest.main(buffer = True)
