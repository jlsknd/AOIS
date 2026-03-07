import unittest
import math
from src.ieee754 import IEEE754

class TestIEEE754(unittest.TestCase):
    
    def setUp(self):
        self.ieee = IEEE754()
    
    def test_float_to_binary_zero(self):
        result = self.ieee.float_to_binary(0.0)
        self.assertEqual(sum(result), 0)  # Все биты должны быть 0
    
    def test_float_to_binary_one(self):
        result = self.ieee.float_to_binary(1.0)
        # 1.0 в IEEE-754: 0 01111111 00000000000000000000000
        self.assertEqual(result[0], 0)  # sign
        # exponent = 127
        exp_part = result[1:9]
        exp_value = 0
        for i, bit in enumerate(exp_part):
            exp_value = (exp_value << 1) | bit
        self.assertEqual(exp_value, 127)
    
    def test_binary_to_float(self):
        binary = [0] * 32
        # 1.0
        binary[1:9] = [0, 1, 1, 1, 1, 1, 1, 1]  # exponent = 127
        result = self.ieee.binary_to_float(binary)
        self.assertEqual(result, 1.0)
    
    def test_add(self):
        result = self.ieee.add(1.5, 2.5)
        self.assertAlmostEqual(result['decimal'], 4.0, places=5)
    
    def test_subtract(self):
        result = self.ieee.subtract(5.5, 2.2)
        self.assertAlmostEqual(result['decimal'], 3.3, places=5)
    
    def test_multiply(self):
        result = self.ieee.multiply(3.0, 1.5)
        self.assertAlmostEqual(result['decimal'], 4.5, places=5)
    
    def test_divide(self):
        result = self.ieee.divide(10.0, 2.0)
        self.assertAlmostEqual(result['decimal'], 5.0, places=5)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.ieee.divide(10.0, 0.0)
    
    def test_infinity(self):
        inf_binary = self.ieee.float_to_binary(float('inf'))
        self.assertEqual(inf_binary[0], 0)
        for i in range(1, 9):
            self.assertEqual(inf_binary[i], 1)
    
    def test_nan(self):
        nan_binary = self.ieee.float_to_binary(float('nan'))
        self.assertEqual(nan_binary[0], 0)
        for i in range(1, 9):
            self.assertEqual(nan_binary[i], 1)
        self.assertEqual(nan_binary[9], 1)

if __name__ == '__main__':
    unittest.main()