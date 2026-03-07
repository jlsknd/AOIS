from src.binary_converter import BinaryConverter

class FixedPointOperations:
    """Операции с целыми числами в различных кодах"""
    
    def __init__(self, bits=32):
        self.bits = bits
        self.converter = BinaryConverter()  # Создаем экземпляр
        self.max_value = 2 ** (bits - 1) - 1
        self.min_value = -2 ** (bits - 1)
    
    def _int_to_binary_string(self, num):
        """Ручное преобразование целого числа в двоичную строку"""
        if num == 0:
            return "0"
        
        binary_digits = []
        temp = num
        while temp > 0:
            binary_digits.insert(0, str(temp % 2))
            temp = temp // 2
        
        return ''.join(binary_digits)
    
    def add_additional(self, num1, num2):
        """Сложение двух чисел в дополнительном коде"""
        # Получаем дополнительный код для обоих чисел
        add1 = self.converter.to_additional_code(num1, self.bits)
        add2 = self.converter.to_additional_code(num2, self.bits)
        
        # Складываем побитово
        result = [0] * self.bits
        carry = 0
        
        for i in range(self.bits - 1, -1, -1):
            total = add1[i] + add2[i] + carry
            result[i] = total % 2
            carry = total // 2
        
        # Преобразуем результат в десятичное число
        decimal_result = self.converter.additional_to_decimal(result)
        
        # Проверка на переполнение
        if num1 + num2 > self.max_value:
            decimal_result = self.max_value
        elif num1 + num2 < self.min_value:
            decimal_result = self.min_value
        
        return {
            'binary': self.converter.binary_array_to_string(result),
            'decimal': decimal_result,
            'num1_binary': self.converter.binary_array_to_string(add1),
            'num2_binary': self.converter.binary_array_to_string(add2)
        }
    
    def subtract_additional(self, num1, num2):
        """Вычитание через дополнительный код (num1 - num2)"""
        return self.add_additional(num1, -num2)
    
    def multiply_direct(self, num1, num2):
        """Умножение в прямом коде"""
        # Определяем знак результата
        sign = 1 if (num1 >= 0) == (num2 >= 0) else -1
        
        # Получаем прямые коды абсолютных значений
        abs_num1 = abs(num1)
        abs_num2 = abs(num2)
        
        # Ручное умножение "в столбик"
        product = 0
        temp = abs_num2
        shift = 0
        while temp > 0:
            if temp % 2 == 1:
                # Ручное сложение со сдвигом
                shifted = abs_num1
                for _ in range(shift):
                    shifted = self._add_without_plus(shifted, shifted)
                product = self._add_without_plus(product, shifted)
            temp = temp // 2
            shift += 1
        
        result = product * sign
        
        # Проверка на переполнение
        if result > self.max_value:
            result = self.max_value
        elif result < self.min_value:
            result = self.min_value
        
        result_direct = self.converter.to_direct_code(result, self.bits)
        num1_direct = self.converter.to_direct_code(num1, self.bits)
        num2_direct = self.converter.to_direct_code(num2, self.bits)
        
        return {
            'binary': self.converter.binary_array_to_string(result_direct),
            'decimal': result,
            'num1_binary': self.converter.binary_array_to_string(num1_direct),
            'num2_binary': self.converter.binary_array_to_string(num2_direct)
        }
    
    def _add_without_plus(self, a, b):
        """Ручное сложение без использования оператора +"""
        while b != 0:
            carry = a & b
            a = a ^ b
            b = carry << 1
        return a
    
    def divide_direct(self, num1, num2, precision=5):
        """Деление в прямом коде с точностью до precision знаков"""
        if num2 == 0:
            raise ValueError("Деление на ноль!")
        
        # Определяем знак результата
        sign = 1 if (num1 >= 0) == (num2 >= 0) else -1
        
        # Берем абсолютные значения
        dividend = abs(num1)
        divisor = abs(num2)
        
        # Ручное деление
        quotient = 0
        remainder = dividend
        
        # Ручное вычитание для получения целой части
        while remainder >= divisor:
            remainder -= divisor
            quotient += 1
        
        # Дробная часть с заданной точностью
        fractional = []
        temp_remainder = remainder
        for _ in range(precision):
            temp_remainder *= 10
            digit = 0
            while temp_remainder >= divisor:
                temp_remainder -= divisor
                digit += 1
            fractional.append(digit)
        
        # Формируем результат
        fractional_str = ''.join(str(d) for d in fractional)
        result = float(f"{quotient}.{fractional_str}") * sign
        
        # Проверка на переполнение
        if result > self.max_value:
            result = float(self.max_value)
        elif result < self.min_value:
            result = float(self.min_value)
        
        # Ручное получение двоичного представления дробной части
        binary_int = self._int_to_binary_string(quotient) if quotient > 0 else '0'
        binary_frac = []
        
        frac_part = dividend / divisor - quotient
        temp_frac = frac_part
        for _ in range(precision):
            temp_frac *= 2
            bit = 1 if temp_frac >= 1 else 0
            binary_frac.append(str(bit))
            if temp_frac >= 1:
                temp_frac -= 1
        
        binary_result = f"{binary_int}.{''.join(binary_frac)}"
        
        num1_direct = self.converter.to_direct_code(num1, self.bits)
        num2_direct = self.converter.to_direct_code(num2, self.bits)
        
        return {
            'quotient': result,
            'quotient_binary': binary_result,
            'decimal': result,
            'num1_binary': self.converter.binary_array_to_string(num1_direct),
            'num2_binary': self.converter.binary_array_to_string(num2_direct)
        }