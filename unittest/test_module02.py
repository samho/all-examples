import unittest
import inspect

class TestCase02(unittest.TestCase):

    def test_case02(self):
        print ("\nRunning Test Method: " + inspect.stack()[0][3])

    def test_case01(self):
        print ("\nRunning Test Method: " + inspect.stack()[0][3])


if __name__ == 'main':
    unittest.main(verbosity=2)