import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boolean_parser import BooleanParser
from truth_table import TruthTable


class TestTruthTable(unittest.TestCase):
    
    def setUp(self):
        self.parser = BooleanParser()
    
    def test_truth_table_2_variables(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        
        self.assertEqual(len(tt.truth_table), 4)
        self.assertEqual(tt.get_vector(), [0, 0, 0, 1])
    
    def test_truth_table_3_variables(self):
        variables, ast, eval_func = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, eval_func)
        
        self.assertEqual(len(tt.truth_table), 8)
        self.assertEqual(tt.get_vector(), [0, 0, 0, 0, 0, 0, 0, 1])
    
    def test_truth_table_4_variables(self):
        variables, ast, eval_func = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, eval_func)
        self.assertEqual(len(tt.truth_table), 16)
    
    def test_truth_table_5_variables(self):
        variables, ast, eval_func = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, eval_func)
        self.assertEqual(len(tt.truth_table), 32)
    
    def test_get_on_sets(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        self.assertEqual(len(tt.get_on_sets()), 3)
    
    def test_get_off_sets(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        self.assertEqual(len(tt.get_off_sets()), 1)
    
    def test_get_vector(self):
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        self.assertEqual(tt.get_vector(), [0, 1, 1, 0])
    
    def test_implication_table(self):
        variables, ast, eval_func = self.parser.parse("a->b")
        tt = TruthTable(variables, ast, eval_func)
        self.assertEqual(tt.get_vector(), [1, 1, 0, 1])
    
    def test_constant_false(self):
        variables, ast, eval_func = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, eval_func)
        self.assertEqual(tt.get_vector(), [0, 0])
    
    def test_constant_true(self):
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        self.assertEqual(tt.get_vector(), [1, 1])
    
    def test_print_table_does_not_crash(self):
        """Просто проверяем, что print_table не падает"""
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        try:
            tt.print_table()
        finally:
            sys.stdout = sys.__stdout__
        self.assertTrue(len(captured.getvalue()) > 0)


if __name__ == '__main__':
    unittest.main()