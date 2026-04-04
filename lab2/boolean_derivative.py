class BooleanDerivative:
    """Класс для вычисления булевой производной."""
    
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.vector = truth_table.get_vector()
        self.n = len(self.variables)
    
    def partial_derivative(self, var_name):
        """
        Вычисление частной производной по переменной.
        ∂f/∂xi = f(xi=0) ⊕ f(xi=1)
        """
        var_index = self.variables.index(var_name)
        result = []
        
        block_size = 2 ** (self.n - var_index - 1)
        
        for i in range(0, len(self.vector), 2 * block_size):
            for j in range(block_size):
                idx0 = i + j
                idx1 = i + block_size + j
                if idx1 < len(self.vector):
                    result.append(self.vector[idx0] ^ self.vector[idx1])
                else:
                    result.append(self.vector[idx0])
        
        return result
    
    def partial_derivative_as_function(self, var_name):
        """
        Вычисление частной производной и возврат в виде логической функции.
        """
        result_vector = self.partial_derivative(var_name)
        
        # Получаем остальные переменные (без var_name)
        other_vars = [v for v in self.variables if v != var_name]
        
        if not other_vars:
            return "1" if result_vector[0] == 1 else "0"
        
        # Строим СДНФ для производной
        terms = []
        n_other = len(other_vars)
        
        for i, val in enumerate(result_vector):
            if val == 1:
                term_parts = []
                for j, var in enumerate(other_vars):
                    bit = (i >> (n_other - 1 - j)) & 1
                    if bit == 0:
                        term_parts.append(f"!{var}")
                    else:
                        term_parts.append(var)
                terms.append("(" + "&".join(term_parts) + ")")
        
        if not terms:
            return "0"
        
        return "|".join(terms)
    
    def mixed_derivative(self, var_names):
        """
        Вычисление смешанной производной по нескольким переменным.
        """
        result = self.vector.copy()
        current_vars = self.variables.copy()
        
        for var_name in sorted(var_names):
            var_index = current_vars.index(var_name)
            new_result = []
            
            block_size = 2 ** (len(current_vars) - var_index - 1)
            
            for i in range(0, len(result), 2 * block_size):
                for j in range(block_size):
                    idx0 = i + j
                    idx1 = i + block_size + j
                    if idx1 < len(result):
                        new_result.append(result[idx0] ^ result[idx1])
                    else:
                        new_result.append(result[idx0])
            
            result = new_result
            current_vars.pop(var_index)
        
        return result
    
    def mixed_derivative_as_function(self, var_names):
        """
        Вычисление смешанной производной и возврат в виде логической функции.
        """
        result_vector = self.mixed_derivative(var_names)
        
        # Получаем оставшиеся переменные
        remaining_vars = [v for v in self.variables if v not in var_names]
        
        if not remaining_vars:
            return "1" if result_vector[0] == 1 else "0"
        
        # Строим СДНФ для производной
        terms = []
        n_remaining = len(remaining_vars)
        
        for i, val in enumerate(result_vector):
            if val == 1:
                term_parts = []
                for j, var in enumerate(remaining_vars):
                    bit = (i >> (n_remaining - 1 - j)) & 1
                    if bit == 0:
                        term_parts.append(f"!{var}")
                    else:
                        term_parts.append(var)
                terms.append("(" + "&".join(term_parts) + ")")
        
        if not terms:
            return "0"
        
        return "|".join(terms)
    
    def get_derivative_table(self):
        """Получение таблицы всех частных и смешанных производных."""
        derivatives = {}
        
        # Частные производные
        for var in self.variables:
            key = f"∂f/∂{var}"
            vector = self.partial_derivative(var)
            func = self.partial_derivative_as_function(var)
            derivatives[key] = {
                'vector': vector,
                'function': func
            }
        
        # Смешанные производные для 2 переменных
        if len(self.variables) >= 2:
            for i, var1 in enumerate(self.variables):
                for var2 in self.variables[i+1:]:
                    key = f"∂²f/∂{var1}∂{var2}"
                    vector = self.mixed_derivative([var1, var2])
                    func = self.mixed_derivative_as_function([var1, var2])
                    derivatives[key] = {
                        'vector': vector,
                        'function': func
                    }
        
        return derivatives