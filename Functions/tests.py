# unit tests for all functions

import unittest
from special_fn import *
from subordinate_fn import PI

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

class Test_SD(unittest.TestCase):

    def test_sd_ints(self):
        self.assertEqual(round(standard_deviation([12, 11, 17, 15, 13, 12, 14, 15], True), 10), 1.9955307207)
        self.assertEqual(round(standard_deviation([12, 11, 17, 15, 13, 12, 14, 15], False), 10), 1.8666480654)
        
    def test_sd_floats(self):
        self.assertEqual(round(standard_deviation([2.5, 3.4, 2.1, 3.1, 3.2, 2.9], True), 10), 0.4844240567)
        self.assertEqual(round(standard_deviation([2.5, 3.4, 2.1, 3.1, 3.2, 2.9], False), 10), 0.4422166387)

    def test_sd_mixed(self):
        self.assertEqual(round(standard_deviation([7, 6.5, 7.5, 6, 3, 5.6], True), 10), 1.5895492023)
        self.assertEqual(round(standard_deviation([7, 6.5, 7.5, 6, 3, 5.6], False), 10), 1.4510532573)

class Test_MAD(unittest.TestCase):

    def test_mad_ints(self):
        self.assertEqual(round(mad([12, 11, 17, 15, 13, 12, 14, 15]), 10), 1.625)
        
    def test_mad_floats(self):
        self.assertEqual(round(mad([2.5, 3.4, 2.1, 3.1, 3.2, 2.9]), 10), 0.3777777778)

    def test_mad_mixed(self):
        self.assertEqual(round(mad([7, 6.5, 7.5, 6, 3, 5.6]), 10), 1.0888888889)

class Test_Natural_Exp(unittest.TestCase):

    def test_natural_exp_(self):
        self.assertEqual(round(natural_exp(2, 3, 4), 10), 162)
        self.assertEqual(round(natural_exp(100, 1.1, 4), 10), 146.41)
        self.assertEqual(round(natural_exp(-100, 0.5, -10), 10), -102400)

class Test_Sinh(unittest.TestCase):

    def test_sinh(self):
        self.assertEqual(round(sinh(0), 10), 0)
        self.assertEqual(round(sinh(1), 10), 1.1752011936)
        self.assertEqual(round(sinh(PI), 10), 11.5487393573)

class Test_Power(unittest.TestCase):

    def test_power(self):
        self.assertEqual(round(power(2, 10), 10), 1024)
        self.assertEqual(round(power(2, 2.5), 10), 5.6568542495)
        self.assertEqual(round(power(2.5, 2), 10), 6.25)
        self.assertEqual(round(power(2.5, 2.5), 10), 9.8821176880)

class Test_Arccos(unittest.TestCase):

    def test_arccos_valid_input(self):
        self.assertEqual(round(arccos(1), 10), 0)
        self.assertEqual(round(arccos(-1), 10), 3.1415926536)
        self.assertEqual(round(arccos(0.5), 10), 1.0471974888)
        self.assertEqual(round(arccos(0.1), 10), 1.4706289917)

    def test_arccos_invalid_input(self):
        self.assertEqual(arccos(5), None)
        self.assertEqual(arccos(-2), None)

if __name__ == '__main__':
    unittest.main()