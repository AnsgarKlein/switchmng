import unittest

from flask.app import Flask

from switchmng import wsgi

class Test_Wsgi(unittest.TestCase):
    """Test class that tests wsgi application entry point"""

    def test_wsgi_dummy(self):
        """Dummy wsgi main test"""

        app = wsgi.app()
        self.assertTrue(isinstance(app, Flask))

if __name__ == '__main__':
    unittest.main(buffer = True)
