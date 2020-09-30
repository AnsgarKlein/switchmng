import unittest

from switchmng import config

class Test_Config(unittest.TestCase):
    """Test class that tests config parser"""

    def setUp(self):
        config.parse_arguments([])

    def _cli_arg(self, args):
        # Check if args is a list or a str
        if isinstance(args, str):
            args = args.split(' ')

        # Parse given argument
        config.parse_arguments(args)

    def test_param_dbtype_fail(self):
        """Test dbtype cli argument with invalid value"""

        try:
            config.parse_arguments(['--dbtype', 'invalid-option'])
        except:
            return
        self.assertTrue(False, msg = 'Expected ArgumentError')

    def test_param_dbtype(self):
        """Test dbtype cli argument"""

        self._cli_arg('--dbtype sqlite')
        self.assertEqual(config.DB_TYPE, 'sqlite')

    def test_param_dbpath(self):
        """Test dbpath cli argument"""

        self._cli_arg('--dbpath /tmp/foo.db')
        self.assertEqual(config.DB_PATH, '/tmp/foo.db')

    def test_param_verbose_fail(self):
        """Test verbose cli argument"""

        try:
            self._cli_arg('--verbose invalid-verbose-option')
        except:
            return
        self.assertTrue(False, msg = 'Expected ArgumentError')

    def test_param_verbose_sql(self):
        """Test verbose cli argument"""

        self._cli_arg('--verbose sql')
        self.assertTrue(config.DB_VERBOSE)

    def test_param_verbose_short_sql(self):
        """Test verbose cli argument"""

        self._cli_arg('-v sql')
        self.assertTrue(config.DB_VERBOSE)

    def test_param_debug(self):
        """Test debug cli argument"""

        self._cli_arg('webserver --debug')
        self.assertTrue(config.DEBUG)

    def test_param_debug_short(self):
        """Test (short) debug cli argument"""

        self._cli_arg('webserver -d')
        self.assertTrue(config.DEBUG)

    def test_param_ip(self):
        """Test ip cli argument"""

        self._cli_arg('webserver --ip 192.168.0.1')
        self.assertEqual(config.IP, '192.168.0.1')

    def test_param_ip_short(self):
        """Test (short) ip cli argument"""

        self._cli_arg('webserver -i 192.168.0.1')
        self.assertEqual(config.IP, '192.168.0.1')

    def test_param_port_short(self):
        """Test (short) port cli argument"""

        self._cli_arg('webserver -p 9081')
        self.assertEqual(config.PORT, 9081)

    def test_param_port(self):
        """Test port cli argument"""

        self._cli_arg('webserver --port 9081')
        self.assertEqual(config.PORT, 9081)

if __name__ == '__main__':
    unittest.main(buffer = True)
