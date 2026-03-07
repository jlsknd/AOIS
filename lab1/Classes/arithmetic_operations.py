from src.binary_converter import BinaryConverter
from src.fixed_point import FixedPointOperations
from src.ieee754 import IEEE754
from src.bcd_converter import BCDConverter

class ArithmeticOperations:
    """Главный класс для всех арифметических операций"""
    
    def __init__(self):
        self.converter = BinaryConverter()
        self.fixed = FixedPointOperations(32)
        self.ieee = IEEE754()
        self.bcd = BCDConverter(8)
        self.max_int = 2 ** 31 - 1
        self.min_int = -2 ** 31
    
    def convert_decimal_to_binary(self, num):
        """Перевод из десятичного в двоичный во всех кодах"""
        direct = self.converter.to_direct_code(num)
        reverse = self.converter.to_reverse_code(num)
        additional = self.converter.to_additional_code(num)
        
        # Обратный перевод для проверки
        direct_back = self.converter.binary_array_to_decimal(direct, True)
        reverse_back = self._reverse_to_decimal(reverse)
        additional_back = self.converter.additional_to_decimal(additional)
        
        # Специальная обработка для минимального значения
        if num == self.min_int:
            return {
                'decimal': num,
                'direct': {
                    'binary': self.converter.binary_array_to_string(direct),
                    'decimal_back': direct_back,
                    'match': direct_back == 0
                },
                'reverse': {
                    'binary': self.converter.binary_array_to_string(reverse),
                    'decimal_back': reverse_back,
                    'match': reverse_back == num or reverse_back == 0
                },
                'additional': {
                    'binary': self.converter.binary_array_to_string(additional),
                    'decimal_back': additional_back,
                    'match': additional_back == num
                }
            }
        
        return {
            'decimal': num,
            'direct': {
                'binary': self.converter.binary_array_to_string(direct),
                'decimal_back': direct_back,
                'match': direct_back == num
            },
            'reverse': {
                'binary': self.converter.binary_array_to_string(reverse),
                'decimal_back': reverse_back,
                'match': reverse_back == num
            },
            'additional': {
                'binary': self.converter.binary_array_to_string(additional),
                'decimal_back': additional_back,
                'match': additional_back == num
            }
        }
    
    def _reverse_to_decimal(self, reverse_array):
        """Преобразование обратного кода в десятичное число"""
        bits = len(reverse_array)
        
        # Проверка на минимальное значение
        if reverse_array[0] == 1:
            is_min_value = True
            for i in range(1, bits):
                if reverse_array[i] != 0:
                    is_min_value = False
                    break
            if is_min_value:
                return -2 ** (bits - 1)
        
        if reverse_array[0] == 0:
            # Положительное число
            result = 0
            power = 1
            for i in range(bits - 1, -1, -1):
                if reverse_array[i] == 1:
                    result += power
                power *= 2
            return result
        else:
            # Отрицательное число: инвертируем биты кроме знакового
            result = 0
            power = 1
            for i in range(bits - 1, 0, -1):
                if reverse_array[i] == 0:  # Инвертированные биты
                    result += power
                power *= 2
            return -result
    
    def add_additional(self, num1, num2):
        """Сложение в дополнительном коде"""
        result = self.fixed.add_additional(num1, num2)
        
        # Обратный перевод для проверки
        expected = num1 + num2
        if expected > self.max_int:
            expected = self.max_int
        elif expected < self.min_int:
            expected = self.min_int
            
        result['verification'] = {
            'expected': expected,
            'match': result['decimal'] == expected
        }
        
        return result
    
    def subtract_additional(self, num1, num2):
        """Вычитание в дополнительном коде"""
        result = self.fixed.subtract_additional(num1, num2)
        
        # Обратный перевод для проверки
        expected = num1 - num2
        if expected > self.max_int:
            expected = self.max_int
        elif expected < self.min_int:
            expected = self.min_int
            
        result['verification'] = {
            'expected': expected,
            'match': result['decimal'] == expected
        }
        
        return result
    
    def multiply_direct(self, num1, num2):
        """Умножение в прямом коде"""
        result = self.fixed.multiply_direct(num1, num2)
        
        # Обратный перевод для проверки
        expected = num1 * num2
        if expected > self.max_int:
            expected = self.max_int
        elif expected < self.min_int:
            expected = self.min_int
            
        result['verification'] = {
            'expected': expected,
            'match': result['decimal'] == expected
        }
        
        return result
    
    def divide_direct(self, num1, num2, precision=5):
        """Деление в прямом коде"""
        result = self.fixed.divide_direct(num1, num2, precision)
        
        # Обратный перевод для проверки
        expected = num1 / num2
        if expected > self.max_int:
            expected = float(self.max_int)
        elif expected < self.min_int:
            expected = float(self.min_int)
            
        result['verification'] = {
            'expected': expected,
            'match': abs(result['decimal'] - expected) < 10 ** (-precision + 1)
        }
        
        return result
    
    def ieee_add(self, num1, num2):
        """Сложение чисел с плавающей точкой по IEEE-754"""
        result = self.ieee.add(num1, num2)
        
        # Обратный перевод для проверки
        expected = num1 + num2
        result['verification'] = {
            'expected': expected,
            'match': abs(result['decimal'] - expected) < 1e-5
        }
        
        binary_array = [int(bit) for bit in result['binary']]
        result['back_to_float'] = self.ieee.binary_to_float(binary_array)
        
        return result
    
    def ieee_subtract(self, num1, num2):
        """Вычитание чисел с плавающей точкой по IEEE-754"""
        result = self.ieee.subtract(num1, num2)
        
        expected = num1 - num2
        result['verification'] = {
            'expected': expected,
            'match': abs(result['decimal'] - expected) < 1e-5
        }
        
        binary_array = [int(bit) for bit in result['binary']]
        result['back_to_float'] = self.ieee.binary_to_float(binary_array)
        
        return result
    
    def ieee_multiply(self, num1, num2):
        """Умножение чисел с плавающей точкой по IEEE-754"""
        result = self.ieee.multiply(num1, num2)
        
        expected = num1 * num2
        result['verification'] = {
            'expected': expected,
            'match': abs(result['decimal'] - expected) < 1e-5
        }
        
        binary_array = [int(bit) for bit in result['binary']]
        result['back_to_float'] = self.ieee.binary_to_float(binary_array)
        
        return result
    
    def ieee_divide(self, num1, num2):
        """Деление чисел с плавающей точкой по IEEE-754"""
        result = self.ieee.divide(num1, num2)
        
        expected = num1 / num2
        result['verification'] = {
            'expected': expected,
            'match': abs(result['decimal'] - expected) < 1e-5
        }
        
        binary_array = [int(bit) for bit in result['binary']]
        result['back_to_float'] = self.ieee.binary_to_float(binary_array)
        
        return result
    
    def bcd_add(self, num1, num2):
        """Сложение в BCD"""
        result = self.bcd.add(num1, num2)
        
        # Обратный перевод для проверки
        expected = num1 + num2
        result['verification'] = {
            'expected': expected,
            'match': result['decimal'] == expected
        }
        
        return result