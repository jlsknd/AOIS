import sys
from boolean_parser import BooleanParser
from truth_table import TruthTable
from normal_forms import NormalForms
from post_classes import PostClasses
from zhegalkin import ZhegalkinPolynomial
from dummy_variables import DummyVariablesFinder
from boolean_derivative import BooleanDerivative
from minimization import Minimization


def main():
    print("=" * 70)
    print("Лабораторная работа 2: Построение СКНФ и СДНФ на основании таблиц истинности")
    print("=" * 70)
    
    # Ввод функции
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
    else:
        print("\nВведите логическую функцию:")
        print("Поддерживаемые операции: & (И), | (ИЛИ), ! (НЕ), -> (→), ~ (≡)")
        print("Переменные: a, b, c, d, e")
        print("\nПримеры:")
        print("  !(!a->!b)|c")
        print("  (a&b)|(!a&c)")
        print("  a->b")
        expression = input("\n> ")
    
    print(f"\n{'='*70}")
    print(f"Выражение: {expression}")
    print(f"{'='*70}")
    
    # Парсинг
    parser = BooleanParser()
    variables, ast, eval_func = parser.parse(expression)
    print(f"\nПеременные: {variables}")
    print(f"AST: {ast}")
    
    # Построение таблицы истинности
    truth_table = TruthTable(variables, ast, eval_func)
    print("\nТАБЛИЦА ИСТИННОСТИ:")
    truth_table.print_table()
    
    # Нормальные формы
    forms = NormalForms(truth_table)
    
    sdnf = forms.get_sdnf()
    sknf = forms.get_sknf()
    print(f"\n{'='*70}")
    print("НОРМАЛЬНЫЕ ФОРМЫ:")
    print(f"{'='*70}")
    print(f"СДНФ: {sdnf}")
    print(f"СКНФ: {sknf}")
    
    # Числовая форма
    num_sdnf = forms.get_numeric_form_sdnf()
    num_sknf = forms.get_numeric_form_sknf()
    print(f"\nЧисловая форма СДНФ: {num_sdnf}")
    print(f"Числовая форма СКНФ: {num_sknf}")
    
    # Индексная форма
    index_form = forms.get_index_form()
    print(f"\nИндексная форма функции: {index_form} (десятичная)")
    vector = truth_table.get_vector()
    print(f"Вектор функции: {vector}")
    
    # Классы Поста
    post = PostClasses(truth_table)
    classes = post.get_classes()
    print(f"\n{'='*70}")
    print("КЛАССЫ ПОСТА:")
    print(f"{'='*70}")
    for class_name, belongs in classes.items():
        desc = ""
        if class_name == 'T0':
            desc = "сохраняет 0"
        elif class_name == 'T1':
            desc = "сохраняет 1"
        elif class_name == 'S':
            desc = "самодвойственная"
        elif class_name == 'M':
            desc = "монотонная"
        elif class_name == 'L':
            desc = "линейная"
        print(f"  {class_name} ({desc}): {'Да' if belongs else 'Нет'}")
    
    # Полином Жегалкина
    zhegalkin = ZhegalkinPolynomial(truth_table)
    polynomial = zhegalkin.get_polynomial()
    print(f"\n{'='*70}")
    print("ПОЛИНОМ ЖЕГАЛКИНА:")
    print(f"{'='*70}")
    print(f"  {polynomial}")
    
    # Фиктивные переменные
    dummy_finder = DummyVariablesFinder(truth_table)
    dummy_vars = dummy_finder.find_dummy_variables()
    print(f"\n{'='*70}")
    print("ФИКТИВНЫЕ ПЕРЕМЕННЫЕ:")
    print(f"{'='*70}")
    print(f"  {dummy_vars if dummy_vars else 'Нет фиктивных переменных'}")
    
    # Булева дифференциация
    derivative = BooleanDerivative(truth_table)
    derivatives = derivative.get_derivative_table()
    print(f"\n{'='*70}")
    print("БУЛЕВЫ ПРОИЗВОДНЫЕ:")
    print(f"{'='*70}")
    for key, value in derivatives.items():
        print(f"  {key}:")
        print(f"    Вектор: {value['vector']}")
        print(f"    Функция: {value['function']}")
    
    # Минимизация (теперь методы сами выводят этапы)
    minimizer = Minimization(truth_table)
    
    # Расчетный метод
    result_calc, _ = minimizer.minimization_calculated()
    
    # Расчетно-табличный метод
    result_table, _, _ = minimizer.minimization_table()
    
    # Карта Карно
    result_karnaugh, _ = minimizer.minimization_karnaugh()
    
    print(f"\n{'='*70}")
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ МИНИМИЗАЦИИ:")
    print(f"{'='*70}")
    print(f"  Расчетный метод: {result_calc}")
    print(f"  Расчетно-табличный метод: {result_table}")
    print(f"  Карта Карно: {result_karnaugh}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()