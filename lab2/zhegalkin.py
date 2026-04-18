class ZhegalkinPolynomial:
    """
    Класс для построения полинома Жегалкина.
    Использует метод треугольника Паскаля или метод неопределенных коэффициентов.
    """
    
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.vector = truth_table.get_vector()
        self.coeffs = self._calculate_coeffs()
    
    def _calculate_coeffs(self):
        """
        Вычисление коэффициентов полинома Жегалкина.
        Использует преобразование для получения коэффициентов.
        """
        n = len(self.variables)
        size = 2 ** n
        coeffs = self.vector.copy()
        
        # метод треугольника Паскаля
        for i in range(size):
            for j in range(size):
                if (j & i) == i and i != j:
                    coeffs[j] ^= coeffs[i]
        
        return coeffs
    
    def get_polynomial(self):
        """
        Построение полинома Жегалкина.
        Формат: a0 ⊕ a1x1 ⊕ a2x2 ⊕ ... ⊕ a12x1x2 ⊕ ...
        """
        terms = []
        n = len(self.variables)
        
        for i in range(2 ** n):
            if self.coeffs[i] == 1:
                term = self._index_to_term(i)
                terms.append(term)
        
        if not terms:
            return "0"
        
        return " ⊕ ".join(terms)
    
    def _index_to_term(self, index):
        """Преобразует индекс в терм полинома"""
        if index == 0:
            return "1"
        
        n = len(self.variables)
        term_parts = []
        
        for j in range(n):
            if (index >> (n - 1 - j)) & 1:
                term_parts.append(self.variables[j])
        
        return "".join(term_parts)
