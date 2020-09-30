import unittest

class Test_Main(unittest.TestCase):
    """Test class that tests main application entry point"""

    def test_main_dummy(self):
        """Dummy main test"""

        import switchmng.__main__ as switchmng_main

if __name__ == '__main__':
    unittest.main(buffer = True)
