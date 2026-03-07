class BCDConverter:
    """Двоично-десятичный код (8421 BCD)"""
    
    def __init__(self, digits=8):
        self.digits = digits  # Количество десятичных цифр
        self.bits_per_digit = 4
        self.total_bits = digits * self.bits_per_digit
    
    def _int_to_digits(self, num):
        """Ручное преобразование числа в список цифр"""
        if num == 0:
            return [0]
        
        digits = []
        temp = abs(num)
        while temp > 0:
            digits.insert(0, temp % 10)
            temp = temp // 10
        return digits
    
    def _digits_to_int(self, digits):
        """Ручное преобразование списка цифр в число"""
        result = 0
        for digit in digits:
            result = result * 10 + digit
        return result
    
    def _digit_to_bcd(self, digit):
        """Преобразование одной цифры в 4-битный BCD"""
        result = [0] * 4
        temp = digit
        for i in range(3, -1, -1):
            power = 2 ** i
            if temp >= power:
                result[3 - i] = 1
                temp -= power
        return result
    
    def _bcd_to_digit(self, bcd_bits):
        """Преобразование 4-битного BCD в цифру"""
        result = 0
        power = 1
        for i in range(3, -1, -1):
            if bcd_bits[i] == 1:
                result += power
            power *= 2
        return result
    
    def decimal_to_bcd(self, num):
        """Преобразование десятичного числа в BCD"""
        # Получаем цифры числа вручную
        digits = self._int_to_digits(abs(num))
        
        # Ограничиваем количество цифр
        while len(digits) < self.digits:
            digits.insert(0, 0)
        if len(digits) > self.digits:
            digits = digits[-self.digits:]
        
        result = []
        for digit in digits:
            result.extend(self._digit_to_bcd(digit))
        
        return result
    
    def bcd_to_decimal(self, bcd_array):
        """Преобразование BCD в десятичное число"""
        if len(bcd_array) != self.total_bits:
            raise ValueError(f"Ожидается {self.total_bits} бит, получено {len(bcd_array)}")
        
        digits = []
        for i in range(0, self.total_bits, self.bits_per_digit):
            digit_bits = bcd_array[i:i + self.bits_per_digit]
            digits.append(self._bcd_to_digit(digit_bits))
        
        return self._digits_to_int(digits)
    
    def bcd_array_to_string(self, bcd_array):
        """Преобразование BCD массива в строку"""
        result = ""
        for i in range(0, len(bcd_array), self.bits_per_digit):
            if i > 0:
                result += " "
            for j in range(self.bits_per_digit):
                if i + j < len(bcd_array):
                    result += str(bcd_array[i + j])
        return result
    
    def add(self, num1, num2):
        """Сложение в BCD"""
        bcd1 = self.decimal_to_bcd(num1)
        bcd2 = self.decimal_to_bcd(num2)
        
        # Поразрядное сложение с коррекцией
        result_bcd = [0] * self.total_bits
        carry = 0
        
        for i in range(self.digits - 1, -1, -1):
            # Извлекаем текущие цифры
            digit1_bits = bcd1[i * self.bits_per_digit:(i + 1) * self.bits_per_digit]
            digit2_bits = bcd2[i * self.bits_per_digit:(i + 1) * self.bits_per_digit]
            
            digit1 = self._bcd_to_digit(digit1_bits)
            digit2 = self._bcd_to_digit(digit2_bits)
            
            # Складываем с переносом
            digit_sum = digit1 + digit2 + carry
            
            # BCD коррекция
            if digit_sum >= 10:
                digit_sum -= 10
                carry = 1
            else:
                carry = 0
            
            # Записываем результат
            digit_result_bits = self._digit_to_bcd(digit_sum)
            for j in range(self.bits_per_digit):
                result_bcd[i * self.bits_per_digit + j] = digit_result_bits[j]
        
        # Преобразуем результат в число
        result_decimal = self.bcd_to_decimal(result_bcd)
        
        return {
            'binary': self.bcd_array_to_string(result_bcd),
            'decimal': result_decimal,
            'num1_binary': self.bcd_array_to_string(bcd1),
            'num2_binary': self.bcd_array_to_string(bcd2)
        }