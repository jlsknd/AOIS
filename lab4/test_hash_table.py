"""
Модульные тесты для хеш-таблицы
"""

import unittest
from hash_table import HashTable
from data import MATH_DATA


class TestHashTable(unittest.TestCase):

    def setUp(self):
        self.ht = HashTable()


    def test_compute_v_errors(self):
        # Слишком короткое слово
        with self.assertRaises(ValueError):
            HashTable.compute_v("A")
        with self.assertRaises(ValueError):
            HashTable.compute_v("")

        with self.assertRaises(ValueError):
            HashTable.compute_v("Abc")
        with self.assertRaises(ValueError):
            HashTable.compute_v("Hello")


        with self.assertRaises(ValueError):
            HashTable.compute_v("Aбвг")


    def test_hash_function(self):
        """Тест хеш-функции h(V) = V mod H + B"""
        self.assertEqual(self.ht.hash_function(1), 1)
        self.assertEqual(self.ht.hash_function(48), 8)
        self.assertEqual(self.ht.hash_function(388), 8)
        self.assertEqual(self.ht.hash_function(20), 0)
        self.assertEqual(self.ht.hash_function(40), 0)
        self.assertEqual(self.ht.hash_function(41), 1)


    def test_insert_and_search(self):
        """Тест вставки и поиска"""
        self.assertTrue(self.ht.insert("Интеграл", "Понятие интеграла"))
        self.assertEqual(self.ht.search("Интеграл"), "Понятие интеграла")
        self.assertIsNone(self.ht.search("Несуществующий"))

    def test_insert_duplicate(self):
        """Тест: запрет вставки дубликатов"""
        self.ht.insert("Матрица", "Таблица чисел")
        self.assertFalse(self.ht.insert("Матрица", "Другое определение"))
        self.assertEqual(self.ht.search("Матрица"), "Таблица чисел")

    def test_insert_many_records(self):
        """Тест вставки множества записей"""
        for i in range(15):
            key = f"Ключ{i:02d}"
            data = f"Данные{i}"
            self.assertTrue(self.ht.insert(key, data))

        # Проверяем, что все вставились
        for i in range(15):
            key = f"Ключ{i:02d}"
            self.assertIsNotNone(self.ht.search(key))

    def test_insert_with_collision(self):
        """Тест вставки с коллизией"""
        self.ht.insert("Абаев", "Первый")
        self.ht.insert("Абвгд", "Второй")  # Коллизия
        self.ht.insert("Абрамов", "Третий")  # Ещё коллизия

        self.assertEqual(self.ht.search("Абаев"), "Первый")
        self.assertEqual(self.ht.search("Абвгд"), "Второй")
        self.assertEqual(self.ht.search("Абрамов"), "Третий")

    def test_insert_invalid_key(self):
        """Тест вставки с невалидным ключом"""
        self.assertFalse(self.ht.insert("A", "Данные"))  # Слишком короткий
        self.assertFalse(self.ht.insert("", "Данные"))  # Пустой
        self.assertFalse(self.ht.insert("Hello", "Данные"))  # Латиница


    def test_update(self):
        """Тест обновления записи"""
        self.ht.insert("Предел", "Старое определение")
        self.assertTrue(self.ht.update("Предел", "Новое определение"))
        self.assertEqual(self.ht.search("Предел"), "Новое определение")
        self.assertFalse(self.ht.update("НетТакого", "Данные"))

    def test_update_nonexistent(self):
        """Тест обновления несуществующей записи"""
        result = self.ht.update("НесуществующийКлюч", "Данные")
        self.assertFalse(result)

    def test_delete(self):
        """Тест удаления записи"""
        self.ht.insert("Множество", "Совокупность элементов")
        self.assertTrue(self.ht.delete("Множество"))
        self.assertIsNone(self.ht.search("Множество"))

    def test_delete_nonexistent(self):
        """Тест удаления несуществующей записи"""
        result = self.ht.delete("НесуществующийКлюч")
        self.assertFalse(result)

    def test_delete_twice(self):
        """Тест повторного удаления"""
        self.ht.insert("Вектор", "Направленный отрезок")
        self.assertTrue(self.ht.delete("Вектор"))
        self.assertFalse(self.ht.delete("Вектор"))

    def test_delete_and_reinsert(self):
        """Тест: удаление и повторная вставка того же ключа"""
        self.ht.insert("Функция", "Зависимость")
        self.assertTrue(self.ht.delete("Функция"))
        self.assertTrue(self.ht.insert("Функция", "Новая зависимость"))
        self.assertEqual(self.ht.search("Функция"), "Новая зависимость")

    # коэф-т заполнения

    def test_load_factor_empty(self):
        """Тест коэффициента заполнения пустой таблицы"""
        self.assertEqual(self.ht.get_load_factor(), 0.0)
        self.assertEqual(self.ht.get_occupied_count(), 0)

    def test_load_factor(self):
        """Тест коэффициента заполнения"""
        for key, data in MATH_DATA[:10]:
            self.ht.insert(key, data)
        self.assertAlmostEqual(self.ht.get_load_factor(), 10 / 20)
        self.assertEqual(self.ht.get_occupied_count(), 10)

    def test_load_factor_after_delete(self):
        """Тест коэффициента заполнения после удаления"""
        self.ht.insert("Ключ1", "Данные1")
        self.ht.insert("Ключ2", "Данные2")
        self.assertEqual(self.ht.get_load_factor(), 2 / 20)

        self.ht.delete("Ключ1")
        self.assertEqual(self.ht.get_load_factor(), 1 / 20)

    def test_load_factor_full_table(self):
        """Тест коэффициента заполнения полной таблицы"""
        for i in range(20):
            key = f"Ключ{i:02d}"
            self.ht.insert(key, f"Данные{i}")

        self.assertEqual(self.ht.get_load_factor(), 1.0)
        self.assertEqual(self.ht.get_occupied_count(), 20)

    # получение V, h
    def test_get_v_h(self):
        """Тест получения V и h для ключа"""
        self.ht.insert("Интеграл", "Данные")
        v, h, exists = self.ht.get_v_h("Интеграл")
        self.assertIsInstance(v, int)
        self.assertIsInstance(h, int)
        self.assertTrue(0 <= h < self.ht.size)
        self.assertTrue(exists)

    def test_get_v_h_nonexistent(self):
        """Тест получения V и h для несуществующего ключа"""
        v, h, exists = self.ht.get_v_h("НесуществующийТермин")
        self.assertIsInstance(v, int)
        self.assertIsInstance(h, int)
        self.assertFalse(exists)

    def test_get_v_h_invalid_key(self):
        """Тест получения V и h для невалидного ключа"""
        v, h, exists = self.ht.get_v_h("A")
        self.assertEqual(v, -1)
        self.assertEqual(h, -1)
        self.assertFalse(exists)


    def test_print_table(self):
        """Тест вывода таблицы"""
        self.ht.insert("Тест", "Данные")
        try:
            self.ht.print_table()
        except Exception as e:
            self.fail(f"print_table() вызвал ошибку: {e}")

    def test_print_empty_table(self):
        """Тест вывода пустой таблицы"""
        try:
            self.ht.print_table()
        except Exception as e:
            self.fail(f"print_table() пустой таблицы вызвал ошибку: {e}")


    def test_full_table_insert(self):
        """Тест: вставка в полностью заполненную таблицу"""
        for i in range(20):
            self.ht.insert(f"Ключ{i:02d}", f"Данные{i}")

        result = self.ht.insert("ЛишнийКлюч", "ЛишниеДанные")
        self.assertFalse(result)

    def test_search_in_full_table(self):
        """Тест поиска в полной таблице"""
        for i in range(20):
            self.ht.insert(f"Ключ{i:02d}", f"Данные{i}")

        self.assertIsNotNone(self.ht.search("Ключ05"))
        self.assertIsNone(self.ht.search("Несуществующий"))

    def test_collision_chain(self):
        """Тест цепочки коллизий"""
        # Вставляем ключи с одинаковым h
        self.ht.insert("Абаев", "1")  # h=1
        self.ht.insert("Абвгд", "2")  # h=1 - коллизия
        self.ht.insert("Абрамов", "3")  # h=1 - коллизия

        records = self.ht.get_all_records()
        records_with_h1 = [r for r in records if r["h"] == 1]
        self.assertGreaterEqual(len(records_with_h1), 3)


    def test_min_requirements(self):
        """Проверка минимальных требований лр"""
        for key, data in MATH_DATA:
            self.ht.insert(key, data)

        records = self.ht.get_all_records()

        #  не менее 10 записей
        self.assertGreaterEqual(len(records), 10)
        print(f"\n[TEST] Всего записей: {len(records)}")

        # не менее 2 коллизий
        collisions = sum(1 for r in records if r["c"] == 1)
        self.assertGreaterEqual(collisions, 2)
        print(f"[TEST] Коллизий: {collisions}")

        #цепочка не менее 3 элементов
        chain_lengths = {}
        for r in records:
            h = r["h"]
            chain_lengths[h] = chain_lengths.get(h, 0) + 1
        max_chain = max(chain_lengths.values()) if chain_lengths else 0
        self.assertGreaterEqual(max_chain, 3)
        print(f"[TEST] Максимальная длина цепочки: {max_chain}")

    # ТЕСТЫ CRUD 

    def test_crud_sequence(self):
        """Тест полного цикла CRUD операций"""
        # CREATE
        self.ht.insert("Ряд", "Последовательность чисел")

        # READ
        self.assertEqual(self.ht.search("Ряд"), "Последовательность чисел")

        # UPDATE
        self.ht.update("Ряд", "Сумма членов последовательности")
        self.assertEqual(self.ht.search("Ряд"), "Сумма членов последовательности")

        # DELETE
        self.ht.delete("Ряд")
        self.assertIsNone(self.ht.search("Ряд"))

    #получение записей

    def test_get_all_records(self):
        """Тест получения всех записей"""
        self.ht.insert("Запись1", "Данные1")
        self.ht.insert("Запись2", "Данные2")

        records = self.ht.get_all_records()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["id"], "Запись1")
        self.assertEqual(records[1]["id"], "Запись2")

    def test_get_all_records_empty(self):
        """Тест получения всех записей из пустой таблицы"""
        records = self.ht.get_all_records()
        self.assertEqual(len(records), 0)

    # ============ ТЕСТ ШАГА ЛИНЕЙНОГО ПОИСКА ============

    def test_get_probe_step(self):
        """Тест получения шага линейного поиска"""
        step = self.ht.get_probe_step()
        self.assertEqual(step, 3)  # По умолчанию 3 из constants.py

    # ============ ТЕСТ ОЧИСТКИ ЯЧЕЙКИ ============

    def test_cell_clear(self):
        """Тест очистки ячейки"""
        from hash_table import HashTableCell

        cell = HashTableCell("Тест", "Данные", 100, 5)
        cell.u = 1
        cell.clear()

        self.assertEqual(cell.id, "")
        self.assertEqual(cell.pi, "")
        self.assertEqual(cell.u, 0)
        self.assertEqual(cell.c, 0)
        self.assertEqual(cell.d, 0)
        self.assertEqual(cell.po, -1)
        self.assertEqual(cell.v, -1)
        self.assertEqual(cell.h, -1)


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
