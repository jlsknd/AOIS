class DummyVariablesFinder:
    """
    Класс для поиска фиктивных переменных.
    Переменная фиктивна, если значение функции не зависит от ее значения.
    """
    
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.vector = truth_table.get_vector()
        self.n = len(self.variables)
    
    def find_dummy_variables(self):
        """
        Поиск фиктивных переменных.
        Для каждой переменной проверяем, меняется ли значение функции при изменении этой переменной.
        """
        dummy_vars = []
        
        for i, var in enumerate(self.variables):
            if self._is_dummy(i):
                dummy_vars.append(var)
        
        return dummy_vars
    
    def _is_dummy(self, var_index):
        """
        Проверка, является ли переменная фиктивной.
        Для всех наборов: f(..., xi=0, ...) == f(..., xi=1, ...)
        """
        size = 2 ** self.n
        
        for i in range(0, size, 2 ** (self.n - var_index)):
            for j in range(2 ** (self.n - var_index - 1)):
                idx0 = i + j
                idx1 = idx0 + 2 ** (self.n - var_index - 1)
                
                if self.vector[idx0] != self.vector[idx1]:
                    return False
        
        return True