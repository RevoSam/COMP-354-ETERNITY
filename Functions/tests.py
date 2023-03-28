# unit tests for all functions

import unittest
from gamma import *

class Test_Gamma(unittest.TestCase):

    # tests at 9 decimal points precision
    def test_gamma_valid_input(self):
        self.assertEqual(round(gamma(0.1), 9), 9.513507699)
        self.assertEqual(round(gamma(0.2), 9), 4.590843712)
        self.assertEqual(round(gamma(0.5), 9), 1.772453851)
        self.assertEqual(round(gamma(1), 9), 1)
        self.assertEqual(round(gamma(2), 9), 1)
        self.assertEqual(round(gamma(5), 9), 24)
    
    def test_gamma_invalid_input(self):
        self.assertEqual(gamma(0), None)
        self.assertEqual(gamma(-1), None)

if __name__ == '__main__':
    unittest.main()