"""
Хеш-таблица с линейным пробированием (линейный поиск с шагом q)
"""

from constants import RUS_ALPHABET, TABLE_SIZE, BASE_ADDR, LINEAR_PROBE_STEP
from typing import Optional, List, Dict, Tuple


class HashTableCell:
    """Структура ячейки хеш-таблицы согласно рисунку 1."""
    
    __slots__ = ('id', 'c', 'u', 't', 'l', 'd', 'po', 'pi', 'v', 'h')
    
    def __init__(self, key: str = "", data: str = "", v: int = -1, h: int = -1):
        self.id = key          # ID - ключевое слово
        self.c = 0             # C - флажок коллизий
        self.u = 0             # U - флажок "занято"
        self.t = 1             # T - терминальный флажок
        self.l = 0             # L - флажок связи
        self.d = 0             # D - флажок удаленія
        self.po = -1           # Po - указатель на следующую запись
        self.pi = data         # Pi - данные
        self.v = v             # V - числовое значение (для вывода)
        self.h = h             # h - хеш-адрес (для вывода)
    
    def clear(self):
        """Очистка ячейки (делает её свободной)"""
        self.id = ""
        self.pi = ""
        self.c = 0
        self.u = 0
        self.t = 1
        self.l = 0
        self.d = 0
        self.po = -1
        self.v = -1
        self.h = -1


