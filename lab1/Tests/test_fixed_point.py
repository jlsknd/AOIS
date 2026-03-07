import unittest
from src.fixed_point import FixedPointOperations

class TestFixedPointOperations(unittest.TestCase):
    
    def setUp(self):
        self.fixed = FixedPointOperations(8)  # Используем 8 бит для простоты тестов
    
    def test_add_additional_positive(self):
        result = self.fixed.add_additional(10, 5)
        self.assertEqual(result['decimal'], 15)
    
    def test_add_additional_negative(self):
        result = self.fixed.add_additional(-10, -5)
        self.assertEqual(result['decimal'], -15)
    
    def test_add_additional_mixed(self):
        result = self.fixed.add_additional(10, -5)
        self.assertEqual(result['decimal'], 5)
    
    def test_subtract_additional(self):
        result = self.fixed.subtract_additional(10, 5)
        self.assertEqual(result['decimal'], 5)
    
    def test_subtract_additional_negative_result(self):
        result = self.fixed.subtract_additional(5, 10)
        self.assertEqual(result['decimal'], -5)
    
    def test_multiply_direct_positive(self):
        result = self.fixed.multiply_direct(6, 7)
        self.assertEqual(result['decimal'], 42)
    
    def test_multiply_direct_negative(self):
        result = self.fixed.multiply_direct(6, -7)
        self.assertEqual(result['decimal'], -42)
    
    def test_multiply_direct_both_negative(self):
        result = self.fixed.multiply_direct(-6, -7)
        self.assertEqual(result['decimal'], 42)
    
    def test_divide_direct(self):
        result = self.fixed.divide_direct(42, 6, 5)
        self.assertAlmostEqual(result['decimal'], 7.0, places=5)
    
    def test_divide_direct_with_fraction(self):
        result = self.fixed.divide_direct(10, 3, 5)
        self.assertAlmostEqual(result['decimal'], 3.33333, places=5)
    
    def test_divide_direct_negative(self):
        result = self.fixed.divide_direct(-42, 6, 5)
        self.assertAlmostEqual(result['decimal'], -7.0, places=5)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.fixed.divide_direct(10, 0)

if __name__ == '__main__':
    unittest.main()