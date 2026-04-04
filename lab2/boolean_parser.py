import re
from typing import List, Dict, Any, Set, Tuple, Optional


class ASTNode:
    """Узел абстрактного синтаксического дерева"""
    def __init__(self, node_type: str, value: str = None, left: 'ASTNode' = None, right: 'ASTNode' = None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right
    
    def __repr__(self):
        if self.type == 'var':
            return self.value
        elif self.type == 'not':
            return f'!{self.left}'
        elif self.type == 'and':
            return f'({self.left} & {self.right})'
        elif self.type == 'or':
            return f'({self.left} | {self.right})'
        elif self.type == 'implies':
            return f'({self.left} -> {self.right})'
        elif self.type == 'equiv':
            return f'({self.left} ~ {self.right})'
        return str(self.value)
    
    def __eq__(self, other):
        if not isinstance(other, ASTNode):
            return False
        return (self.type == other.type and 
                self.value == other.value and
                self.left == other.left and
                self.right == other.right)


class BooleanParser:
    """Парсер логических выражений"""
    
    def __init__(self):
        self.variables: List[str] = []
        self.expression: str = ""
        self.tokens: List[str] = []
        self.pos: int = 0
    
    def parse(self, expression: str) -> Tuple[List[str], ASTNode, callable]:
        """Парсит выражение и возвращает переменные, AST и функцию вычисления"""
        self.expression = expression
        self.variables = sorted(list(set(re.findall(r'[a-e]', expression))))
        
        self._tokenize()
        self.pos = 0
        ast = self._parse_expression()
        eval_func = self._create_evaluator(ast)
        
        return self.variables, ast, eval_func
    
    def parse_only_ast(self, expression: str) -> ASTNode:
        """Только парсинг в AST (для тестов)"""
        self.expression = expression
        self.variables = sorted(list(set(re.findall(r'[a-e]', expression))))
        self._tokenize()
        self.pos = 0
        return self._parse_expression()
    
    def _tokenize(self):
        """Разбивает выражение на токены"""
        expr = self.expression.replace(' ', '')
        expr = expr.replace('->', '→')
        expr = expr.replace('~', '≡')
        
        tokens = []
        i = 0
        while i < len(expr):
            char = expr[i]
            if char in '()!&|→≡':
                tokens.append(char)
                i += 1
            elif char.isalpha() and char in 'abcde':
                tokens.append(char)
                i += 1
            else:
                i += 1
        
        self.tokens = tokens
    
    def _parse_expression(self) -> ASTNode:
        return self._parse_implication()
    
    def _parse_implication(self) -> ASTNode:
        node = self._parse_equivalence()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '→':
            self.pos += 1
            right = self._parse_equivalence()
            node = ASTNode('implies', left=node, right=right)
        return node
    
    def _parse_equivalence(self) -> ASTNode:
        node = self._parse_or()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '≡':
            self.pos += 1
            right = self._parse_or()
            node = ASTNode('equiv', left=node, right=right)
        return node
    
    def _parse_or(self) -> ASTNode:
        node = self._parse_and()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '|':
            self.pos += 1
            right = self._parse_and()
            node = ASTNode('or', left=node, right=right)
        return node
    
    def _parse_and(self) -> ASTNode:
        node = self._parse_not()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '&':
            self.pos += 1
            right = self._parse_not()
            node = ASTNode('and', left=node, right=right)
        return node
    
    def _parse_not(self) -> ASTNode:
        if self.pos < len(self.tokens) and self.tokens[self.pos] == '!':
            self.pos += 1
            node = self._parse_atom()
            return ASTNode('not', left=node)
        return self._parse_atom()
    
    def _parse_atom(self) -> ASTNode:
        if self.pos >= len(self.tokens):
            raise ValueError("Неожиданный конец выражения")
        
        token = self.tokens[self.pos]
        
        if token == '(':
            self.pos += 1
            node = self._parse_expression()
            if self.pos < len(self.tokens) and self.tokens[self.pos] == ')':
                self.pos += 1
                return node
            raise ValueError("Ожидалась закрывающая скобка")
        
        elif token in 'abcde':
            self.pos += 1
            return ASTNode('var', value=token)
        
        raise ValueError(f"Неожиданный токен: {token}")
    
    def _create_evaluator(self, node: ASTNode) -> callable:
        def evaluate(values: Dict[str, bool]) -> bool:
            return self._eval_node(node, values)
        return evaluate
    
    def _eval_node(self, node: ASTNode, values: Dict[str, bool]) -> bool:
        if node.type == 'var':
            return values.get(node.value, False)
        elif node.type == 'not':
            return not self._eval_node(node.left, values)
        elif node.type == 'and':
            return self._eval_node(node.left, values) and self._eval_node(node.right, values)
        elif node.type == 'or':
            return self._eval_node(node.left, values) or self._eval_node(node.right, values)
        elif node.type == 'implies':
            left_val = self._eval_node(node.left, values)
            right_val = self._eval_node(node.right, values)
            return (not left_val) or right_val
        elif node.type == 'equiv':
            return self._eval_node(node.left, values) == self._eval_node(node.right, values)
        return False
    
    def evaluate_with_subexpressions(self, node: ASTNode, values: Dict[str, bool]) -> Dict[str, bool]:
        results = {}
        self._collect_subexpressions(node, values, results, "F")
        return results
    
    def _collect_subexpressions(self, node: ASTNode, values: Dict[str, bool], 
                                 results: Dict[str, bool], name: str):
        results[name] = self._eval_node(node, values)
        
        if node.type == 'not':
            self._collect_subexpressions(node.left, values, results, f'!{name[:-1] if name != "F" else "A"}')
        elif node.type in ('and', 'or', 'implies', 'equiv'):
            left_name = f'{name}_L' if name != "F" else "A"
            right_name = f'{name}_R' if name != "F" else "B"
            self._collect_subexpressions(node.left, values, results, left_name)
            self._collect_subexpressions(node.right, values, results, right_name)