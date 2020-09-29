import switchmng

import unittest

class Test_Main(unittest.TestCase):
    def test_main_dummy(self):
        """Dummy main test"""

        import switchmng.__main__

if __name__ == '__main__':
    unittest.main(buffer = True)
