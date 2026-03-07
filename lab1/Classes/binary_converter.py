class BinaryConverter:
    """Класс для конвертации между десятичными и двоичными числами"""
    
    def __init__(self):
        pass
    
    def decimal_to_binary_array(self, num, bits=32, signed=True):
        """
        Преобразование десятичного числа в массив битов (прямой код)
        Возвращает список из 0 и 1 длиной bits
        """
        result = [0] * bits
        
        if num == 0:
            return result
        
        # Специальная обработка для минимального значения
        min_value = -2 ** (bits - 1)
        if num == min_value:
            if signed:
                # Для минимального значения в дополнительном коде
                result[0] = 1
                return result
            else:
                # Для беззнакового представления
                num = abs(num)
        
        # Определяем знак
        is_negative = num < 0
        num = abs(num)
        
        # Преобразуем абсолютное значение в двоичное
        if num > 0:
            binary_digits = []
            temp = num
            while temp > 0:
                binary_digits.insert(0, temp % 2)
                temp = temp // 2
            
            # Заполняем массив справа налево
            for i in range(len(binary_digits)):
                if bits - 1 - i >= 0:
                    result[bits - 1 - i] = binary_digits[len(binary_digits) - 1 - i]
        
        # Устанавливаем знаковый бит
        if signed and is_negative:
            result[0] = 1
            
        return result
    
    def binary_array_to_decimal(self, binary_array, signed=True):
        """
        Преобразование массива битов (прямой код) в десятичное число
        """
        bits = len(binary_array)
        result = 0
        
        # Вычисляем значение без учета знака
        power = 1
        for i in range(bits - 1, 0, -1):  # Пропускаем знаковый бит
            if binary_array[i] == 1:
                result += power
            power *= 2
        
        # Если число отрицательное в прямом коде
        if signed and binary_array[0] == 1:
            result = -result
            
        return result
    
    def binary_array_to_string(self, binary_array):
        """Преобразование массива битов в строку"""
        return ''.join(str(bit) for bit in binary_array)
    
    def to_direct_code(self, num, bits=32):
        """Прямой код"""
        return self.decimal_to_binary_array(num, bits, True)
    
    def to_reverse_code(self, num, bits=32):
        """Обратный код"""
        min_value = -2 ** (bits - 1)
        if num == min_value:
            # Для минимального числа обратный код = 1000...0
            result = [0] * bits
            result[0] = 1
            return result
            
        if num >= 0:
            return self.to_direct_code(num, bits)
        
        # Для отрицательных чисел: знаковый бит = 1, остальные инвертируем
        abs_num = abs(num)
        direct = self.decimal_to_binary_array(abs_num, bits, False)
        result = [0] * bits
        result[0] = 1  # Устанавливаем знаковый бит
        # Инвертируем все биты кроме знакового
        for i in range(1, bits):
            result[i] = 1 - direct[i]
        return result
    
    def to_additional_code(self, num, bits=32):
        """Дополнительный код"""
        min_value = -2 ** (bits - 1)
        if num == min_value:
            # Для минимального числа дополнительный код = 1000...0
            result = [0] * bits
            result[0] = 1
            return result
            
        if num >= 0:
            return self.to_direct_code(num, bits)
        
        # Для отрицательных: обратный код + 1
        reverse = self.to_reverse_code(num, bits)
        
        # Добавляем 1
        result = reverse.copy()
        carry = 1
        for i in range(bits - 1, -1, -1):
            if result[i] == 1 and carry == 1:
                result[i] = 0
            elif result[i] == 0 and carry == 1:
                result[i] = 1
                carry = 0
                break
        
        return result
    
    def additional_to_decimal(self, binary_array):
        """Преобразование из дополнительного кода в десятичное"""
        bits = len(binary_array)
        
        # Проверка на минимальное значение
        if binary_array[0] == 1:
            is_min_value = True
            for i in range(1, bits):
                if binary_array[i] != 0:
                    is_min_value = False
                    break
            if is_min_value:
                return -2 ** (bits - 1)
        
        if binary_array[0] == 0:
            # Положительное число
            result = 0
            power = 1
            for i in range(bits - 1, -1, -1):
                if binary_array[i] == 1:
                    result += power
                power *= 2
            return result
        
        # Отрицательное число: инвертируем и добавляем 1
        inverted = [1 - bit for bit in binary_array]
        
        # Добавляем 1
        carry = 1
        for i in range(bits - 1, -1, -1):
            if inverted[i] == 1 and carry == 1:
                inverted[i] = 0
            elif inverted[i] == 0 and carry == 1:
                inverted[i] = 1
                carry = 0
                break
        
        # Вычисляем значение
        result = 0
        power = 1
        for i in range(bits - 1, -1, -1):
            if inverted[i] == 1:
                result += power
            power *= 2
        
        return -result