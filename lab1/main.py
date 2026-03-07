from src.arithmetic_operations import ArithmeticOperations


def print_separator():
    print("\n" + "-" * 80)


def print_verification(result):
    """Вывод проверки результата"""
    if "verification" in result:
        print(f"  ПРОВЕРКА:")
        print(f"    Ожидалось: {result['verification']['expected']}")
        print(f"    Совпадает: {'✓' if result['verification']['match'] else '✗'}")

    if "back_to_float" in result:
        print(f"  Обратный перевод из IEEE-754: {result['back_to_float']}")


def main():
    ops = ArithmeticOperations()

    print("=" * 80)
    print("ДЕМОНСТРАЦИЯ АРИФМЕТИЧЕСКИХ ОПЕРАЦИЙ С ПРОВЕРКОЙ")
    print("=" * 80)

    # 1. Перевод чисел в различные коды
    print_separator()
    print("1. ПЕРЕВОД ЧИСЕЛ В ДВОИЧНЫЕ КОДЫ")
    num = -42
    result = ops.convert_decimal_to_binary(num)
    print(f"Число {num}:")
    print(f"  Прямой код:    {result['direct']['binary']}")
    print(
        f"    Обратный перевод: {result['direct']['decimal_back']} (совпадает: {result['direct']['match']})"
    )
    print(f"  Обратный код:  {result['reverse']['binary']}")
    print(
        f"    Обратный перевод: {result['reverse']['decimal_back']} (совпадает: {result['reverse']['match']})"
    )
    print(f"  Дополнительный: {result['additional']['binary']}")
    print(
        f"    Обратный перевод: {result['additional']['decimal_back']} (совпадает: {result['additional']['match']})"
    )

    # 2. Сложение в дополнительном коде
    print_separator()
    print("2. СЛОЖЕНИЕ В ДОПОЛНИТЕЛЬНОМ КОДЕ")
    a, b = 25, -10
    result = ops.add_additional(a, b)
    print(f"{a} + ({b}) = {result['decimal']}")
    print(f"  {a} в доп. коде: {result['num1_binary']}")
    print(f"  {b} в доп. коде: {result['num2_binary']}")
    print(f"  Результат:      {result['binary']}")
    print_verification(result)

    # 3. Вычитание через дополнительный код
    print_separator()
    print("3. ВЫЧИТАНИЕ В ДОПОЛНИТЕЛЬНОМ КОДЕ")
    a, b = 30, 15
    result = ops.subtract_additional(a, b)
    print(f"{a} - {b} = {result['decimal']}")
    print(f"  {a} в доп. коде: {result['num1_binary']}")
    print(f"  -{b} в доп. коде: {result['num2_binary']}")
    print(f"  Результат:      {result['binary']}")
    print_verification(result)

    # 4. Умножение в прямом коде
    print_separator()
    print("4. УМНОЖЕНИЕ В ПРЯМОМ КОДЕ")
    a, b = 7, -6
    result = ops.multiply_direct(a, b)
    print(f"{a} * ({b}) = {result['decimal']}")
    print(f"  {a} в прямом коде: {result['num1_binary']}")
    print(f"  {b} в прямом коде: {result['num2_binary']}")
    print(f"  Результат:        {result['binary']}")
    print_verification(result)

    # 5. Деление в прямом коде
    print_separator()
    print("5. ДЕЛЕНИЕ В ПРЯМОМ КОДЕ")
    a, b = 42, 5
    result = ops.divide_direct(a, b, 5)
    print(f"{a} / {b} = {result['decimal']:.5f}")
    print(f"  {a} в прямом коде: {result['num1_binary']}")
    print(f"  {b} в прямом коде: {result['num2_binary']}")
    print(f"  Результат (двоичный): {result['quotient_binary']}")
    print_verification(result)

    # 6. Операции с плавающей точкой IEEE-754
    print_separator()
    print("6. ОПЕРАЦИИ С ЧИСЛАМИ С ПЛАВАЮЩЕЙ ТОЧКОЙ (IEEE-754)")
    a, b = 3.14, 2.71

    # Сложение
    result = ops.ieee_add(a, b)
    print(f"\nСложение: {a} + {b} = {result['decimal']}")
    print(f"  {a} в IEEE-754: {result['num1_binary']}")
    print(f"  {b} в IEEE-754: {result['num2_binary']}")
    print(f"  Результат:     {result['binary']}")
    print_verification(result)

    # Вычитание
    result = ops.ieee_subtract(a, b)
    print(f"\nВычитание: {a} - {b} = {result['decimal']}")
    print(f"  Результат: {result['binary']}")
    print_verification(result)

    # Умножение
    result = ops.ieee_multiply(a, b)
    print(f"\nУмножение: {a} * {b} = {result['decimal']}")
    print(f"  Результат: {result['binary']}")
    print_verification(result)

    # Деление
    result = ops.ieee_divide(a, b)
    print(f"\nДеление: {a} / {b} = {result['decimal']}")
    print(f"  Результат: {result['binary']}")
    print_verification(result)

    # 7. Операции в BCD (8421) - только сложение
    print_separator()
    print("7. ОПЕРАЦИИ В BCD (8421)")

    a, b = 123, 456
    result = ops.bcd_add(a, b)
    print(f"\nСложение: {a} + {b} = {result['decimal']}")
    print(f"  {a} в BCD: {result['num1_binary']}")
    print(f"  {b} в BCD: {result['num2_binary']}")
    print(f"  Результат: {result['binary']}")
    print_verification(result)

    a, b = 5, 6
    result = ops.bcd_add(a, b)
    print(f"\nСложение с переносом: {a} + {b} = {result['decimal']}")
    print(f"  {a} в BCD: {result['num1_binary']}")
    print(f"  {b} в BCD: {result['num2_binary']}")
    print(f"  Результат: {result['binary']}")
    print_verification(result)

    a, b = 99, 1
    result = ops.bcd_add(a, b)
    print(f"\nСложение с несколькими переносами: {a} + {b} = {result['decimal']}")
    print(f"  {a} в BCD: {result['num1_binary']}")
    print(f"  {b} в BCD: {result['num2_binary']}")
    print(f"  Результат: {result['binary']}")
    print_verification(result)

    print_separator()
    print("\n✓ Все операции выполнены с проверкой результатов!")


if __name__ == "__main__":
    main()
