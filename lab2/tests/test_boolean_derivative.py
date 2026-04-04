import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boolean_parser import BooleanParser
from truth_table import TruthTable
from boolean_derivative import BooleanDerivative


class TestBooleanDerivative(unittest.TestCase):
    
    def setUp(self):
        self.parser = BooleanParser()
    
    def test_partial_derivative_and_by_a(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.partial_derivative('a')
        self.assertEqual(result, [0, 1])
    
    def test_partial_derivative_and_by_b(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.partial_derivative('b')
        self.assertEqual(result, [0, 1])
    
    def test_partial_derivative_xor_by_a(self):
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.partial_derivative('a')
        self.assertEqual(result, [1, 1])
    
    def test_partial_derivative_xor_by_b(self):
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.partial_derivative('b')
        self.assertEqual(result, [1, 1])
    
    def test_partial_derivative_or_by_a(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.partial_derivative('a')
        # ∂(a|b)/∂a = !b
        self.assertEqual(result, [1, 0])
    
    def test_partial_derivative_implies_by_a(self):
        variables, ast, eval_func = self.parser.parse("a->b")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.partial_derivative('a')
        # ∂(a->b)/∂a = !b
        self.assertEqual(result, [1, 0])
    
    def test_mixed_derivative_and(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.mixed_derivative(['a', 'b'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 1)
    
    def test_mixed_derivative_xor(self):
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.mixed_derivative(['a', 'b'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0)
    
    def test_mixed_derivative_3_vars(self):
        variables, ast, eval_func = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.mixed_derivative(['a', 'b'])
        self.assertEqual(len(result), 2)
    
    def test_mixed_derivative_all_3_vars(self):
        variables, ast, eval_func = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.mixed_derivative(['a', 'b', 'c'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 1)
    
    def test_get_derivative_table_2_vars(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        derivatives = derivative.get_derivative_table()
        self.assertIn('∂f/∂a', derivatives)
        self.assertIn('∂f/∂b', derivatives)
        self.assertIn('∂²f/∂a∂b', derivatives)
    
    def test_get_derivative_table_3_vars(self):
        variables, ast, eval_func = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        derivatives = derivative.get_derivative_table()
        self.assertIn('∂f/∂a', derivatives)
        self.assertIn('∂f/∂b', derivatives)
        self.assertIn('∂f/∂c', derivatives)
        self.assertIn('∂²f/∂a∂b', derivatives)
        self.assertIn('∂²f/∂a∂c', derivatives)
        self.assertIn('∂²f/∂b∂c', derivatives)
    
    def test_partial_derivative_4_vars(self):
        variables, ast, eval_func = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.partial_derivative('a')
        self.assertEqual(len(result), 8)
    
    def test_partial_derivative_5_vars(self):
        variables, ast, eval_func = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, eval_func)
        derivative = BooleanDerivative(tt)
        result = derivative.partial_derivative('a')
        self.assertEqual(len(result), 16)


if __name__ == '__main__':
    unittest.main()