import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boolean_parser import BooleanParser
from truth_table import TruthTable
from normal_forms import NormalForms


class TestNormalForms(unittest.TestCase):
    """Тесты для СДНФ и СКНФ"""
    
    def setUp(self):
        self.parser = BooleanParser()
    
    def test_sdnf_and_2_variables(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        sdnf = forms.get_sdnf()
        self.assertEqual(sdnf, "(a&b)")
    
    def test_sdnf_or_2_variables(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        sdnf = forms.get_sdnf()
        self.assertIn("!a&b", sdnf)
        self.assertIn("a&!b", sdnf)
        self.assertIn("a&b", sdnf)
    
    def test_sknf_and_2_variables(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        sknf = forms.get_sknf()
        self.assertIn("(a|b)", sknf)
        self.assertIn("(a|!b)", sknf)
        self.assertIn("(!a|b)", sknf)
    
    def test_sknf_or_2_variables(self):
        variables, ast, eval_func = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        sknf = forms.get_sknf()
        self.assertEqual(sknf, "(a|b)")
    
    def test_numeric_form_sdnf(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        num_form = forms.get_numeric_form_sdnf()
        self.assertEqual(num_form, [3])
    
    def test_numeric_form_sknf(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        num_form = forms.get_numeric_form_sknf()
        self.assertEqual(num_form, [0, 1, 2])
    
    def test_index_form(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        index = forms.get_index_form()
        vector = tt.get_vector()
        expected = int(''.join(str(b) for b in vector), 2)
        self.assertEqual(index, expected)
    
    def test_sdnf_xor(self):
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        sdnf = forms.get_sdnf()
        self.assertIn("!a&b", sdnf)
        self.assertIn("a&!b", sdnf)
    
    def test_sknf_xor(self):
        variables, ast, eval_func = self.parser.parse("!(a~b)")
        tt = TruthTable(variables, ast, eval_func)
        forms = NormalForms(tt)
        
        sknf = forms.get_sknf()
        self.assertIn("(a|b)", sknf)
        self.assertIn("(!a|!b)", sknf)


if __name__ == '__main__':
    unittest.main()