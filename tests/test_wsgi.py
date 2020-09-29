import switchmng
from switchmng import wsgi

from flask.app import Flask

import unittest

class Test_Wsgi(unittest.TestCase):
    def test_wsgi_dummy(self):
        """Dummy wsgi main test"""

        app = wsgi.app()
        self.assertTrue(isinstance(app, Flask))

if __name__ == '__main__':
    unittest.main(buffer = True)