class HashTable:
    """
    Хеш-таблица с Линейным поиском (линейное пробирование с шагом q)
    
    При коллизии используется линейное пробирование с шагом q:
    - h, h+q, h+2q, h+3q, ... (с циклическим обходом)
    
    Формула: h(V) = (start_idx + i * q) mod H
    """
    
    def __init__(self, size: int = TABLE_SIZE, base: int = BASE_ADDR, step: int = LINEAR_PROBE_STEP):
        self.size = size
        self.base = base
        self.step = step
        self.table: List[HashTableCell] = [HashTableCell() for _ in range(size)]
    
    @staticmethod
    def compute_v(key: str) -> int:
        """Вычисление числового значения V по первым двум буквам."""
        if len(key) < 2:
            raise ValueError("Ключевое слово должно содержать не менее 2 букв")
        
        first_char = key[0].upper()
        second_char = key[1].upper()
        
        if first_char not in RUS_ALPHABET or second_char not in RUS_ALPHABET:
            raise ValueError("Ключевое слово должно содержать русские буквы")
        
        return RUS_ALPHABET[first_char] * 33 + RUS_ALPHABET[second_char]
    
    def hash_function(self, v: int) -> int:
        """Хеш-функция h(V) = V mod H + B"""
        return (v % self.size) + self.base
    
    def _linear_probe(self, start_idx: int, key: str = None) -> int:
        """
        Линейный поиск (линейное пробирование) с шагом q.
        
        Если key указан: ищет ячейку с данным ключом (u=1, d=0, id=key).
        Если key не указан: ищет первую свободную ячейку (u=0 ИЛИ d=1).
        """
        q = self.step
        
        for i in range(self.size):
            idx = (start_idx + i * q) % self.size
            cell = self.table[idx]
            
            if key is not None:
                if cell.u == 1 and cell.d == 0 and cell.id == key:
                    return idx
            else:
                if cell.u == 0 or (cell.u == 1 and cell.d == 1):
                    return idx
        
        return -1
    
    def insert(self, key: str, data: str) -> bool:
        """Вставка записи в хеш-таблицу."""
        if self.search_index(key) != -1:
            print(f"!ОШИБКА! Ключ '{key}' уже существует в таблице.")
            return False
        
        try:
            v = self.compute_v(key)
        except ValueError as e:
            print(f"!ОШИБКА! {e}")
            return False
        
        h = self.hash_function(v)
        target_cell = self.table[h]
        
        if target_cell.u == 0 or (target_cell.u == 1 and target_cell.d == 1):
            target_cell.id = key
            target_cell.pi = data
            target_cell.u = 1
            target_cell.d = 0
            target_cell.c = 0
            target_cell.t = 1
            target_cell.po = -1
            target_cell.v = v
            target_cell.h = h
            return True
        
        free_idx = self._linear_probe(h)
        if free_idx == -1:
            print("!ОШИБКА! Таблица полностью заполнена.")
            return False
        
        last_idx = h
        while self.table[last_idx].po != -1 and self.table[last_idx].t == 0:
            last_idx = self.table[last_idx].po
        
        new_cell = self.table[free_idx]
        new_cell.id = key
        new_cell.pi = data
        new_cell.u = 1
        new_cell.d = 0
        new_cell.c = 1
        new_cell.t = 1
        new_cell.po = -1
        new_cell.v = v
        new_cell.h = h
        
        prev_cell = self.table[last_idx]
        prev_cell.t = 0
        prev_cell.po = free_idx
        
        return True
    
    def search_index(self, key: str) -> int:
        """Поиск индекса записи по ключу."""
        try:
            v = self.compute_v(key)
        except ValueError:
            return -1
        
        h = self.hash_function(v)
        return self._linear_probe(h, key)
    
    def search(self, key: str) -> Optional[str]:
        """Поиск данных по ключу."""
        idx = self.search_index(key)
        if idx == -1:
            return None
        return self.table[idx].pi
    
    def update(self, key: str, new_data: str) -> bool:
        """Обновление данных по ключу."""
        idx = self.search_index(key)
        if idx == -1:
            print(f"!ОШИБКА! Ключ '{key}' не найден.")
            return False
        self.table[idx].pi = new_data
        return True
    
    def delete(self, key: str) -> bool:
        """Логическое удаление записи по ключу."""
        idx = self.search_index(key)
        if idx == -1:
            print(f"!ОШИБКА! Ключ '{key}' не найден.")
            return False
        
        cell = self.table[idx]
        cell.d = 1
        cell.u = 0
        return True
    
    def get_load_factor(self) -> float:
        """Расчёт коэффициента заполнения."""
        occupied = sum(1 for cell in self.table if cell.u == 1 and cell.d == 0)
        return occupied / self.size
    
    def get_v_h(self, key: str) -> Tuple[int, int, bool]:
        """
        Получение V, h и проверка существования ключа.
        Возвращает (V, h, exists)
        exists = True если ключ есть в таблице
        """
        try:
            v = self.compute_v(key)
            h = self.hash_function(v)
            exists = (self.search_index(key) != -1)
            return v, h, exists
        except ValueError as e:
            return -1, -1, False
    
    def print_table(self) -> None:
        """Вывод хеш-таблицы."""
        print("\n" + "=" * 120)
        print(f"ХЕШ-ТАБЛИЦА (линейный поиск, шаг q={self.step})")
        print("=" * 120)
        print(f"{'№':<4} {'ID':<16} {'C':<2} {'U':<2} {'T':<2} {'L':<2} {'D':<2} {'Po':<4} {'Pi (данные)':<40} {'V':<6} {'h':<4}")
        print("-" * 120)
        
        for i, cell in enumerate(self.table):
            if cell.u == 1 and cell.d == 0:
                pi_display = cell.pi[:37] + "..." if len(cell.pi) > 40 else cell.pi
                print(f"{i:<4} {cell.id:<16} {cell.c:<2} {cell.u:<2} {cell.t:<2} {cell.l:<2} {cell.d:<2} {cell.po:<4} {pi_display:<40} {cell.v:<6} {cell.h:<4}")
            else:
                status = "удалено" if cell.d == 1 else ""
                print(f"{i:<4} {'':<16} {'':<2} {cell.u:<2} {'':<2} {'':<2} {cell.d:<2} {cell.po:<4} {status:<40} {'':<6} {'':<4}")
        
        print("=" * 120 + "\n")
    
    def get_all_records(self) -> List[Dict]:
        """Получение всех записей для тестирования."""
        return [
            {
                'index': i,
                'id': cell.id,
                'data': cell.pi,
                'c': cell.c,
                'u': cell.u,
                't': cell.t,
                'd': cell.d,
                'po': cell.po,
                'v': cell.v,
                'h': cell.h
            }
            for i, cell in enumerate(self.table)
            if cell.u == 1 and cell.d == 0
        ]
    
    def get_occupied_count(self) -> int:
        """Количество занятых ячеек."""
        return sum(1 for cell in self.table if cell.u == 1 and cell.d == 0)
    
    def get_probe_step(self) -> int:
        """Возвращает шаг линейного поиска."""
        return self.step