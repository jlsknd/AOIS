from src.arithmetic_operations import ArithmeticOperations

def print_separator():
    print("\n" + "=" * 80)

def print_verification(result):
    """Вывод проверки результата"""
    if 'verification' in result:
        print(f"  ПРОВЕРКА:")
        print(f"    Ожидалось: {result['verification']['expected']}")
        print(f"    Совпадает: {'✓' if result['verification']['match'] else '✗'}")
    
    if 'back_to_float' in result:
        print(f"  Обратный перевод из IEEE-754: {result['back_to_float']}")
    
    if 'back_to_decimal' in result:
        print(f"  Обратный перевод из BCD: {result['back_to_decimal']}")

def get_integer_input(prompt):
    """Получение целого числа от пользователя"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число!")

def get_float_input(prompt):
    """Получение числа с плавающей точкой от пользователя"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число!")

def get_positive_integer_input(prompt):
    """Получение положительного целого числа"""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Ошибка: введите положительное число!")
        except ValueError:
            print("Ошибка: введите целое число!")

def show_menu():
    """Отображение главного меню"""
    print_separator()
    print("ГЛАВНОЕ МЕНЮ")
    print("1. Перевод числа в двоичные коды")
    print("2. Сложение в дополнительном коде")
    print("3. Вычитание в дополнительном коде")
    print("4. Умножение в прямом коде")
    print("5. Деление в прямом коде")
    print("6. Операции IEEE-754 (с плавающей точкой)")
    print("7. Сложение в BCD (8421)")
    print("0. Выход")
    print_separator()

def main():
    ops = ArithmeticOperations()
    
    while True:
        show_menu()
        choice = input("Выберите операцию (0-7): ")
        
        if choice == '0':
            print("Программа завершена.")
            break
        
        elif choice == '1':
            print_separator()
            print("ПЕРЕВОД ЧИСЛА В ДВОИЧНЫЕ КОДЫ")
            num = get_integer_input("Введите целое число: ")
            
            result = ops.convert_decimal_to_binary(num)
            print(f"\nЧисло {num}:")
            print(f"  Прямой код:    {result['direct']['binary']}")
            print(f"    Обратный перевод: {result['direct']['decimal_back']} (совпадает: {'✓' if result['direct']['match'] else '✗'})")
            print(f"  Обратный код:  {result['reverse']['binary']}")
            print(f"    Обратный перевод: {result['reverse']['decimal_back']} (совпадает: {'✓' if result['reverse']['match'] else '✗'})")
            print(f"  Дополнительный: {result['additional']['binary']}")
            print(f"    Обратный перевод: {result['additional']['decimal_back']} (совпадает: {'✓' if result['additional']['match'] else '✗'})")
        
        elif choice == '2':
            print_separator()
            print("СЛОЖЕНИЕ В ДОПОЛНИТЕЛЬНОМ КОДЕ")
            a = get_integer_input("Введите первое число: ")
            b = get_integer_input("Введите второе число: ")
            
            result = ops.add_additional(a, b)
            print(f"\n{a} + ({b}) = {result['decimal']}")
            print(f"  {a} в доп. коде: {result['num1_binary']}")
            print(f"  {b} в доп. коде: {result['num2_binary']}")
            print(f"  Результат:      {result['binary']}")
            print_verification(result)
        
        elif choice == '3':
            print_separator()
            print("ВЫЧИТАНИЕ В ДОПОЛНИТЕЛЬНОМ КОДЕ")
            a = get_integer_input("Введите уменьшаемое: ")
            b = get_integer_input("Введите вычитаемое: ")
            
            result = ops.subtract_additional(a, b)
            print(f"\n{a} - {b} = {result['decimal']}")
            print(f"  {a} в доп. коде: {result['num1_binary']}")
            print(f"  -{b} в доп. коде: {result['num2_binary']}")
            print(f"  Результат:      {result['binary']}")
            print_verification(result)
        
        elif choice == '4':
            print_separator()
            print("УМНОЖЕНИЕ В ПРЯМОМ КОДЕ")
            a = get_integer_input("Введите первый множитель: ")
            b = get_integer_input("Введите второй множитель: ")
            
            result = ops.multiply_direct(a, b)
            print(f"\n{a} * {b} = {result['decimal']}")
            print(f"  {a} в прямом коде: {result['num1_binary']}")
            print(f"  {b} в прямом коде: {result['num2_binary']}")
            print(f"  Результат:        {result['binary']}")
            print_verification(result)
        
        elif choice == '5':
            print_separator()
            print("ДЕЛЕНИЕ В ПРЯМОМ КОДЕ")
            a = get_integer_input("Введите делимое: ")
            b = get_integer_input("Введите делитель: ")
            precision = get_positive_integer_input("Введите точность (количество знаков после запятой): ")
            
            try:
                result = ops.divide_direct(a, b, precision)
                print(f"\n{a} / {b} = {result['decimal']:.{precision}f}")
                print(f"  {a} в прямом коде: {result['num1_binary']}")
                print(f"  {b} в прямом коде: {result['num2_binary']}")
                print(f"  Результат (двоичный): {result['quotient_binary']}")
                print_verification(result)
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == '6':
            print_separator()
            print("ОПЕРАЦИИ С ЧИСЛАМИ С ПЛАВАЮЩЕЙ ТОЧКОЙ (IEEE-754)")
            print("1. Сложение")
            print("2. Вычитание")
            print("3. Умножение")
            print("4. Деление")
            
            sub_choice = input("Выберите операцию (1-4): ")
            
            a = get_float_input("Введите первое число: ")
            b = get_float_input("Введите второе число: ")
            
            if sub_choice == '1':
                result = ops.ieee_add(a, b)
                print(f"\n{a} + {b} = {result['decimal']}")
            elif sub_choice == '2':
                result = ops.ieee_subtract(a, b)
                print(f"\n{a} - {b} = {result['decimal']}")
            elif sub_choice == '3':
                result = ops.ieee_multiply(a, b)
                print(f"\n{a} * {b} = {result['decimal']}")
            elif sub_choice == '4':
                try:
                    result = ops.ieee_divide(a, b)
                    print(f"\n{a} / {b} = {result['decimal']}")
                except ValueError as e:
                    print(f"Ошибка: {e}")
                    continue
            else:
                print("Неверный выбор!")
                continue
            
            print(f"\n  {a} в IEEE-754: {result['num1_binary']}")
            print(f"  {b} в IEEE-754: {result['num2_binary']}")
            print(f"  Результат:     {result['binary']}")
            print_verification(result)
        
        elif choice == '7':
            print_separator()
            print("СЛОЖЕНИЕ В BCD (8421)")
            print("(числа должны быть неотрицательными)")
            a = get_positive_integer_input("Введите первое число: ")
            b = get_positive_integer_input("Введите второе число: ")
            
            result = ops.bcd_add(a, b)
            print(f"\n{a} + {b} = {result['decimal']}")
            print(f"  {a} в BCD: {result['num1_binary']}")
            print(f"  {b} в BCD: {result['num2_binary']}")
            print(f"  Результат: {result['binary']}")
            print_verification(result)
        
        else:
            print("Неверный выбор! Пожалуйста, выберите 0-7.")
        
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()
