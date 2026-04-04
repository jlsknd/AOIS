class NormalForms:
    """
    Класс для построения совершенных нормальных форм.
    СДНФ: дизъюнкция конституэнт единицы
    СКНФ: конъюнкция конституэнт нуля
    """
    
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.on_sets = truth_table.get_on_sets()
        self.off_sets = truth_table.get_off_sets()
    
    def get_sdnf(self):
        """
        Построение СДНФ.
        Конституэнта единицы: конъюнкция переменных (прямых или с отрицанием)
        """
        if not self.on_sets:
            return "0"
        
        terms = []
        for assignment in self.on_sets:
            term = []
            for var in self.variables:
                if assignment[var]:
                    term.append(var)
                else:
                    term.append(f'!{var}')
            terms.append('(' + '&'.join(term) + ')')
        
        return '|'.join(terms)
    
    def get_sknf(self):
        """
        Построение СКНФ.
        Конституэнта нуля: дизъюнкция переменных (прямых или с отрицанием)
        """
        if not self.off_sets:
            return "1"
        
        terms = []
        for assignment in self.off_sets:
            term = []
            for var in self.variables:
                if assignment[var]:
                    term.append(f'!{var}')
                else:
                    term.append(var)
            terms.append('(' + '|'.join(term) + ')')
        
        return '&'.join(terms)
    
    def get_numeric_form_sdnf(self):
        """
        Числовая форма СДНФ.
        Представляет наборы, на которых функция равна 1, в виде десятичных чисел.
        """
        numeric_form = []
        n = len(self.variables)
        
        for assignment in self.on_sets:
            bits = [1 if assignment[var] else 0 for var in self.variables]
            value = 0
            for bit in bits:
                value = (value << 1) | bit
            numeric_form.append(value)
        
        return sorted(numeric_form)
    
    def get_numeric_form_sknf(self):
        """
        Числовая форма СКНФ.
        Представляет наборы, на которых функция равна 0, в виде десятичных чисел.
        """
        numeric_form = []
        n = len(self.variables)
        
        for assignment in self.off_sets:
            bits = [1 if assignment[var] else 0 for var in self.variables]
            value = 0
            for bit in bits:
                value = (value << 1) | bit
            numeric_form.append(value)
        
        return sorted(numeric_form)
    
    def get_index_form(self):
        """
        Индексная форма функции.
        Представляет вектор значений в двоичном виде как десятичное число.
        """
        vector = self.truth_table.get_vector()
        # Преобразуем список битов в двоичное число
        result = 0
        for bit in vector:
            result = (result << 1) | bit
        return result