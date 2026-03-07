import unittest
from src.bcd_converter import BCDConverter

class TestBCDConverter(unittest.TestCase):
    
    def setUp(self):
        self.bcd = BCDConverter(4)  # 4 десятичные цифры
    
    def test_decimal_to_bcd(self):
        """Тест преобразования десятичного числа в BCD"""
        result = self.bcd.decimal_to_bcd(1234)
        # 1=0001, 2=0010, 3=0011, 4=0100
        expected = [0,0,0,1, 0,0,1,0, 0,0,1,1, 0,1,0,0]
        self.assertEqual(result, expected)
    
    def test_bcd_to_decimal(self):
        """Тест преобразования BCD в десятичное число"""
        bcd = [0,0,0,1, 0,0,1,0, 0,0,1,1, 0,1,0,0]
        result = self.bcd.bcd_to_decimal(bcd)
        self.assertEqual(result, 1234)
    
    def test_add_no_carry(self):
        """Тест сложения без переноса"""
        result = self.bcd.add(123, 456)
        self.assertEqual(result['decimal'], 579)
    
    def test_add_with_carry(self):
        """Тест сложения с переносом"""
        result = self.bcd.add(5, 6)
        self.assertEqual(result['decimal'], 11)
    
    def test_add_with_multiple_carries(self):
        """Тест сложения с несколькими переносами"""
        result = self.bcd.add(99, 1)
        self.assertEqual(result['decimal'], 100)
    
    def test_add_edge_cases(self):
        """Тест граничных случаев сложения"""
        result = self.bcd.add(999, 1)
        self.assertEqual(result['decimal'], 1000)
        
        result = self.bcd.add(0, 0)
        self.assertEqual(result['decimal'], 0)
        
        result = self.bcd.add(9999, 1)  # Переполнение разрядной сетки
        self.assertNotEqual(result['decimal'], 10000)  # Должно обрезаться

if __name__ == '__main__':
    unittest.main()