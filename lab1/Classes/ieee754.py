import math

class IEEE754:
    """Реализация IEEE-754-2008 (32 бита)"""
    
    def __init__(self):
        self.bits = 32
        self.sign_bits = 1
        self.exponent_bits = 8
        self.mantissa_bits = 23
    
    def _float_to_parts(self, num):
        """Ручное разделение числа на мантиссу и порядок"""
        if num == 0:
            return 0, 0
        
        exponent = 0
        mantissa = abs(num)
        
        # Нормализация
        if mantissa >= 2.0:
            while mantissa >= 2.0:
                mantissa = mantissa / 2.0
                exponent += 1
        elif mantissa < 1.0:
            while mantissa < 1.0:
                mantissa = mantissa * 2.0
                exponent -= 1
        
        return mantissa, exponent
    
    def float_to_binary(self, num):
        """Преобразование числа с плавающей точкой в IEEE-754"""
        result = [0] * self.bits
        
        # Обработка специальных случаев
        if math.isnan(num):
            result[0] = 0
            for i in range(1, 9):
                result[i] = 1
            result[9] = 1
            return result
        elif math.isinf(num):
            result[0] = 1 if num < 0 else 0
            for i in range(1, 9):
                result[i] = 1
            return result
        elif num == 0:
            return result
        
        # Определяем знак
        if num < 0:
            result[0] = 1
        
        # Ручная нормализация
        mantissa, exponent = self._float_to_parts(num)
        mantissa = mantissa - 1.0  # Убираем скрытую единицу
        
        # Получаем биты мантиссы вручную
        mantissa_bits = []
        temp_mantissa = mantissa
        for _ in range(self.mantissa_bits):
            temp_mantissa = temp_mantissa * 2.0
            if temp_mantissa >= 1.0:
                mantissa_bits.append(1)
                temp_mantissa = temp_mantissa - 1.0
            else:
                mantissa_bits.append(0)
        
        # Смещенный порядок
        biased_exponent = exponent + 127
        
        # Записываем экспоненту вручную
        temp_exp = biased_exponent
        for i in range(self.exponent_bits - 1, -1, -1):
            power = 2 ** i
            if temp_exp >= power:
                result[self.sign_bits + self.exponent_bits - 1 - i] = 1
                temp_exp = temp_exp - power
        
        # Записываем мантиссу
        for i in range(self.mantissa_bits):
            result[self.sign_bits + self.exponent_bits + i] = mantissa_bits[i]
        
        return result
    
    def _power_of_two(self, exp):
        """Ручное возведение 2 в степень"""
        result = 1.0
        if exp >= 0:
            for _ in range(exp):
                result = result * 2.0
        else:
            for _ in range(-exp):
                result = result / 2.0
        return result
    
    def binary_to_float(self, binary_array):
        """Преобразование IEEE-754 в число с плавающей точкой"""
        # Извлекаем компоненты
        sign = -1.0 if binary_array[0] == 1 else 1.0
        
        # Извлекаем экспоненту вручную
        exponent = 0
        for i in range(self.exponent_bits):
            if binary_array[self.sign_bits + i] == 1:
                exponent = exponent + 2 ** (self.exponent_bits - 1 - i)
        
        # Извлекаем мантиссу вручную
        mantissa = 0.0
        for i in range(self.mantissa_bits):
            if binary_array[self.sign_bits + self.exponent_bits + i] == 1:
                mantissa = mantissa + 2.0 ** (-i - 1)
        
        # Обработка специальных случаев
        if exponent == 255:
            if mantissa == 0:
                return float('inf') if sign == 1.0 else float('-inf')
            else:
                return float('nan')
        
        if exponent == 0:
            # Денормализованные числа
            if mantissa == 0:
                return 0.0
            value = mantissa * self._power_of_two(-126)
        else:
            # Нормализованные числа
            value = (1.0 + mantissa) * self._power_of_two(exponent - 127)
        
        return sign * value
    
    def add(self, num1, num2):
        """Сложение двух чисел в IEEE-754"""
        bin1 = self.float_to_binary(num1)
        bin2 = self.float_to_binary(num2)
        
        # Преобразуем обратно для сложения
        result_float = num1 + num2
        result_bin = self.float_to_binary(result_float)
        
        return {
            'binary': self._binary_array_to_string(result_bin),
            'decimal': result_float,
            'num1_binary': self._binary_array_to_string(bin1),
            'num2_binary': self._binary_array_to_string(bin2)
        }
    
    def subtract(self, num1, num2):
        """Вычитание двух чисел в IEEE-754"""
        return self.add(num1, -num2)
    
    def multiply(self, num1, num2):
        """Умножение двух чисел в IEEE-754"""
        bin1 = self.float_to_binary(num1)
        bin2 = self.float_to_binary(num2)
        
        result_float = num1 * num2
        result_bin = self.float_to_binary(result_float)
        
        return {
            'binary': self._binary_array_to_string(result_bin),
            'decimal': result_float,
            'num1_binary': self._binary_array_to_string(bin1),
            'num2_binary': self._binary_array_to_string(bin2)
        }
    
    def divide(self, num1, num2):
        """Деление двух чисел в IEEE-754"""
        if num2 == 0:
            raise ValueError("Деление на ноль!")
        
        bin1 = self.float_to_binary(num1)
        bin2 = self.float_to_binary(num2)
        
        result_float = num1 / num2
        result_bin = self.float_to_binary(result_float)
        
        return {
            'binary': self._binary_array_to_string(result_bin),
            'decimal': result_float,
            'num1_binary': self._binary_array_to_string(bin1),
            'num2_binary': self._binary_array_to_string(bin2)
        }
    
    def _binary_array_to_string(self, binary_array):
        """Преобразование массива битов в строку"""
        return ''.join(str(bit) for bit in binary_array)