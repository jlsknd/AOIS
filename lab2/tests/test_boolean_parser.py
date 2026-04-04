import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boolean_parser import BooleanParser, ASTNode


class TestBooleanParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = BooleanParser()
    
    def test_parse_single_variable(self):
        variables, ast, _ = self.parser.parse("a")
        self.assertEqual(variables, ['a'])
        self.assertEqual(ast.type, 'var')
        self.assertEqual(ast.value, 'a')
    
    def test_parse_not_operation(self):
        variables, ast, _ = self.parser.parse("!a")
        self.assertEqual(variables, ['a'])
        self.assertEqual(ast.type, 'not')
        self.assertEqual(ast.left.type, 'var')
        self.assertEqual(ast.left.value, 'a')
    
    def test_parse_and_operation(self):
        variables, ast, _ = self.parser.parse("a&b")
        self.assertEqual(variables, ['a', 'b'])
        self.assertEqual(ast.type, 'and')
        self.assertEqual(ast.left.type, 'var')
        self.assertEqual(ast.left.value, 'a')
        self.assertEqual(ast.right.type, 'var')
        self.assertEqual(ast.right.value, 'b')
    
    def test_parse_or_operation(self):
        variables, ast, _ = self.parser.parse("a|b")
        self.assertEqual(variables, ['a', 'b'])
        self.assertEqual(ast.type, 'or')
        self.assertEqual(ast.left.value, 'a')
        self.assertEqual(ast.right.value, 'b')
    
    def test_parse_implication(self):
        variables, ast, _ = self.parser.parse("a->b")
        self.assertEqual(variables, ['a', 'b'])
        self.assertEqual(ast.type, 'implies')
    
    def test_parse_equivalence(self):
        variables, ast, _ = self.parser.parse("a~b")
        self.assertEqual(variables, ['a', 'b'])
        self.assertEqual(ast.type, 'equiv')
    
    def test_parse_complex_expression(self):
        variables, ast, _ = self.parser.parse("!(!a->!b)|c")
        self.assertEqual(variables, ['a', 'b', 'c'])
        self.assertEqual(ast.type, 'or')
    
    def test_parse_with_parentheses(self):
        variables, ast, _ = self.parser.parse("(a&b)|c")
        self.assertEqual(variables, ['a', 'b', 'c'])
        self.assertEqual(ast.type, 'or')
        self.assertEqual(ast.left.type, 'and')
    
    def test_parse_all_variables(self):
        variables, ast, _ = self.parser.parse("a&b&c&d&e")
        self.assertEqual(variables, ['a', 'b', 'c', 'd', 'e'])
    
    def test_eval_single_variable_true(self):
        _, _, eval_func = self.parser.parse("a")
        result = eval_func({'a': True})
        self.assertTrue(result)
    
    def test_eval_single_variable_false(self):
        _, _, eval_func = self.parser.parse("a")
        result = eval_func({'a': False})
        self.assertFalse(result)
    
    def test_eval_not_operation(self):
        _, _, eval_func = self.parser.parse("!a")
        self.assertTrue(eval_func({'a': False}))
        self.assertFalse(eval_func({'a': True}))
    
    def test_eval_and_operation(self):
        _, _, eval_func = self.parser.parse("a&b")
        self.assertTrue(eval_func({'a': True, 'b': True}))
        self.assertFalse(eval_func({'a': True, 'b': False}))
        self.assertFalse(eval_func({'a': False, 'b': True}))
        self.assertFalse(eval_func({'a': False, 'b': False}))
    
    def test_eval_or_operation(self):
        _, _, eval_func = self.parser.parse("a|b")
        self.assertTrue(eval_func({'a': True, 'b': True}))
        self.assertTrue(eval_func({'a': True, 'b': False}))
        self.assertTrue(eval_func({'a': False, 'b': True}))
        self.assertFalse(eval_func({'a': False, 'b': False}))
    
    def test_eval_implication(self):
        _, _, eval_func = self.parser.parse("a->b")
        self.assertTrue(eval_func({'a': False, 'b': False}))
        self.assertTrue(eval_func({'a': False, 'b': True}))
        self.assertFalse(eval_func({'a': True, 'b': False}))
        self.assertTrue(eval_func({'a': True, 'b': True}))
    
    def test_eval_equivalence(self):
        _, _, eval_func = self.parser.parse("a~b")
        self.assertTrue(eval_func({'a': True, 'b': True}))
        self.assertFalse(eval_func({'a': True, 'b': False}))
        self.assertFalse(eval_func({'a': False, 'b': True}))
        self.assertTrue(eval_func({'a': False, 'b': False}))
    
    def test_eval_complex_expression(self):
        _, _, eval_func = self.parser.parse("!(!a->!b)|c")
        self.assertFalse(eval_func({'a': False, 'b': False, 'c': False}))
        self.assertTrue(eval_func({'a': False, 'b': False, 'c': True}))
        self.assertTrue(eval_func({'a': False, 'b': True, 'c': False}))
    
    def test_parse_only_ast_method(self):
        ast = self.parser.parse_only_ast("a&b")
        self.assertEqual(ast.type, 'and')
    
    def test_parse_invalid_expression(self):
        with self.assertRaises(ValueError):
            self.parser.parse("a&")
    
    def test_parse_expression_with_spaces(self):
        variables, ast, _ = self.parser.parse(" a & b ")
        self.assertEqual(variables, ['a', 'b'])
    
    def test_extract_variables_multiple(self):
        _, ast, _ = self.parser.parse("a&b|c&d")
        self.assertEqual(self.parser.variables, ['a', 'b', 'c', 'd'])
    
    def test_ast_node_equality(self):
        node1 = ASTNode('var', value='a')
        node2 = ASTNode('var', value='a')
        node3 = ASTNode('var', value='b')
        
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, "not a node")
    
    def test_ast_node_repr(self):
        var_node = ASTNode('var', value='a')
        self.assertEqual(repr(var_node), 'a')
        
        not_node = ASTNode('not', left=var_node)
        self.assertEqual(repr(not_node), '!a')
        
        and_node = ASTNode('and', left=var_node, right=ASTNode('var', value='b'))
        self.assertEqual(repr(and_node), '(a & b)')


if __name__ == '__main__':
    unittest.main()