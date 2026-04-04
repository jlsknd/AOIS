class PostClasses:
    """
    Класс для определения принадлежности функции к классам Поста:
    1. T0 - сохраняющие 0
    2. T1 - сохраняющие 1
    3. S - самодвойственные
    4. M - монотонные
    5. L - линейные
    """
    
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.vector = truth_table.get_vector()
    
    def is_t0(self):
        """Проверка на сохранение 0"""
        # На наборе (0,0,...,0) функция должна быть 0
        return self.vector[0] == 0
    
    def is_t1(self):
        """Проверка на сохранение 1"""
        # На наборе (1,1,...,1) функция должна быть 1
        return self.vector[-1] == 1
    
    def is_self_dual(self):
        """Проверка на самодвойственность"""
        n = len(self.variables)
        for i in range(2 ** n):
            # f(x) != ¬f(¬x)
            inverted_index = (2 ** n - 1) ^ i
            if self.vector[i] == self.vector[inverted_index]:
                return False
        return True
    
    def is_monotone(self):
        """Проверка на монотонность"""
        n = len(self.variables)
        for i in range(2 ** n):
            for j in range(2 ** n):
                # Если i <= j (поэлементно), то f(i) <= f(j)
                if self._is_less_or_equal(i, j, n):
                    if self.vector[i] > self.vector[j]:
                        return False
        return True
    
    def _is_less_or_equal(self, a, b, n):
        """Проверка, что все биты a <= битов b"""
        for shift in range(n):
            bit_a = (a >> (n - 1 - shift)) & 1
            bit_b = (b >> (n - 1 - shift)) & 1
            if bit_a > bit_b:
                return False
        return True
    
    def is_linear(self):
        """Проверка на линейность (через полином Жегалкина)"""
        # Линейная функция: f(x) = a0 ⊕ a1x1 ⊕ ... ⊕ anxn
        # Получаем коэффициенты полинома Жегалкина
        coeffs = self._get_zhegalkin_coeffs()
        
        # Проверяем, что нет произведений переменных
        n = len(self.variables)
        for i in range(2 ** n):
            # Если в индексе больше одного бита, то это произведение
            if bin(i).count('1') > 1 and coeffs[i] == 1:
                return False
        return True
    
    def _get_zhegalkin_coeffs(self):
        """Получение коэффициентов полинома Жегалкина"""
        n = len(self.variables)
        coeffs = self.vector.copy()
        
        # Преобразование для получения коэффициентов
        size = 2 ** n
        for i in range(size):
            if coeffs[i] == 1:
                for j in range(i + 1, size):
                    if (j & i) == i:
                        coeffs[j] ^= coeffs[i]
        return coeffs
    
    def get_classes(self):
        """Возвращает словарь с принадлежностью ко всем классам"""
        return {
            'T0': self.is_t0(),
            'T1': self.is_t1(),
            'S': self.is_self_dual(),
            'M': self.is_monotone(),
            'L': self.is_linear()
        }