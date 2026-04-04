import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boolean_parser import BooleanParser
from truth_table import TruthTable
from zhegalkin import ZhegalkinPolynomial


class TestZhegalkinPolynomial(unittest.TestCase):
    
    def setUp(self):
        self.parser = BooleanParser()
    
    def test_zhegalkin_and_2_variables(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        zhegalkin = ZhegalkinPolynomial(tt)
        
        polynomial = zhegalkin.get_polynomial()
        self.assertEqual(polynomial, "ab")
    
    def test_zhegalkin_or_2_variables(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        zhegalkin = ZhegalkinPolynomial(tt)
        
        polynomial = zhegalkin.get_polynomial()
        terms = polynomial.split(" ⊕ ")
        self.assertEqual(len(terms), 3)
        self.assertIn("a", terms)
        self.assertIn("b", terms)
        self.assertIn("ab", terms)
    
    def test_zhegalkin_xor(self):
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        zhegalkin = ZhegalkinPolynomial(tt)
        
        polynomial = zhegalkin.get_polynomial()
        terms = polynomial.split(" ⊕ ")
        self.assertEqual(len(terms), 2)
        self.assertIn("a", terms)
        self.assertIn("b", terms)
    
    def test_zhegalkin_constant_true(self):
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        zhegalkin = ZhegalkinPolynomial(tt)
        
        polynomial = zhegalkin.get_polynomial()
        self.assertEqual(polynomial, "1")
    
    def test_zhegalkin_constant_false(self):
        variables, ast, eval_func = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, eval_func)
        zhegalkin = ZhegalkinPolynomial(tt)
        
        polynomial = zhegalkin.get_polynomial()
        self.assertEqual(polynomial, "0")
    
    def test_zhegalkin_implication(self):
        variables, ast, eval_func = self.parser.parse("a->b")
        tt = TruthTable(variables, ast, eval_func)
        zhegalkin = ZhegalkinPolynomial(tt)
        
        polynomial = zhegalkin.get_polynomial()
        terms = polynomial.split(" ⊕ ")
        self.assertIn("1", terms)
        self.assertIn("a", terms)
        self.assertIn("ab", terms)
    
    def test_zhegalkin_3_variables(self):
        variables, ast, eval_func = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, eval_func)
        zhegalkin = ZhegalkinPolynomial(tt)
        
        polynomial = zhegalkin.get_polynomial()
        self.assertEqual(polynomial, "abc")


if __name__ == '__main__':
    unittest.main()