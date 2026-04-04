import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boolean_parser import BooleanParser
from truth_table import TruthTable
from minimization import Minimization


class TestMinimization(unittest.TestCase):
    
    def setUp(self):
        self.parser = BooleanParser()
    
    def test_minimization_calculated_and(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, _ = minimizer.minimization_calculated()
        self.assertEqual(result, "a&b")
    
    def test_minimization_calculated_or(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, _ = minimizer.minimization_calculated()
        self.assertIn("a", result)
        self.assertIn("b", result)
    
    def test_minimization_calculated_constant_false(self):
        variables, ast, eval_func = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, _ = minimizer.minimization_calculated()
        self.assertEqual(result, "0")
    
    def test_minimization_calculated_constant_true(self):
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, _ = minimizer.minimization_calculated()
        self.assertEqual(result, "1")
    
    def test_minimization_calculated_3_vars(self):
        variables, ast, eval_func = self.parser.parse("(a&b)|(a&c)|(b&c)")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, _ = minimizer.minimization_calculated()
        self.assertIsNotNone(result)
    
    def test_minimization_table_and(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, _, _ = minimizer.minimization_table()
        self.assertEqual(result, "a&b")
    
    def test_minimization_table_constant_false(self):
        variables, ast, eval_func = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, _, _ = minimizer.minimization_table()
        self.assertEqual(result, "0")
    
    def test_minimization_table_constant_true(self):
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, _, _ = minimizer.minimization_table()
        self.assertEqual(result, "1")
    
    def test_minimization_karnaugh_2_vars(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, k_map = minimizer.minimization_karnaugh()
        self.assertIsNotNone(result)
        self.assertIsNotNone(k_map)
    
    def test_minimization_karnaugh_2_vars_all_ones(self):
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, k_map = minimizer.minimization_karnaugh()
        self.assertIsNotNone(result)
    
    def test_minimization_karnaugh_3_vars(self):
        variables, ast, eval_func = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, k_map = minimizer.minimization_karnaugh()
        self.assertEqual(len(k_map), 2)
        self.assertEqual(len(k_map[0]), 4)
    
    def test_minimization_karnaugh_3_vars_all_ones(self):
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, k_map = minimizer.minimization_karnaugh()
        self.assertIsNotNone(result)
    
    def test_minimization_karnaugh_4_vars(self):
        variables, ast, eval_func = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, k_map = minimizer.minimization_karnaugh()
        self.assertEqual(len(k_map), 4)
        self.assertEqual(len(k_map[0]), 4)
    
    def test_minimization_karnaugh_4_vars_all_ones(self):
        variables, ast, eval_func = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, k_map = minimizer.minimization_karnaugh()
        self.assertIsNotNone(result)
    
    def test_minimization_karnaugh_5_vars_not_supported(self):
        variables, ast, eval_func = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result, k_map = minimizer.minimization_karnaugh()
        self.assertEqual(result, "Метод Карно поддерживается для 2-4 переменных")
    
    def test_assignment_to_binary(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        assignment = {'a': True, 'b': False}
        result = minimizer._assignment_to_binary(assignment)
        self.assertEqual(result, "10")
        
        assignment = {'a': False, 'b': True}
        result = minimizer._assignment_to_binary(assignment)
        self.assertEqual(result, "01")
    
    def test_binary_to_term(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result = minimizer._binary_to_term("10")
        self.assertIsNotNone(result)
        
        result = minimizer._binary_to_term("1X")
        self.assertIsNotNone(result)
    
    def test_implicant_to_term(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result = minimizer._implicant_to_term("1X")
        self.assertEqual(result, "a")
        
        result = minimizer._implicant_to_term("X1")
        self.assertEqual(result, "b")
        
        result = minimizer._implicant_to_term("XX")
        self.assertEqual(result, "1")
        
        result = minimizer._implicant_to_term("0X")
        self.assertEqual(result, "!a")
    
    def test_implicant_to_display(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        # Просто проверяем, что метод возвращает строку
        result = minimizer._implicant_to_display("1X")
        self.assertIsInstance(result, str)
        
        result = minimizer._implicant_to_display("XX")
        self.assertEqual(result, "1")
        
        result = minimizer._implicant_to_display("0X")
        self.assertIsInstance(result, str)
    
    def test_can_glue(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        can, pos = minimizer._can_glue("10", "11")
        self.assertTrue(can)
        self.assertEqual(pos, 1)
        
        can, pos = minimizer._can_glue("10", "01")
        self.assertFalse(can)
        
        can, pos = minimizer._can_glue("10", "10")
        self.assertFalse(can)
    
    def test_glue(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result = minimizer._glue("10", "11", 1)
        self.assertEqual(result, "1X")
    
    def test_covers(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        self.assertTrue(minimizer._covers("1X", "10"))
        self.assertTrue(minimizer._covers("X1", "01"))
        self.assertFalse(minimizer._covers("1X", "00"))
        self.assertFalse(minimizer._covers("0X", "10"))
    
    def test_get_condition(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        result = minimizer._get_condition("10")
        self.assertIn("a=1", result)
        self.assertIn("b=0", result)
    
    def test_build_karnaugh_2(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        k_map = minimizer._build_karnaugh_2()
        self.assertEqual(len(k_map), 2)
        self.assertEqual(len(k_map[0]), 2)
    
    def test_build_karnaugh_3(self):
        variables, ast, eval_func = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        k_map = minimizer._build_karnaugh_3()
        self.assertEqual(len(k_map), 2)
        self.assertEqual(len(k_map[0]), 4)
    
    def test_build_karnaugh_4(self):
        variables, ast, eval_func = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        k_map = minimizer._build_karnaugh_4()
        self.assertEqual(len(k_map), 4)
        self.assertEqual(len(k_map[0]), 4)
    
    def test_group_description(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        self.assertEqual(minimizer._group_description([(0,0)]), "одиночная клетка")
        self.assertEqual(minimizer._group_description([(0,0), (0,1)]), "пара клеток")
        self.assertEqual(minimizer._group_description([(0,0), (0,1), (1,0), (1,1)]), "прямоугольник 2x2")
    
    def test_remove_redundant_implicants_empty(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)
        
        original_on_sets = minimizer.on_sets
        minimizer.on_sets = []
        result = minimizer._remove_redundant_implicants_with_output(["1X"])
        minimizer.on_sets = original_on_sets
        
        self.assertEqual(result, ["1X"])


if __name__ == '__main__':
    unittest.main()