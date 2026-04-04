import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boolean_parser import BooleanParser
from truth_table import TruthTable
from post_classes import PostClasses


class TestPostClasses(unittest.TestCase):
    
    def setUp(self):
        self.parser = BooleanParser()
    
    def test_t0_and_function(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_t0())
    
    def test_t0_or_function(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_t0())
    
    def test_t0_not_function(self):
        variables, ast, eval_func = self.parser.parse("!a")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_t0())
    
    def test_t1_and_function(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_t1())
    
    def test_t1_or_function(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_t1())
    
    def test_t1_not_function(self):
        variables, ast, eval_func = self.parser.parse("!a")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_t1())
    
    def test_self_dual_not_function(self):
        variables, ast, eval_func = self.parser.parse("!a")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_self_dual())
    
    def test_self_dual_and_function(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_self_dual())
    
    def test_self_dual_xor_function(self):
        """Тест самодвойственности XOR"""
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_self_dual())
    
    def test_self_dual_implication_function(self):
        """Тест самодвойственности импликации"""
        variables, ast, eval_func = self.parser.parse("a->b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_self_dual())
    
    def test_monotone_and_function(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_monotone())
    
    def test_monotone_or_function(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_monotone())
    
    def test_monotone_not_function(self):
        variables, ast, eval_func = self.parser.parse("!a")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_monotone())
    
    def test_monotone_constant_function(self):
        """Тест монотонности константной функции"""
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_monotone())
    
    def test_linear_xor_function(self):
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_linear())
    
    def test_linear_and_function(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_linear())
    
    def test_linear_or_function(self):
        """Тест линейности OR"""
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_linear())
    
    def test_linear_implication_function(self):
        """Тест линейности импликации"""
        variables, ast, eval_func = self.parser.parse("a->b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_linear())
    
    def test_linear_constant_function(self):
        """Тест линейности константной функции"""
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertTrue(post.is_linear())
    
    def test_get_classes_method(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        classes = post.get_classes()
        self.assertIn('T0', classes)
        self.assertIn('T1', classes)
        self.assertIn('S', classes)
        self.assertIn('M', classes)
        self.assertIn('L', classes)
    
    def test_is_less_or_equal_method(self):
        """Тест метода _is_less_or_equal"""
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        # 2 (10) <= 3 (11) должно быть True
        self.assertTrue(post._is_less_or_equal(2, 3, 2))
        # 3 (11) <= 2 (10) должно быть False
        self.assertFalse(post._is_less_or_equal(3, 2, 2))
        # 1 (01) <= 1 (01) должно быть True
        self.assertTrue(post._is_less_or_equal(1, 1, 2))
    
    def test_get_zhegalkin_coeffs_method(self):
        """Тест метода _get_zhegalkin_coeffs"""
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        coeffs = post._get_zhegalkin_coeffs()
        self.assertEqual(len(coeffs), 4)
    
    def test_t0_false_function(self):
        """Тест функции, не сохраняющей 0"""
        variables, ast, eval_func = self.parser.parse("!a")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_t0())
    
    def test_t1_false_function(self):
        """Тест функции, не сохраняющей 1"""
        variables, ast, eval_func = self.parser.parse("!a")
        tt = TruthTable(variables, ast, eval_func)
        post = PostClasses(tt)
        self.assertFalse(post.is_t1())


if __name__ == '__main__':
    unittest.main()