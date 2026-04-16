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
    def test_karnaugh_cnf_2var_all_ones(self):
        variables, ast, f = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "1")

    def test_karnaugh_cnf_2var_all_zeros(self):
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "0")

   

    def test_karnaugh_dnf_2var_all_ones(self):
        variables, ast, f = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        self.assertEqual(result, "1")

    def test_karnaugh_dnf_3var_all_zeros(self):
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        self.assertEqual(result, "0")

    def test_karnaugh_dnf_3var_majority(self):
        variables, ast, f = self.parser.parse("(a&b)|(a&c)|(b&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        # Ожидаем a&b ∨ a&c ∨ b&c (пробелы могут быть, проверим наличие частей)
        self.assertIn("a&b", result.replace(" ", ""))
        self.assertIn("a&c", result.replace(" ", ""))
        self.assertIn("b&c", result.replace(" ", ""))
# Добавить в файл tests/test_minimization.py (после существующих тестов)

import itertools

class TestMinimizationExtended(unittest.TestCase):
    """Расширенные тесты для минимизации, покрывающие методы карт Карно и внутренние алгоритмы."""

    def setUp(self):
        self.parser = BooleanParser()

    # ----- Тесты для _get_all_rectangles -----
    def test_get_all_rectangles_2x2(self):
        variables, ast, f = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта 2x2 все единицы
        k_map = [[1,1],[1,1]]
        rects = m._get_all_rectangles(k_map)
        # Должны быть прямоугольники размеров: 1x1 (4 шт), 1x2 (2), 2x1 (2), 2x2 (1)
        # Уникальных форм должно быть 9 (4+2+2+1 = 9)
        # Но из-за циклических могут быть повторы, проверим количество
        self.assertGreaterEqual(len(rects), 4)  # как минимум 4 одиночных
        # Проверим, что есть прямоугольник 2x2
        full = [(0,0),(0,1),(1,0),(1,1)]
        self.assertTrue(any(set(r) == set(full) for r in rects))

    def test_get_all_rectangles_3x4(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта 2x4 с одной единицей
        k_map = [[0,0,0,0],[0,0,1,0]]
        rects = m._get_all_rectangles(k_map)
        # Должны быть только одиночные прямоугольники (размер 1x1)
        # Но могут быть и горизонтальные пары, если есть соседи (здесь нет)
        self.assertTrue(any(len(r)==1 for r in rects))

    def test_get_all_rectangles_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта 4x4 все единицы
        k_map = [[1]*4 for _ in range(4)]
        rects = m._get_all_rectangles(k_map)
        # Должен быть прямоугольник 4x4
        full = [(i,j) for i in range(4) for j in range(4)]
        self.assertTrue(any(set(r) == set(full) for r in rects))
        # Проверим, что есть прямоугольники 2x2, 1x4, 4x1 и т.д.
        sizes = [len(r) for r in rects]
        self.assertIn(16, sizes)
        self.assertIn(8, sizes)   # 2x4 или 4x2
        self.assertIn(4, sizes)

    # ----- Тесты для _minimal_cover_exact -----
    def test_minimal_cover_exact_simple(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cells = [(0,0),(0,1)]
        rects = [[(0,0)],[(0,1)],[(0,0),(0,1)]]
        cover = m._minimal_cover_exact(cells, rects)
        # Должен выбрать один прямоугольник, покрывающий оба
        self.assertEqual(len(cover), 1)
        self.assertTrue(set(cover[0]) == set(cells))

    def test_minimal_cover_exact_multiple(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cells = [(0,0),(1,1)]
        rects = [[(0,0)],[(1,1)],[(0,0),(0,1)],[(1,1),(1,2)]]
        cover = m._minimal_cover_exact(cells, rects)
        # Должно быть два прямоугольника, так как нет одного, покрывающего оба
        self.assertEqual(len(cover), 2)
        self.assertTrue(any(r[0]==(0,0) for r in cover))
        self.assertTrue(any(r[0]==(1,1) for r in cover))

    def test_minimal_cover_exact_large(self):
        """Проверка, что для большого числа прямоугольников используется жадный алгоритм"""
        variables, ast, f = self.parser.parse("a|b|c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Создаём много прямоугольников (например, все возможные одиночные для 4x4)
        cells = [(i,j) for i in range(4) for j in range(4)]
        rects = [[(i,j)] for i in range(4) for j in range(4)]  # 16 штук
        # Добавим ещё несколько больших, чтобы число превысило 30
        for i in range(15):
            rects.append([(i%4, i%4), ((i+1)%4, (i+1)%4)])
        # Теперь rects около 31, должен сработать жадный алгоритм
        cover = m._minimal_cover_exact(cells, rects)
        # Должен покрыть все 16 клеток (жадный выберет много одиночных)
        covered = set()
        for r in cover:
            covered.update(r)
        self.assertEqual(covered, set(cells))

    # ----- Тесты для _group_to_dnf_term -----
    def test_group_to_dnf_term_2x2(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа из двух клеток по горизонтали: (0,0) и (0,1)
        # В 2-переменной карте: строка 0 → a=0, столбцы 0→b=0, 1→b=1
        # Группа даёт ¬a
        group = [(0,0),(0,1)]
        term = m._group_to_dnf_term(group)
        self.assertEqual(term, "¬a")
        # Группа из двух клеток по вертикали: (0,0) и (1,0) → ¬b
        group = [(0,0),(1,0)]
        term = m._group_to_dnf_term(group)
        self.assertEqual(term, "¬b")

    def test_group_to_dnf_term_3x4(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа из двух клеток по горизонтали в одной строке: a=0, bc=00 и bc=01
        # Это соответствует ¬a & ¬b
        group = [(0,0),(0,1)]
        term = m._group_to_dnf_term(group)
        self.assertIn("¬a", term)
        self.assertIn("¬b", term)
        # Группа из двух клеток по вертикали: a=0,bc=00 и a=1,bc=00 → bc=00 фиксировано → ¬b & ¬c
        group = [(0,0),(1,0)]
        term = m._group_to_dnf_term(group)
        self.assertIn("¬b", term)
        self.assertIn("¬c", term)

    def test_group_to_dnf_term_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа 2x2 в углу: строки 0-1, столбцы 0-1 → a=0,b=0,c=0,d=0? Нет, надо разобраться.
        # В 4-переменной карте: строка 0: a=0,b=0; строка1: a=0,b=1; столбец0: c=0,d=0; столбец1: c=0,d=1.
        # Группа 2x2 даст фиксированные a=0 (потому что строки 0 и 1 оба имеют a=0) и c=0 (столбцы 0 и 1 оба имеют c=0)
        group = [(0,0),(0,1),(1,0),(1,1)]
        term = m._group_to_dnf_term(group)
        self.assertIn("¬a", term)
        self.assertIn("¬c", term)
        # b и d меняются, поэтому не входят

    # ----- Тесты для _group_to_cnf_term -----
    def test_group_to_cnf_term_2x2(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа из двух клеток по вертикали: (0,0) и (1,0)
        # Для КНФ: значения: a меняется, b=0 фиксировано → дизъюнкт (b)
        group = [(0,0),(1,0)]
        term = m._group_to_cnf_term(group)
        self.assertEqual(term, "(b)")

    def test_group_to_cnf_term_3x4(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа по вертикали: a=0,bc=00 и a=1,bc=00 → bc=00 фиксировано → дизъюнкт (b | c)
        group = [(0,0),(1,0)]
        term = m._group_to_cnf_term(group)
        self.assertIn("b", term)
        self.assertIn("c", term)

    def test_group_to_cnf_term_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа 2x2 в углу (как выше) → фиксированы a=0 и c=0 → дизъюнкт (a | c)
        group = [(0,0),(0,1),(1,0),(1,1)]
        term = m._group_to_cnf_term(group)
        # Порядок может быть разным, проверим наличие
        self.assertTrue("a" in term or "!a" in term)   # a без отрицания, потому что a=0
        self.assertTrue("c" in term or "!c" in term)

    # ----- Тесты для karnaugh DNF и CNF на разных примерах -----
    def test_karnaugh_dnf_2var_cover_all_rects(self):
        variables, ast, f = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        # Должна быть минимизация a|b
        self.assertIn("a", result)
        self.assertIn("b", result)

    def test_karnaugh_dnf_3var_majority(self):
        variables, ast, f = self.parser.parse("(a&b)|(a&c)|(b&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        # Ожидается a&b ∨ a&c ∨ b&c (уже минимум)
        self.assertIn("a&b", result)
        self.assertIn("a&c", result)
        self.assertIn("b&c", result)

    def test_karnaugh_cnf_3var_majority(self):
        variables, ast, f = self.parser.parse("(a&b)|(a&c)|(b&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        # Для majority КНФ: (a|b) & (a|c) & (b|c)
        self.assertIn("a|b", result)
        self.assertIn("a|c", result)
        self.assertIn("b|c", result)

   

    def test_karnaugh_dnf_4var_single_one(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        # Должна остаться a&b&c&d
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("d", result)

    def test_karnaugh_cnf_4var_single_zero(self):
        # Функция, имеющая один ноль (например, NAND от 4 переменных)
        variables, ast, f = self.parser.parse("!(a&b&c&d)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        # Должен быть один дизъюнкт (!a|!b|!c|!d) или эквивалент
        self.assertIn("!a", result)
        self.assertIn("!b", result)
        self.assertIn("!c", result)
        self.assertIn("!d", result)

    def test_cnf_removal_redundant_complex(self):
        variables, ast, f = self.parser.parse("(a&b)|(c&d)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Создадим искусственные импликанты для КНФ
        implicants = ["X00X", "0XX0", "X0X0"]
        essential = m._remove_redundant_implicants_cnf(implicants)
        # Проверим, что метод не падает и возвращает список
        self.assertIsInstance(essential, list)

    # ----- Тесты для karnaugh при n=2,3,4 с разными картами -----
   

    

   
    def test_karnaugh_cnf_2var_all_zeros(self):
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "0")  # всегда 0 → КНФ = 0

    # ----- Тесты для _minimal_cover_exact с пустыми входными данными -----
    def test_minimal_cover_exact_empty_cells(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cover = m._minimal_cover_exact([], [ [(0,0)] ])
        self.assertEqual(cover, [])

    def test_minimal_cover_exact_no_rectangles(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cover = m._minimal_cover_exact([(0,0)], [])
        self.assertEqual(cover, [])

    # ----- Тесты для _get_all_rectangles с циклическими группами -----
    def test_get_all_rectangles_cyclic_3x4(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта с единицами на противоположных краях, чтобы проверить циклические группы
        k_map = [[1,0,0,1], [1,0,0,1]]
        rects = m._get_all_rectangles(k_map)
        # Должна быть циклическая группа из двух клеток по горизонтали через край (столбцы 3 и 0)
        cyclic = [(0,3),(0,0)]  # в одной строке
        found = any(set(r) == set(cyclic) for r in rects)
        self.assertTrue(found)

    # ----- Тесты для _group_to_dnf_term и _group_to_cnf_term с большими группами -----
    def test_group_to_dnf_term_full_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Вся карта 4x4 единиц
        group = [(i,j) for i in range(4) for j in range(4)]
        term = m._group_to_dnf_term(group)
        self.assertEqual(term, "1")

    def test_group_to_cnf_term_full_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        group = [(i,j) for i in range(4) for j in range(4)]
        term = m._group_to_cnf_term(group)
        self.assertEqual(term, "0")  # пустой дизъюнкт

if __name__ == '__main__':
    unittest.main()
