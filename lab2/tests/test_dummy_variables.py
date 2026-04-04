import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boolean_parser import BooleanParser
from truth_table import TruthTable
from dummy_variables import DummyVariablesFinder


class TestDummyVariables(unittest.TestCase):
    
    def setUp(self):
        self.parser = BooleanParser()
    
    def test_no_dummy_variables_and(self):
        """Тест AND: нет фиктивных переменных"""
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertEqual(dummy_vars, [])
    
    def test_dummy_variable_in_and_with_constant(self):
        """Тест: фиктивная переменная в AND с константой"""
        variables, ast, eval_func = self.parser.parse("a&(b|!b)")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertIn('b', dummy_vars)
    
    def test_function_only_one_variable(self):
        """Тест функции с одной переменной - нет фиктивных"""
        variables, ast, eval_func = self.parser.parse("a")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertEqual(dummy_vars, [])
    
    def test_constant_function_all_dummy(self):
        """Тест константной функции - все переменные фиктивные"""
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertEqual(set(dummy_vars), {'a'})
    
    def test_xor_no_dummy(self):
        """Тест XOR: нет фиктивных переменных"""
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertEqual(dummy_vars, [])
    
    def test_dummy_in_3_vars(self):
        """Тест фиктивной переменной в 3-переменной функции"""
        # Функция зависит только от a и b, c - фиктивная
        variables, ast, eval_func = self.parser.parse("a&b&(c|!c)")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertIn('c', dummy_vars)
    
    def test_dummy_in_4_vars(self):
        """Тест фиктивной переменной в 4-переменной функции"""
        # Функция зависит только от a и b, c и d - фиктивные
        variables, ast, eval_func = self.parser.parse("a&b&(c|!c)&(d|!d)")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertIn('c', dummy_vars)
        self.assertIn('d', dummy_vars)
    
    def test_dummy_in_5_vars(self):
        """Тест фиктивной переменной в 5-переменной функции"""
        # Функция зависит только от a и b, c, d, e - фиктивные
        variables, ast, eval_func = self.parser.parse("a&b&(c|!c)&(d|!d)&(e|!e)")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertIn('c', dummy_vars)
        self.assertIn('d', dummy_vars)
        self.assertIn('e', dummy_vars)
    
    def test_dummy_in_constant_2_vars(self):
        """Тест константной функции с 2 переменными"""
        variables, ast, eval_func = self.parser.parse("(a|!a)&(b|!b)")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertEqual(set(dummy_vars), {'a', 'b'})
    
    def test_no_dummy_in_complex(self):
        """Тест сложной функции без фиктивных переменных"""
        variables, ast, eval_func = self.parser.parse("(a&b)|(c&d)")
        tt = TruthTable(variables, ast, eval_func)
        finder = DummyVariablesFinder(tt)
        dummy_vars = finder.find_dummy_variables()
        self.assertEqual(dummy_vars, [])


if __name__ == '__main__':
    unittest.main()