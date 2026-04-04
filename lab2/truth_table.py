from typing import List, Dict, Any, Tuple
from boolean_parser import ASTNode


class TruthTable:
    """Класс для построения полной таблицы истинности"""
    
    def __init__(self, variables: List[str], ast: ASTNode, eval_func: callable):
        self.variables = variables
        self.ast = ast
        self.eval_func = eval_func
        self.truth_table: List[Dict[str, Any]] = []
        self.subexpression_names: List[str] = []
        self._build()
    
    def _build(self):
        """Строит полную таблицу истинности со всеми подвыражениями"""
        n = len(self.variables)
        self.truth_table = []
        
        # Собираем все возможные наборы
        for i in range(2 ** n):
            # Создаем набор значений для переменных
            values = {}
            for j, var in enumerate(self.variables):
                values[var] = bool((i >> (n - 1 - j)) & 1)
            
            # Вычисляем все подвыражения
            subresults = self._evaluate_subexpressions(values)
            
            # Сохраняем строку таблицы
            row = {
                'values': values.copy(),
                'subresults': subresults
            }
            self.truth_table.append(row)
            
            # Сохраняем имена подвыражений для заголовка
            if not self.subexpression_names:
                # Получаем все ключи, кроме переменных
                self.subexpression_names = [k for k in subresults.keys() 
                                           if k not in self.variables]
    
    def _evaluate_subexpressions(self, values: Dict[str, bool]) -> Dict[str, bool]:
        """Вычисляет все подвыражения в AST"""
        results = {}
        # Сначала добавляем значения переменных
        for var in self.variables:
            results[var] = values[var]
        
        # Вычисляем выражение рекурсивно
        self._collect_subexpr(self.ast, values, results)
        return results
    
    def _get_expr_name(self, node: ASTNode) -> str:
        """Генерирует читаемое имя для подвыражения"""
        if node.type == 'var':
            return node.value
        elif node.type == 'not':
            return f'¬{self._get_expr_name(node.left)}'
        elif node.type == 'and':
            return f'({self._get_expr_name(node.left)} ∧ {self._get_expr_name(node.right)})'
        elif node.type == 'or':
            return f'({self._get_expr_name(node.left)} ∨ {self._get_expr_name(node.right)})'
        elif node.type == 'implies':
            return f'({self._get_expr_name(node.left)} → {self._get_expr_name(node.right)})'
        elif node.type == 'equiv':
            return f'({self._get_expr_name(node.left)} ~ {self._get_expr_name(node.right)})'
        return "?"
    
    def _collect_subexpr(self, node: ASTNode, values: Dict[str, bool], 
                         results: Dict[str, bool]) -> bool:
        """
        Рекурсивно собирает результаты подвыражений.
        Возвращает значение текущего узла.
        """
        if node.type == 'var':
            val = values[node.value]
            results[node.value] = val
            return val
        
        elif node.type == 'not':
            left_val = self._collect_subexpr(node.left, values, results)
            result = not left_val
            expr_name = self._get_expr_name(node)
            results[expr_name] = result
            return result
        
        elif node.type == 'and':
            left_val = self._collect_subexpr(node.left, values, results)
            right_val = self._collect_subexpr(node.right, values, results)
            result = left_val and right_val
            expr_name = self._get_expr_name(node)
            results[expr_name] = result
            return result
        
        elif node.type == 'or':
            left_val = self._collect_subexpr(node.left, values, results)
            right_val = self._collect_subexpr(node.right, values, results)
            result = left_val or right_val
            expr_name = self._get_expr_name(node)
            results[expr_name] = result
            return result
        
        elif node.type == 'implies':
            left_val = self._collect_subexpr(node.left, values, results)
            right_val = self._collect_subexpr(node.right, values, results)
            result = (not left_val) or right_val
            expr_name = self._get_expr_name(node)
            results[expr_name] = result
            return result
        
        elif node.type == 'equiv':
            left_val = self._collect_subexpr(node.left, values, results)
            right_val = self._collect_subexpr(node.right, values, results)
            result = (left_val == right_val)
            expr_name = self._get_expr_name(node)
            results[expr_name] = result
            return result
        
        return False
    
    def get_on_sets(self) -> List[Dict[str, bool]]:
        """Возвращает наборы, на которых функция равна 1"""
        return [row['values'] for row in self.truth_table 
                if row['subresults'].get(self._get_expr_name(self.ast), False)]
    
    def get_off_sets(self) -> List[Dict[str, bool]]:
        """Возвращает наборы, на которых функция равна 0"""
        return [row['values'] for row in self.truth_table 
                if not row['subresults'].get(self._get_expr_name(self.ast), False)]
    
    def get_vector(self) -> List[int]:
        """Возвращает вектор значений функции"""
        expr_name = self._get_expr_name(self.ast)
        return [1 if row['subresults'].get(expr_name, False) else 0 
                for row in self.truth_table]
    
    def print_table(self):
        """Выводит красивую таблицу истинности"""
        if not self.truth_table:
            print("Таблица истинности пуста")
            return
        
        # Заголовки: переменные + все подвыражения (кроме переменных)
        headers = self.variables + self.subexpression_names
        
        if len(headers) <= len(self.variables):
            # Если нет подвыражений, просто выводим переменные и результат
            headers = self.variables + [self._get_expr_name(self.ast)]
        
        # Вычисляем ширину каждого столбца
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(str(header))
            
            # Проверяем значения в этом столбце
            if i < len(self.variables):
                # Столбец переменной
                for row in self.truth_table:
                    val = int(row['values'][header])
                    max_width = max(max_width, len(str(val)))
            else:
                # Столбец подвыражения
                subexpr_name = headers[i]
                for row in self.truth_table:
                    val = 1 if row['subresults'].get(subexpr_name, False) else 0
                    max_width = max(max_width, len(str(val)))
            
            col_widths.append(min(max_width + 2, 30))  # Ограничиваем ширину
        
        # Разделительная линия
        separator = '+' + '+'.join(['-' * w for w in col_widths]) + '+'
        
        # Печатаем заголовки
        print(separator)
        header_line = '|'
        for i, header in enumerate(headers):
            header_str = str(header)
            if len(header_str) > col_widths[i] - 2:
                header_str = header_str[:col_widths[i] - 5] + "..."
            header_line += f' {header_str:^{col_widths[i]-2}} |'
        print(header_line)
        print(separator)
        
        # Печатаем строки
        for row in self.truth_table:
            line = '|'
            
            # Значения переменных
            for i, var in enumerate(self.variables):
                val = int(row['values'][var])
                line += f' {val:^{col_widths[i]-2}} |'
            
            # Значения подвыражений
            for i in range(len(self.variables), len(headers)):
                subexpr_name = headers[i]
                val = 1 if row['subresults'].get(subexpr_name, False) else 0
                line += f' {val:^{col_widths[i]-2}} |'
            
            print(line)
        
        print(separator)