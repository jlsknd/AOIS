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
    
    # Таблица истинности
    truth_table = TruthTable(variables, ast, eval_func)
    print("\nТАБЛИЦА ИСТИННОСТИ:")
    truth_table.print_table()
    
    # Нормальные формы
    forms = NormalForms(truth_table)
    print(f"\n{'='*70}")
    print("НОРМАЛЬНЫЕ ФОРМЫ:")
    print(f"{'='*70}")
    print(f"СДНФ: {forms.get_sdnf()}")
    print(f"СКНФ: {forms.get_sknf()}")
    print(f"\nЧисловая форма СДНФ: {forms.get_numeric_form_sdnf()}")
    print(f"Числовая форма СКНФ: {forms.get_numeric_form_sknf()}")
    print(f"\nИндексная форма функции: {forms.get_index_form()} (десятичная)")
    print(f"Вектор функции: {truth_table.get_vector()}")
    
    # Классы Поста
    post = PostClasses(truth_table)
    classes = post.get_classes()
    print(f"\n{'='*70}")
    print("КЛАССЫ ПОСТА:")
    print(f"{'='*70}")
    for class_name, belongs in classes.items():
        desc = {
            'T0': 'сохраняет 0',
            'T1': 'сохраняет 1',
            'S': 'самодвойственная',
            'M': 'монотонная',
            'L': 'линейная'
        }.get(class_name, '')
        print(f"  {class_name} ({desc}): {'Да' if belongs else 'Нет'}")
    
    # Полином Жегалкина
    zhegalkin = ZhegalkinPolynomial(truth_table)
    print(f"\n{'='*70}")
    print("ПОЛИНОМ ЖЕГАЛКИНА:")
    print(f"{'='*70}")
    print(f"  {zhegalkin.get_polynomial()}")
    
    # Фиктивные переменные
    dummy_finder = DummyVariablesFinder(truth_table)
    dummy_vars = dummy_finder.find_dummy_variables()
    print(f"\n{'='*70}")
    print("ФИКТИВНЫЕ ПЕРЕМЕННЫЕ:")
    print(f"{'='*70}")
    print(f"  {dummy_vars if dummy_vars else 'Нет фиктивных переменных'}")
    
    # Булевы производные
    derivative = BooleanDerivative(truth_table)
    derivatives = derivative.get_derivative_table()
    print(f"\n{'='*70}")
    print("БУЛЕВЫ ПРОИЗВОДНЫЕ:")
    print(f"{'='*70}")
    
    print("\nЧастные производные:")
    for var in variables:
        key = f"∂f/∂{var}"
        if key in derivatives:
            d = derivatives[key]
            print(f"  {key}:")
            print(f"    Вектор: {d['vector']}")
            print(f"    Функция: {d['xor_form']}")
    
    if len(variables) >= 2:
        print("\nСмешанные производные (2-го порядка):")
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                key = f"∂²f/∂{var1}∂{var2}"
                if key in derivatives:
                    d = derivatives[key]
                    print(f"  {key}:")
                    print(f"    Вектор: {d['vector']}")
                    print(f"    Функция: {d['xor_form']}")
    
    if len(variables) >= 3:
        print("\nСмешанные производные (3-го порядка):")
        for i, var1 in enumerate(variables):
            for j, var2 in enumerate(variables[i+1:], i+1):
                for var3 in variables[j+1:]:
                    key = f"∂³f/∂{var1}∂{var2}∂{var3}"
                    if key in derivatives:
                        d = derivatives[key]
                        print(f"  {key}:")
                        print(f"    Вектор: {d['vector']}")
                        print(f"    Функция: {d['xor_form']}")
    
    # ========== МИНИМИЗАЦИЯ ==========
    minimizer = Minimization(truth_table)
    
    # --- ДНФ ---
    print(f"\n{'='*70}")
    print("МИНИМИЗАЦИЯ ДНФ (дизъюнктивной нормальной формы):")
    print(f"{'='*70}")
    result_calc_dnf, _ = minimizer.minimization_calculated()
    result_table_dnf, _, _ = minimizer.minimization_table()
    result_karnaugh_dnf, _ = minimizer.minimization_karnaugh()
    print(f"\nРезультаты минимизации ДНФ:")
    print(f"  Расчетный метод: {result_calc_dnf}")
    print(f"  Расчетно-табличный метод: {result_table_dnf}")
    print(f"  Карта Карно: {result_karnaugh_dnf}")
    
        # --- КНФ ---
    print(f"\n{'='*70}")
    print("МИНИМИЗАЦИЯ КНФ (конъюнктивной нормальной формы):")
    print(f"{'='*70}")

# 1. Расчетный метод
    result_calc_cnf, _ = minimizer.minimization_calculated_cnf()

# 2. Расчетно-табличный метод
    result_table_cnf, _, _ = minimizer.minimization_table_cnf()

# 3. Карта Карно
    result_karnaugh_cnf, _ = minimizer.minimization_karnaugh_cnf()

    print(f"\nРезультаты минимизации КНФ:")
    print(f"  Расчетный метод: {result_calc_cnf}")
    print(f"  Расчетно-табличный метод: {result_table_cnf}")
    print(f"  Карта Карно: {result_karnaugh_cnf}")

    print(f"\n{'='*70}")


if __name__ == "__main__":
    main()
