import unittest
from src.arithmetic_operations import ArithmeticOperations

class TestArithmeticOperations(unittest.TestCase):
    
    def setUp(self):
        self.ops = ArithmeticOperations()
        self.max_int = 2 ** 31 - 1
        self.min_int = -2 ** 31
    
    def test_convert_decimal_to_binary_with_verification(self):
        """Тест перевода с проверкой обратного преобразования"""
        test_numbers = [0, 42, -42, 127, -128, 1000, -1000, self.max_int, self.min_int]
        
        for num in test_numbers:
            with self.subTest(num=num):
                result = self.ops.convert_decimal_to_binary(num)
                self.assertEqual(result['decimal'], num)
                
                if num == self.min_int:
                    self.assertTrue(result['direct']['decimal_back'] == 0 or 
                                  result['direct']['decimal_back'] == num)
                    self.assertTrue(result['reverse']['match'] or 
                                  result['reverse']['decimal_back'] == 0)
                    self.assertTrue(result['additional']['match'])
                    self.assertEqual(result['additional']['decimal_back'], num)
                else:
                    self.assertTrue(result['direct']['match'])
                    self.assertEqual(result['direct']['decimal_back'], num)
                    self.assertTrue(result['reverse']['match'])
                    self.assertTrue(result['additional']['match'])
                    self.assertEqual(result['additional']['decimal_back'], num)
    
    def test_add_additional_with_verification(self):
        """Тест сложения с проверкой"""
        test_cases = [
            (15, 27, 42),
            (-15, -27, -42),
            (30, -12, 18),
            (-30, 12, -18),
            (0, 42, 42),
            (self.max_int, 1, self.max_int),
            (self.min_int, -1, self.min_int),
            (2**30, 2**30, self.max_int)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.ops.add_additional(a, b)
                self.assertTrue(result['verification']['match'])
                self.assertEqual(result['decimal'], expected)
    
    def test_subtract_additional_with_verification(self):
        """Тест вычитания с проверкой"""
        test_cases = [
            (42, 15, 27),
            (15, 42, -27),
            (-42, -15, -27),
            (30, -12, 42),
            (0, 42, -42),
            (self.min_int, 1, self.min_int),
            (self.max_int, -1, self.max_int)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.ops.subtract_additional(a, b)
                self.assertTrue(result['verification']['match'])
                self.assertEqual(result['decimal'], expected)
    
    def test_multiply_direct_with_verification(self):
        """Тест умножения с проверкой"""
        test_cases = [
            (6, 7, 42),
            (-6, 7, -42),
            (-6, -7, 42),
            (42, 0, 0),
            (1000, 1000, 1000000),
            (2**20, 2**11, self.max_int),
            (self.max_int, 2, self.max_int)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.ops.multiply_direct(a, b)
                self.assertTrue(result['verification']['match'])
                self.assertEqual(result['decimal'], expected)
    
    def test_divide_direct_with_verification(self):
        """Тест деления с проверкой"""
        test_cases = [
            (42, 6, 7.0),
            (10, 3, 3.33333),
            (-42, 6, -7.0),
            (42, -6, -7.0),
            (-42, -6, 7.0)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.ops.divide_direct(a, b, 5)
                self.assertTrue(result['verification']['match'])
                self.assertAlmostEqual(result['decimal'], expected, places=4)
    
    def test_ieee_add_with_verification(self):
        """Тест IEEE-754 сложения с проверкой"""
        test_cases = [
            (3.14, 2.71, 5.85),
            (-1.5, -2.5, -4.0),
            (1.5, -2.5, -1.0),
            (0.1, 0.2, 0.3)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.ops.ieee_add(a, b)
                self.assertTrue(result['verification']['match'])
                self.assertAlmostEqual(result['decimal'], expected, places=5)
                self.assertAlmostEqual(result['back_to_float'], result['decimal'], places=5)
    
    def test_ieee_multiply_with_verification(self):
        """Тест IEEE-754 умножения с проверкой"""
        test_cases = [
            (2.5, 1.5, 3.75),
            (-2.5, 1.5, -3.75),
            (-2.5, -1.5, 3.75),
            (0.5, 0.5, 0.25)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.ops.ieee_multiply(a, b)
                self.assertTrue(result['verification']['match'])
                self.assertAlmostEqual(result['decimal'], expected, places=5)
                self.assertAlmostEqual(result['back_to_float'], result['decimal'], places=5)
    
    def test_ieee_divide_with_verification(self):
        """Тест IEEE-754 деления с проверкой"""
        test_cases = [
            (10.0, 2.0, 5.0),
            (5.0, 2.0, 2.5),
            (1.0, 3.0, 0.33333),
            (-10.0, 2.0, -5.0)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.ops.ieee_divide(a, b)
                self.assertTrue(result['verification']['match'])
                self.assertAlmostEqual(result['decimal'], expected, places=4)
                self.assertAlmostEqual(result['back_to_float'], result['decimal'], places=4)
    
    def test_bcd_add_with_verification(self):
        """Тест BCD сложения с проверкой"""
        test_cases = [
            (123, 456, 579),
            (5, 6, 11),
            (99, 1, 100),
            (999, 1, 1000)
        ]
        
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                result = self.ops.bcd_add(a, b)
                self.assertTrue(result['verification']['match'])
                self.assertEqual(result['decimal'], expected)

if __name__ == '__main__':
    unittest.main()