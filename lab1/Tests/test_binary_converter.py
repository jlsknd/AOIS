import unittest
from src.binary_converter import BinaryConverter

class TestBinaryConverter(unittest.TestCase):
    
    def setUp(self):
        self.converter = BinaryConverter()
    
    def test_decimal_to_binary_array_positive(self):
        result = self.converter.decimal_to_binary_array(42, 8)
        expected = [0, 0, 1, 0, 1, 0, 1, 0]  # 42 в двоичной
        self.assertEqual(result, expected)
    
    def test_decimal_to_binary_array_negative(self):
        result = self.converter.decimal_to_binary_array(-42, 8)
        expected = [1, 0, 1, 0, 1, 0, 1, 0]  # -42 в прямом коде
        self.assertEqual(result, expected)
    
    def test_binary_array_to_decimal_positive(self):
        binary = [0, 0, 1, 0, 1, 0, 1, 0]
        result = self.converter.binary_array_to_decimal(binary, True)
        self.assertEqual(result, 42)
    
    def test_binary_array_to_decimal_negative(self):
        binary = [1, 0, 1, 0, 1, 0, 1, 0]
        result = self.converter.binary_array_to_decimal(binary, True)
        self.assertEqual(result, -42)
    
    def test_to_direct_code(self):
        result = self.converter.to_direct_code(-42, 8)
        expected = [1, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(result, expected)
    
    def test_to_reverse_code_positive(self):
        result = self.converter.to_reverse_code(42, 8)
        expected = [0, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(result, expected)
    
    def test_to_reverse_code_negative(self):
        result = self.converter.to_reverse_code(-42, 8)
        expected = [1, 1, 0, 1, 0, 1, 0, 1]  # Инвертированные биты
        self.assertEqual(result, expected)
    
    def test_to_additional_code_positive(self):
        result = self.converter.to_additional_code(42, 8)
        expected = [0, 0, 1, 0, 1, 0, 1, 0]
        self.assertEqual(result, expected)
    
    def test_to_additional_code_negative(self):
        result = self.converter.to_additional_code(-42, 8)
        # -42 в доп. коде: инвертировать 42 и добавить 1
        expected = [1, 1, 0, 1, 0, 1, 1, 0]
        self.assertEqual(result, expected)
    
    def test_additional_to_decimal_positive(self):
        binary = [0, 0, 1, 0, 1, 0, 1, 0]
        result = self.converter.additional_to_decimal(binary)
        self.assertEqual(result, 42)
    
    def test_additional_to_decimal_negative(self):
        binary = [1, 1, 0, 1, 0, 1, 1, 0]
        result = self.converter.additional_to_decimal(binary)
        self.assertEqual(result, -42)

if __name__ == '__main__':
    unittest.main()