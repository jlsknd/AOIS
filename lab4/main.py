"""
Лабораторная работа №6
Тема: Моделирование хеш-таблиц
Вариант: 3) Линейное разрешение коллизий - Линейный поиск (шаг q=3)
Тематика: Математика
"""

from hash_table import HashTable
from data import MATH_DATA
from constants import TABLE_SIZE


def print_menu():
    """Вывод меню программы"""
    print("\n" + "=" * 70)
    print("         ЛАБОРАТОРНАЯ РАБОТА №6")
    print("         ХЕШ-ТАБЛИЦА - МАТЕМАТИКА")
    print("         Линейный поиск (шаг q=3)")
    print("=" * 70)
    print("  1. Вывести таблицу")
    print("  2. Вставить запись")
    print("  3. Найти запись")
    print("  4. Обновить запись")
    print("  5. Удалить запись")
    print("  6. Коэффициент заполнения")
    print("  7. Показать V и h для ключа")
    print("  0. Выход")
    print("=" * 70)
    print("Выберите действие: ", end="")


def main():
    """Основная функция программы"""
    ht = HashTable()
    
    # Загрузка начальных данных
    print("\nЗагрузка начальных данных (математическая тематика)...")
    inserted_count = 0
    for key, data in MATH_DATA:
        if ht.insert(key, data):
            inserted_count += 1
    
    print(f"Загружено {inserted_count} записей.")
    print(f"Размер таблицы: {TABLE_SIZE} строк")
    
    
    # меню
    while True:
        print_menu()
        choice = input().strip()
        
        if choice == '1':
            ht.print_table()
        
        elif choice == '2':
            print("\n Вставка новой записи ")
            key = input("Введите ключевое слово (термин на русском): ").strip()
            if not key:
                print("Ошибка: ключевое слово не может быть пустым.")
                continue
            
            data = input("Введите определение: ").strip()
            if not data:
                print("Ошибка: данные не могут быть пустыми.")
                continue
            
            if ht.insert(key, data):
                v, h, exists = ht.get_v_h(key)
                print(f"OK. Запись вставлена. V={v}, h={h}")
            else:
                print("ОШИБКА. Не удалось вставить запись.")
        
        elif choice == '3':
            print("\n Поиск записи ")
            key = input("Введите ключевое слово для поиска: ").strip()
            if not key:
                print("Ошибка: ключевое слово не может быть пустым.")
                continue
            
            result = ht.search(key)
            if result:
                print(f"НАЙДЕНО: {result}")
                idx = ht.search_index(key)
                if idx != -1:
                    cell = ht.table[idx]
                    print(f"  Индекс: {idx}, V={cell.v}, h={cell.h}, C={cell.c}, T={cell.t}")
            else:
                print("НЕ НАЙДЕНО. Запись отсутствует.")
        
        elif choice == '4':
            print("\n Обновление записи ")
            key = input("Введите ключевое слово: ").strip()
            if not key:
                print("Ошибка: ключевое слово не может быть пустым.")
                continue
            
            new_data = input("Введите новые данные: ").strip()
            if not new_data:
                print("Ошибка: данные не могут быть пустыми.")
                continue
            
            if ht.update(key, new_data):
                print("OK. Данные обновлены.")
            else:
                print("ОШИБКА. Запись не найдена.")
        
        elif choice == '5':
            print("\n Удаление записи")
            key = input("Введите ключевое слово для удаления: ").strip()
            if not key:
                print("Ошибка: ключевое слово не может быть пустым.")
                continue
            
            if ht.delete(key):
                print("OK. Запись удалена.")
            else:
                print("ОШИБКА. Запись не найдена.")
        
        elif choice == '6':
            print("\n Коэффициент заполнения ")
            load = ht.get_load_factor()
            occupied = ht.get_occupied_count()
            print(f"Занято ячеек: {occupied} из {TABLE_SIZE}")
            print(f"Коэффициент заполнения: {load*100:.1f}%")
        
        elif choice == '7':
            print("\n Вычисление V и h ")
            key = input("Введите ключевое слово: ").strip()
            if not key:
                print("Ошибка: ключевое слово не может быть пустым.")
                continue
            
            try:
                v, h, exists = ht.get_v_h(key)
                print(f"Ключ: {key}")
                print(f"V = {v}")
                print(f"h = h(V) = {v} mod {TABLE_SIZE} + {0} = {h}")
                if exists:
                    print("(Этот ключ ЕСТЬ в таблице)")
                else:
                    print("(Этого ключа НЕТ в таблице, но V и h вычислены по первым двум буквам)")
            except ValueError as e:
                print(f"Ошибка: {e}")
        
        elif choice == '0':
            print("\nВыход из программы. До свидания!")
            break
        
        else:
            print("Неверный ввод. Пожалуйста, выберите 0-7.")


if __name__ == "__main__":
    main()