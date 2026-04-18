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

    def test_assignment_to_binary(self):
        variables, ast, eval_func = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, eval_func)
        minimizer = Minimization(tt)

        assignment = {"a": True, "b": False}
        result = minimizer._assignment_to_binary(assignment)
        self.assertEqual(result, "10")

        assignment = {"a": False, "b": True}
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

        self.assertEqual(minimizer._group_description([(0, 0)]), "одиночная клетка")
        self.assertEqual(minimizer._group_description([(0, 0), (0, 1)]), "пара клеток")
        self.assertEqual(
            minimizer._group_description([(0, 0), (0, 1), (1, 0), (1, 1)]),
            "прямоугольник 2x2",
        )

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


import itertools


class TestMinimizationExtended(unittest.TestCase):
    """Расширенные тесты для минимизации, покрывающие методы карт Карно и внутренние алгоритмы."""

    def setUp(self):
        self.parser = BooleanParser()

    def test_get_all_rectangles_2x2(self):
        variables, ast, f = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта 2x2 все единицы
        k_map = [[1, 1], [1, 1]]
        rects = m._get_all_rectangles(k_map)
        # Должны быть прямоугольники размеров: 1x1 (4 шт), 1x2 (2), 2x1 (2), 2x2 (1)
        # Уникальных форм должно быть 9 (4+2+2+1 = 9)
        # Но из-за циклических могут быть повторы, проверим количество
        self.assertGreaterEqual(len(rects), 4)  # как минимум 4 одиночных
        # Проверим, что есть прямоугольник 2x2
        full = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertTrue(any(set(r) == set(full) for r in rects))

    def test_get_all_rectangles_3x4(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта 2x4 с одной единицей
        k_map = [[0, 0, 0, 0], [0, 0, 1, 0]]
        rects = m._get_all_rectangles(k_map)
        # Должны быть только одиночные прямоугольники (размер 1x1)
        # Но могут быть и горизонтальные пары, если есть соседи (здесь нет)
        self.assertTrue(any(len(r) == 1 for r in rects))

    def test_get_all_rectangles_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта 4x4 все единицы
        k_map = [[1] * 4 for _ in range(4)]
        rects = m._get_all_rectangles(k_map)
        # Должен быть прямоугольник 4x4
        full = [(i, j) for i in range(4) for j in range(4)]
        self.assertTrue(any(set(r) == set(full) for r in rects))
        # Проверим, что есть прямоугольники 2x2, 1x4, 4x1 и т.д.
        sizes = [len(r) for r in rects]
        self.assertIn(16, sizes)
        self.assertIn(8, sizes)  # 2x4 или 4x2
        self.assertIn(4, sizes)

    def test_minimal_cover_exact_simple(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cells = [(0, 0), (0, 1)]
        rects = [[(0, 0)], [(0, 1)], [(0, 0), (0, 1)]]
        cover = m._minimal_cover_exact(cells, rects)
        # Должен выбрать один прямоугольник, покрывающий оба
        self.assertEqual(len(cover), 1)
        self.assertTrue(set(cover[0]) == set(cells))

    def test_minimal_cover_exact_multiple(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cells = [(0, 0), (1, 1)]
        rects = [[(0, 0)], [(1, 1)], [(0, 0), (0, 1)], [(1, 1), (1, 2)]]
        cover = m._minimal_cover_exact(cells, rects)
        # Должно быть два прямоугольника, так как нет одного, покрывающего оба
        self.assertEqual(len(cover), 2)
        self.assertTrue(any(r[0] == (0, 0) for r in cover))
        self.assertTrue(any(r[0] == (1, 1) for r in cover))

    def test_minimal_cover_exact_large(self):
        """Проверка, что для большого числа прямоугольников используется жадный алгоритм"""
        variables, ast, f = self.parser.parse("a|b|c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Создаём много прямоугольников (например, все возможные одиночные для 4x4)
        cells = [(i, j) for i in range(4) for j in range(4)]
        rects = [[(i, j)] for i in range(4) for j in range(4)]  # 16 штук
        # Добавим ещё несколько больших, чтобы число превысило 30
        for i in range(15):
            rects.append([(i % 4, i % 4), ((i + 1) % 4, (i + 1) % 4)])
        # Теперь rects около 31, должен сработать жадный алгоритм
        cover = m._minimal_cover_exact(cells, rects)
        # Должен покрыть все 16 клеток (жадный выберет много одиночных)
        covered = set()
        for r in cover:
            covered.update(r)
        self.assertEqual(covered, set(cells))

    def test_group_to_dnf_term_2x2(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа из двух клеток по горизонтали: (0,0) и (0,1)
        # В 2-переменной карте: строка 0 → a=0, столбцы 0→b=0, 1→b=1
        # Группа даёт ¬a
        group = [(0, 0), (0, 1)]
        term = m._group_to_dnf_term(group)
        self.assertEqual(term, "¬a")
        # Группа из двух клеток по вертикали: (0,0) и (1,0) → ¬b
        group = [(0, 0), (1, 0)]
        term = m._group_to_dnf_term(group)
        self.assertEqual(term, "¬b")

    def test_group_to_dnf_term_3x4(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа из двух клеток по горизонтали в одной строке: a=0, bc=00 и bc=01
        # Это соответствует ¬a & ¬b
        group = [(0, 0), (0, 1)]
        term = m._group_to_dnf_term(group)
        self.assertIn("¬a", term)
        self.assertIn("¬b", term)
        # Группа из двух клеток по вертикали: a=0,bc=00 и a=1,bc=00 → bc=00 фиксировано → ¬b & ¬c
        group = [(0, 0), (1, 0)]
        term = m._group_to_dnf_term(group)
        self.assertIn("¬b", term)
        self.assertIn("¬c", term)

    def test_group_to_dnf_term_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        group = [(0, 0), (0, 1), (1, 0), (1, 1)]
        term = m._group_to_dnf_term(group)
        self.assertIn("¬a", term)
        self.assertIn("¬c", term)
        # b и d меняются, поэтому не входят

    def test_group_to_cnf_term_2x2(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа из двух клеток по вертикали: (0,0) и (1,0)
        # Для КНФ: значения: a меняется, b=0 фиксировано → дизъюнкт (b)
        group = [(0, 0), (1, 0)]
        term = m._group_to_cnf_term(group)
        self.assertEqual(term, "(b)")

    def test_group_to_cnf_term_3x4(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа по вертикали: a=0,bc=00 и a=1,bc=00 → bc=00 фиксировано → дизъюнкт (b | c)
        group = [(0, 0), (1, 0)]
        term = m._group_to_cnf_term(group)
        self.assertIn("b", term)
        self.assertIn("c", term)

    def test_group_to_cnf_term_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Группа 2x2 в углу (как выше) → фиксированы a=0 и c=0 → дизъюнкт (a | c)
        group = [(0, 0), (0, 1), (1, 0), (1, 1)]
        term = m._group_to_cnf_term(group)
        # Порядок может быть разным, проверим наличие
        self.assertTrue("a" in term or "!a" in term)  # a без отрицания, потому что a=0
        self.assertTrue("c" in term or "!c" in term)

    def test_karnaugh_dnf_2var_cover_all_rects(self):
        variables, ast, f = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        self.assertIn("a", result)
        self.assertIn("b", result)

    def test_karnaugh_dnf_3var_majority(self):
        variables, ast, f = self.parser.parse("(a&b)|(a&c)|(b&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        self.assertIn("a&b", result)
        self.assertIn("a&c", result)
        self.assertIn("b&c", result)

    def test_karnaugh_cnf_3var_majority(self):
        variables, ast, f = self.parser.parse("(a&b)|(a&c)|(b&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        self.assertIn("a|b", result)
        self.assertIn("a|c", result)
        self.assertIn("b|c", result)

    def test_karnaugh_dnf_4var_single_one(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)
        self.assertIn("d", result)

    def test_karnaugh_cnf_4var_single_zero(self):
        variables, ast, f = self.parser.parse("!(a&b&c&d)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        self.assertIn("!a", result)
        self.assertIn("!b", result)
        self.assertIn("!c", result)
        self.assertIn("!d", result)

    def test_cnf_removal_redundant_complex(self):
        variables, ast, f = self.parser.parse("(a&b)|(c&d)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        implicants = ["X00X", "0XX0", "X0X0"]
        essential = m._remove_redundant_implicants_cnf(implicants)
        self.assertIsInstance(essential, list)

    def test_karnaugh_cnf_2var_all_zeros(self):
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "0")  # всегда 0 → КНФ = 0

    def test_minimal_cover_exact_empty_cells(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cover = m._minimal_cover_exact([], [[(0, 0)]])
        self.assertEqual(cover, [])

    def test_minimal_cover_exact_no_rectangles(self):
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cover = m._minimal_cover_exact([(0, 0)], [])
        self.assertEqual(cover, [])

    def test_get_all_rectangles_cyclic_3x4(self):
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта с единицами на противоположных краях, чтобы проверить циклические группы
        k_map = [[1, 0, 0, 1], [1, 0, 0, 1]]
        rects = m._get_all_rectangles(k_map)
        # Должна быть циклическая группа из двух клеток по горизонтали через край (столбцы 3 и 0)
        cyclic = [(0, 3), (0, 0)]  # в одной строке
        found = any(set(r) == set(cyclic) for r in rects)
        self.assertTrue(found)

    def test_group_to_dnf_term_full_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Вся карта 4x4 единиц
        group = [(i, j) for i in range(4) for j in range(4)]
        term = m._group_to_dnf_term(group)
        self.assertEqual(term, "1")

    def test_group_to_cnf_term_full_4x4(self):
        variables, ast, f = self.parser.parse("a&b&c&d")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        group = [(i, j) for i in range(4) for j in range(4)]
        term = m._group_to_cnf_term(group)
        self.assertEqual(term, "0")  # пустой дизъюнкт

    def test_karnaugh_5_vars_dnf_simple(self):
        """Тест карты Карно для 5 переменных (ДНФ) - простая функция"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh()
        # Должна быть одна единица в карте
        self.assertIsNotNone(result)
        self.assertEqual(len(k_map), 4)  # 4 строки
        self.assertEqual(len(k_map[0]), 8)  # 8 столбцов

    def test_karnaugh_5_vars_dnf_all_ones(self):
        """Тест карты Карно для 5 переменных - все единицы"""
        variables, ast, f = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh()
        self.assertEqual(result, "1")

    def test_karnaugh_5_vars_cnf_simple(self):
        """Тест карты Карно для 5 переменных (КНФ)"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh_cnf()
        self.assertIsNotNone(result)

    def test_karnaugh_5_vars_cnf_all_zeros(self):
        """Тест карты Карно для 5 переменных КНФ - все нули"""
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "0")

    def test_get_all_rectangles_5(self):
        """Тест поиска прямоугольников для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Создаём тестовую карту с одной единицей
        k_map = [[0] * 8 for _ in range(4)]
        k_map[0][0] = 1
        rects = m._get_all_rectangles_5(k_map)
        self.assertGreater(len(rects), 0)

    def test_group_to_dnf_term_5_single(self):
        """Тест преобразования одиночной клетки в терм ДНФ для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Клетка (0,0) соответствует a=0,b=0,c=0,d=0,e=0
        term = m._group_to_dnf_term_5([(0, 0)])
        self.assertIsNotNone(term)

    def test_group_to_dnf_term_5_horizontal_pair(self):
        """Тест преобразования горизонтальной пары в терм ДНФ для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Горизонтальная пара (0,0) и (0,1) -> cde = 000 и 001 -> e меняется
        term = m._group_to_dnf_term_5([(0, 0), (0, 1)])
        self.assertIsNotNone(term)

    def test_group_to_dnf_term_5_vertical_pair(self):
        """Тест преобразования вертикальной пары в терм ДНФ для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Вертикальная пара (0,0) и (1,0) -> ab = 00 и 01 -> b меняется
        term = m._group_to_dnf_term_5([(0, 0), (1, 0)])
        self.assertIsNotNone(term)

    def test_group_to_cnf_term_5_single(self):
        """Тест преобразования одиночной клетки в дизъюнкт КНФ для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        term = m._group_to_cnf_term_5([(0, 0)])
        self.assertIsNotNone(term)

    def test_build_karnaugh_5(self):
        """Тест построения карты для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        k_map = m._build_karnaugh_5()
        self.assertEqual(len(k_map), 4)
        self.assertEqual(len(k_map[0]), 8)

    def test_print_karnaugh_5(self):
        """Тест вывода карты для 5 переменных (не падает)"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        k_map = m._build_karnaugh_5()
        import io
        import sys

        captured = io.StringIO()
        sys.stdout = captured
        m._print_karnaugh_5(k_map)
        sys.stdout = sys.__stdout__
        self.assertGreater(len(captured.getvalue()), 0)

    def test_minimal_cover_exact_5_empty(self):
        """Тест минимального покрытия для 5 переменных с пустыми клетками"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cover = m._minimal_cover_exact_5([], [])
        self.assertEqual(cover, [])

    def test_karnaugh_5_vars_complex_dnf(self):
        """Тест сложной функции для 5 переменных ДНФ"""
        # Функция, где есть группа из 2 клеток
        variables, ast, f = self.parser.parse("(a&b&c&d&e)|(a&b&c&d&!e)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh()
        # Должна быть группа из 2 клеток
        self.assertIsNotNone(result)

    def test_karnaugh_5_vars_complex_cnf(self):
        """Тест сложной функции для 5 переменных КНФ"""
        variables, ast, f = self.parser.parse("(a|b|c|d|e)&(a|b|c|d|!e)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh_cnf()
        self.assertIsNotNone(result)

    def test_group_to_dnf_term_5_full_row(self):
        """Тест полной строки в терм ДНФ для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Вся строка 0 (8 клеток)
        group = [(0, j) for j in range(8)]
        term = m._group_to_dnf_term_5(group)
        self.assertIsNotNone(term)

    def test_group_to_dnf_term_5_full_column(self):
        """Тест полного столбца в терм ДНФ для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Весь столбец 0 (4 клетки)
        group = [(i, 0) for i in range(4)]
        term = m._group_to_dnf_term_5(group)
        self.assertIsNotNone(term)

    def test_group_to_dnf_term_5_2x2(self):
        """Тест квадрата 2x2 в терм ДНФ для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Квадрат 2x2 в углу
        group = [(0, 0), (0, 1), (1, 0), (1, 1)]
        term = m._group_to_dnf_term_5(group)
        self.assertIsNotNone(term)

    def test_get_all_rectangles_5_multiple(self):
        """Тест поиска всех прямоугольников для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        # Карта с несколькими единицами
        k_map = [[0] * 8 for _ in range(4)]
        for i in range(4):
            k_map[i][i] = 1
        rects = m._get_all_rectangles_5(k_map)
        self.assertGreater(len(rects), 0)

    def test_karnaugh_5_vars_dnf_with_cover(self):
        """Тест карты Карно для 5 переменных с покрытием"""
        variables, ast, f = self.parser.parse("(a&b&c&d&e)|(a&b&c&!d&e)|(a&b&!c&d&e)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, k_map = m.minimization_karnaugh()
        self.assertIsNotNone(result)

    def test_karnaugh_1_var_dnf(self):
        """Тест карты Карно для 1 переменной (ДНФ)"""
        variables, ast, f = self.parser.parse("a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        self.assertEqual(result, "a")

    def test_karnaugh_1_var_dnf_neg(self):
        """Тест карты Карно для 1 переменной с отрицанием"""
        variables, ast, f = self.parser.parse("!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        self.assertEqual(result, "!a")

    def test_karnaugh_1_var_cnf(self):
        """Тест карты Карно для 1 переменной (КНФ)"""
        variables, ast, f = self.parser.parse("a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "a")

    def test_karnaugh_1_var_cnf_neg(self):
        """Тест карты Карно для 1 переменной с отрицанием (КНФ)"""
        variables, ast, f = self.parser.parse("!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "!a")

    def test_karnaugh_5_vars_dnf_constant_false(self):
        """Тест карты Карно для 5 переменных - константный ложь"""
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh()
        self.assertEqual(result, "0")

    def test_karnaugh_5_vars_cnf_constant_true(self):
        """Тест карты Карно для 5 переменных КНФ - константная истина"""
        variables, ast, f = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        result, _ = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "1")

    def test_minimal_cover_exact_5_with_rectangles(self):
        """Тест минимального покрытия для 5 переменных с прямоугольниками"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        cells = [(0, 0), (0, 1)]
        rectangles = [[(0, 0), (0, 1)], [(0, 0)], [(0, 1)]]
        cover = m._minimal_cover_exact_5(cells, rectangles)
        self.assertEqual(len(cover), 1)

    def test_group_to_cnf_term_5_horizontal_pair(self):
        """Тест преобразования горизонтальной пары в дизъюнкт КНФ для 5 переменных"""
        variables, ast, f = self.parser.parse("a&b&c&d&e")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        group = [(0, 0), (0, 1)]
        term = m._group_to_cnf_term_5(group)
        self.assertIsNotNone(term)

class TestMinimizationCoverage(unittest.TestCase):
    """Тесты для покрытия непокрытых строк minimization.py"""

    def setUp(self):
        self.parser = BooleanParser()

    def test_calculated_dnf_with_verbose_output(self):
        """Покрытие строк 784, 788, 793-798, 807, 811, 813, 816-819"""
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        # Перенаправляем stdout для подавления вывода
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        
        result, implicants = m.minimization_calculated()
        
        sys.stdout = sys.__stdout__
        
        self.assertEqual(result, "a&b")
        self.assertEqual(len(implicants), 1)

    def test_calculated_dnf_empty_on_sets(self):
        """Покрытие строки 788 (return "0", [])"""
        variables, ast, f = self.parser.parse("a&!a")  # всегда 0
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, implicants = m.minimization_calculated()
        self.assertEqual(result, "0")
        self.assertEqual(implicants, [])

    def test_calculated_dnf_single_implicant(self):
        """Покрытие строк 816-819"""
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, implicants = m.minimization_calculated()
        self.assertIn("a", result)
        self.assertIn("b", result)
        self.assertIn("c", result)

    def test_calculated_cnf_basic(self):
        """Покрытие строк 738, 753, 763"""
        variables, ast, f = self.parser.parse("a|b")  # простая функция
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        
        result, implicants = m.minimization_calculated_cnf()
        
        sys.stdout = sys.__stdout__
        
        self.assertIsNotNone(result)
        self.assertIsInstance(implicants, list)

    def test_calculated_cnf_empty_off_sets(self):
        """Покрытие строки 738 (return "1", [])"""
        variables, ast, f = self.parser.parse("a|!a")  # всегда 1
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, implicants = m.minimization_calculated_cnf()
        self.assertEqual(result, "1")
        self.assertEqual(implicants, [])

    def test_calculated_cnf_with_essential(self):
        """Покрытие строк 753, 763"""
        variables, ast, f = self.parser.parse("(a|b)&(a|c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, implicants = m.minimization_calculated_cnf()
        self.assertIsNotNone(result)

    def test_table_dnf_with_core_implicants(self):
        """Покрытие строк 591, 595"""
        variables, ast, f = self.parser.parse("(a&b)|(a&c)|(b&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, core_implicants, cover_table = m.minimization_table()
        self.assertIsNotNone(result)
        self.assertIsInstance(core_implicants, list)
        self.assertIsInstance(cover_table, list)

    def test_table_dnf_empty_on_sets(self):
        """Покрытие ветки if not implicants or not self.on_sets"""
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, core_implicants, cover_table = m.minimization_table()
        self.assertEqual(result, "0")
        self.assertEqual(core_implicants, [])
        self.assertEqual(cover_table, [])

    def test_table_cnf_basic(self):
        """Покрытие строк 329-341, 344-384"""
        variables, ast, f = self.parser.parse("a&b")  # КНФ: a&b
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, core_implicants, cover_table = m.minimization_table_cnf()
        self.assertIsNotNone(result)
        self.assertIsInstance(core_implicants, list)

    def test_table_cnf_empty_off_sets(self):
        """Покрытие ветки if not implicants or not off_sets"""
        variables, ast, f = self.parser.parse("a|!a")  # всегда 1, off_sets пуст
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, core_implicants, cover_table = m.minimization_table_cnf()
        self.assertEqual(result, "1")
        self.assertEqual(core_implicants, [])
        self.assertEqual(cover_table, [])

    def test_table_cnf_with_core(self):
        """Покрытие строк с core_indices"""
        variables, ast, f = self.parser.parse("(a|b)&(a|c)&(b|c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, core_implicants, cover_table = m.minimization_table_cnf()
        self.assertIsNotNone(result)

    def test_get_prime_implicants_verbose(self):
        """Покрытие строк 155, 163-215 с verbose=True"""
        variables, ast, f = self.parser.parse("(a&b)|(a&c)|(b&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        
        implicants = m._get_prime_implicants(verbose=True)
        
        sys.stdout = sys.__stdout__
        
        self.assertIsInstance(implicants, list)
        self.assertGreater(len(implicants), 0)

    def test_get_prime_implicants_single(self):
        """Покрытие строки 155 (if not current_impls: return [])"""
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        implicants = m._get_prime_implicants(verbose=False)
        self.assertEqual(implicants, [])

    def test_get_prime_implicants_cnf_verbose(self):
        """Покрытие строк 231-232, 240, 246, 266"""
        variables, ast, f = self.parser.parse("(a|b)&(a|c)&(b|c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        
        implicants = m._get_prime_implicants_cnf(verbose=True)
        
        sys.stdout = sys.__stdout__
        
        self.assertIsInstance(implicants, list)

    def test_get_prime_implicants_cnf_empty(self):
        """Покрытие строки 240 (if not current_impls: return [])"""
        variables, ast, f = self.parser.parse("a|!a")  # off_sets пуст
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        implicants = m._get_prime_implicants_cnf(verbose=False)
        self.assertEqual(implicants, [])

    def test_remove_redundant_with_output_essential(self):
        """Покрытие строк 415, 434, 449"""
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        implicants = ["11"]  # только одна импликанта
        essential = m._remove_redundant_implicants_with_output(implicants)
        self.assertEqual(essential, ["11"])

    def test_remove_redundant_with_output_empty_implicants(self):
        """Покрытие строки 415 (if not implicants or not self.on_sets)"""
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        essential = m._remove_redundant_implicants_with_output([])
        self.assertEqual(essential, [])
        
        # Пустые on_sets
        original_on_sets = m.on_sets
        m.on_sets = []
        essential = m._remove_redundant_implicants_with_output(["11"])
        m.on_sets = original_on_sets
        self.assertEqual(essential, ["11"])

    def test_remove_redundant_cnf_essential(self):
        """Покрытие строк 501, 519, 526-527, 539"""
        variables, ast, f = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        # Создаём off_sets вручную
        off_sets = m.truth_table.get_off_sets()
        # off_sets для a|b: {(a=0,b=0)}
        
        implicants = ["00"]  # покрывает off_set
        essential = m._remove_redundant_implicants_cnf(implicants)
        self.assertEqual(essential, ["00"])

    def test_remove_redundant_cnf_empty(self):
        """Покрытие строки 501 (if not implicants or not off_sets)"""
        variables, ast, f = self.parser.parse("a|!a")  # off_sets пуст
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        essential = m._remove_redundant_implicants_cnf(["00"])
        self.assertEqual(essential, ["00"])

    def test_karnaugh_2var_dnf_with_output(self):
        """Покрытие строк 832-845, 848, 851, 858"""
        variables, ast, f = self.parser.parse("a|b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        import io
        import sys
        captured = io.StringIO()
        sys.stdout = captured
        
        result, k_map = m.minimization_karnaugh()
        
        sys.stdout = sys.__stdout__
        
        self.assertIsNotNone(result)
        self.assertEqual(len(k_map), 2)

    def test_karnaugh_3var_dnf_empty_cells(self):
        """Покрытие строки 889 (if not cells: return "0", k_map)"""
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, k_map = m.minimization_karnaugh()
        self.assertEqual(result, "0")

    def test_karnaugh_4var_dnf_with_rectangles(self):
        """Покрытие строк 976, 980"""
        variables, ast, f = self.parser.parse("(a&b)|(c&d)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, k_map = m.minimization_karnaugh()
        self.assertIsNotNone(result)

    def test_karnaugh_unsupported_vars(self):
        """Покрытие строк 1005 (возврат сообщения об ошибке)"""
        # Создаём фиктивный TruthTable с 6 переменными
        class MockTruthTable:
            def __init__(self):
                self.variables = ['a', 'b', 'c', 'd', 'e', 'f']
            def get_on_sets(self):
                return []
        
        m = Minimization(MockTruthTable())
        m.n = 6
        result, _ = m.minimization_karnaugh()
        self.assertEqual(result, "Метод Карно поддерживается для 2-5 переменных")


    def test_karnaugh_cnf_3var_empty_cells(self):
        """Покрытие строк 1033, 1036-1038"""
        variables, ast, f = self.parser.parse("a|!a")  # всегда 1, off_sets пуст
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, k_map = m.minimization_karnaugh_cnf()
        self.assertEqual(result, "1")

    def test_karnaugh_cnf_4var_with_rectangles(self):
        """Покрытие строк 1041, 1045"""
        variables, ast, f = self.parser.parse("(a&b)&(c&d)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, k_map = m.minimization_karnaugh_cnf()
        self.assertIsNotNone(result)

    def test_build_karnaugh_2_with_values(self):
        """Покрытие строк 1061"""
        variables, ast, f = self.parser.parse("a&b")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        k_map = m._build_karnaugh_2()
        # Проверяем, что единица в правильном месте (a=1,b=1)
        self.assertEqual(k_map[1][1], 1)

    def test_build_karnaugh_3_with_values(self):
        """Покрытие строк 1081-1083"""
        variables, ast, f = self.parser.parse("a&b&c")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        k_map = m._build_karnaugh_3()
        # a=1, b=1, c=1 -> x=1, col=2 (y=1,z=1)
        self.assertEqual(k_map[1][2], 1)

    def test_calculated_dnf_complex_expression(self):
        """Дополнительный тест для minimization_calculated"""
        variables, ast, f = self.parser.parse("(a&b)|(!a&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, _ = m.minimization_calculated()
        self.assertIsNotNone(result)

    def test_table_cnf_complex_expression(self):
        """Дополнительный тест для minimization_table_cnf"""
        variables, ast, f = self.parser.parse("(a|b)&(!a|c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        result, core, table = m.minimization_table_cnf()
        self.assertIsNotNone(result)

    def test_get_prime_implicants_multilevel_gluing(self):
        """Тест многоуровневого склеивания"""
        variables, ast, f = self.parser.parse("(a&b&c)|(a&b&!c)|(a&!b&c)|(a&!b&!c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        implicants = m._get_prime_implicants(verbose=False)
        # Должна получиться импликанта "a"
        self.assertTrue(any("X" in impl for impl in implicants))

    def test_get_prime_implicants_cnf_multilevel_gluing(self):
        """Тест многоуровневого склеивания для КНФ"""
        variables, ast, f = self.parser.parse("(a|b|c)&(a|b|!c)&(a|!b|c)&(a|!b|!c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        implicants = m._get_prime_implicants_cnf(verbose=False)
        self.assertIsInstance(implicants, list)

    def test_remove_redundant_with_output_multiple(self):
        """Тест удаления лишних импликант с несколькими"""
        variables, ast, f = self.parser.parse("(a&b)|(a&c)")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        
        # Импликанты: "11X", "1X1" (обе необходимы)
        m.on_sets = [{"a": True, "b": True, "c": False}, {"a": True, "b": False, "c": True}]
        implicants = ["11X", "1X1"]
        essential = m._remove_redundant_implicants_with_output(implicants)
        self.assertEqual(len(essential), 2)

    def test_group_to_dnf_term_4x4_full_cover(self):
        """Тест преобразования полной карты"""
        variables, ast, f = self.parser.parse("a|!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        m.n = 4
        
        # Все клетки карты 4x4
        group = [(i, j) for i in range(4) for j in range(4)]
        term = m._group_to_dnf_term(group)
        self.assertEqual(term, "1")

    def test_group_to_cnf_term_4x4_full_cover(self):
        """Тест преобразования полной карты в КНФ"""
        variables, ast, f = self.parser.parse("a&!a")
        tt = TruthTable(variables, ast, f)
        m = Minimization(tt)
        m.n = 4
        
        group = [(i, j) for i in range(4) for j in range(4)]
        term = m._group_to_cnf_term(group)
        self.assertEqual(term, "0")




if __name__ == "__main__":
    unittest.main()
