class Minimization:
    """
    Класс для минимизации булевых функций.
    Методы:
    1. Расчетный метод (метод Квайна)
    2. Расчетно-табличный метод
    3. Табличный метод (карты Карно)
    """
    
    def __init__(self, truth_table):
        self.truth_table = truth_table
        self.variables = truth_table.variables
        self.on_sets = truth_table.get_on_sets()
        self.n = len(self.variables)
    
    def _assignment_to_binary(self, assignment):
        """Преобразует набор значений в двоичную строку"""
        return ''.join([str(int(assignment[var])) for var in self.variables])
    
    def _binary_to_term(self, binary):
        """Преобразует двоичную строку в терм (для вывода)"""
        if 'X' in binary:
            term_parts = []
            for i, val in enumerate(binary):
                if val == '0':
                    term_parts.append(f'¬{self.variables[i]}')
                elif val == '1':
                    term_parts.append(self.variables[i])
            return '(' + ''.join(term_parts) + ')'
        else:
            term_parts = []
            for i, val in enumerate(binary):
                if val == '0':
                    term_parts.append(f'¬{self.variables[i]}')
                elif val == '1':
                    term_parts.append(self.variables[i])
            return '(' + ''.join(term_parts) + ')'
    
    def _implicant_to_term(self, implicant):
        """Преобразует импликанту в терм с фиксированным порядком переменных"""
        if implicant.count('X') == self.n:
            return "1"
        
        term_parts = []
        for i, val in enumerate(implicant):
            if val == '0':
                term_parts.append(f"!{self.variables[i]}")
            elif val == '1':
                term_parts.append(self.variables[i])
        
        term_parts.sort()
        return "&".join(term_parts)
    
    def _implicant_to_display(self, implicant):
        """Преобразует импликанту в читаемый формат для вывода"""
        if implicant.count('X') == self.n:
            return "1"
        
        term_parts = []
        for i, val in enumerate(implicant):
            if val == '0':
                term_parts.append(f"¬{self.variables[i]}")
            elif val == '1':
                term_parts.append(self.variables[i])
            else:
                term_parts.append('X')
        
        return ''.join(term_parts)
    
    def _can_glue(self, impl1, impl2):
        """Проверяет возможность склеивания двух импликант"""
        diff_count = 0
        diff_pos = -1
        
        for i in range(self.n):
            if impl1[i] != impl2[i]:
                diff_count += 1
                diff_pos = i
                if diff_count > 1:
                    return False, -1
        
        return diff_count == 1, diff_pos
    
    def _glue(self, impl1, impl2, pos):
        """Склеивает две импликанты"""
        return impl1[:pos] + 'X' + impl1[pos+1:]
    
    def _covers(self, implicant, binary):
        """Проверяет, покрывает ли импликанта двоичный набор"""
        for i in range(len(implicant)):
            if implicant[i] != 'X' and implicant[i] != binary[i]:
                return False
        return True
    
    def _get_prime_implicants(self, verbose=False):
        """
        Внутренний метод получения простых импликант.
        Если verbose=True, выводит этапы склеивания.
        Возвращает список простых импликант.
        """
        # Начальные импликанты из конституэнт единицы
        current_impls = []
        for assignment in self.on_sets:
            binary = self._assignment_to_binary(assignment)
            current_impls.append(binary)
        
        if not current_impls:
            return []
        
        all_implicants = []
        level = 1
        
        if verbose:
            print(f"\nИсходная СДНФ:")
            terms = [self._binary_to_term(impl) for impl in current_impls]
            print(f"  {', '.join(terms)}")
            print(f"  {[tuple(int(b) for b in impl) for impl in current_impls]}")
            print(f"\nЭтап склеивания (уровень {level}):")
        
        while True:
            used = [False] * len(current_impls)
            next_impls = []
            glued_pairs = []
            
            # Пытаемся склеить все пары
            for i in range(len(current_impls)):
                for j in range(i + 1, len(current_impls)):
                    can_glue, pos = self._can_glue(current_impls[i], current_impls[j])
                    if can_glue:
                        glued = self._glue(current_impls[i], current_impls[j], pos)
                        used[i] = True
                        used[j] = True
                        if glued not in next_impls:
                            next_impls.append(glued)
                            glued_pairs.append((current_impls[i], current_impls[j], glued, pos))
            
            # Выводим склеенные пары (если нужен вывод)
            if verbose:
                for impl1, impl2, glued, pos in glued_pairs:
                    term1 = self._binary_to_term(impl1)
                    term2 = self._binary_to_term(impl2)
                    result = self._implicant_to_display(glued)
                    var_name = self.variables[pos]
                    print(f"  {term1} ∨ {term2} => ({result})  [по переменной {var_name}]")
            
            # Сохраняем неиспользованные импликанты
            for i in range(len(current_impls)):
                if not used[i] and current_impls[i] not in all_implicants:
                    all_implicants.append(current_impls[i])
            
            # Если больше склеивать нечего
            if not next_impls:
                break
            
            if verbose:
                print(f"\nРезультат склеивания уровня {level}:")
                result_terms = [self._implicant_to_display(impl) for impl in next_impls]
                print(f"  {', '.join(result_terms)}")
                print(f"  {[tuple('X' if c == 'X' else int(c) for c in impl) for impl in next_impls]}")
                print(f"\nЭтап склеивания (уровень {level + 1}):")
            
            current_impls = next_impls
            level += 1
        
        # Добавляем последнее поколение
        for impl in current_impls:
            if impl not in all_implicants:
                all_implicants.append(impl)
        
        if verbose:
            print(f"\nРезультат после всех склеиваний:")
            result_terms = [self._implicant_to_display(impl) for impl in all_implicants]
            print(f"  {', '.join(result_terms)}")
        
        return all_implicants
    
    def _remove_redundant_implicants_with_output(self, implicants):
        """Удаление лишних импликант с выводом"""
        if not implicants or not self.on_sets:
            return implicants
        
        essential = []
        
        for i, impl in enumerate(implicants):
            impl_display = self._implicant_to_display(impl)
            is_essential = False
            
            for assignment in self.on_sets:
                binary = self._assignment_to_binary(assignment)
                if self._covers(impl, binary):
                    # Проверяем, покрывает ли эту конституэнту только эта импликанта
                    covered_by_others = False
                    for j, other in enumerate(implicants):
                        if i != j and self._covers(other, binary):
                            covered_by_others = True
                            break
                    if not covered_by_others:
                        is_essential = True
                        break
            
            if is_essential:
                essential.append(impl)
                print(f"  {impl_display} = 1, когда {self._get_condition(impl)} - не лишняя")
            else:
                print(f"  {impl_display} = 1, когда {self._get_condition(impl)} - лишняя")
        
        return essential if essential else implicants
    
    def _get_condition(self, impl):
        """Получает условие для импликанты"""
        conditions = []
        for i, val in enumerate(impl):
            if val == '0':
                conditions.append(f"{self.variables[i]}=0")
            elif val == '1':
                conditions.append(f"{self.variables[i]}=1")
        return ", ".join(conditions)
    
    def minimization_calculated(self):
        """
        Расчетный метод минимизации с выводом этапов склеивания.
        """
        print("\n" + "=" * 70)
        print("РАСЧЕТНЫЙ МЕТОД (МЕТОД КВАЙНА)")
        print("=" * 70)
        
        # Получаем простые импликанты с выводом
        implicants = self._get_prime_implicants(verbose=True)
        
        if not implicants:
            return "0", []
        
        print(f"\nПроверка на лишние импликанты:")
        essential_impls = self._remove_redundant_implicants_with_output(implicants)
        
        # Преобразуем в выражение
        terms = [self._implicant_to_term(impl) for impl in essential_impls]
        sorted_terms = sorted(terms)
        result = " | ".join(sorted_terms)
        
        print(f"\nРезультат после удаления лишних импликант:")
        print(f"  {result}")
        
        return result, essential_impls
    
    def minimization_table(self):
        """
        Расчетно-табличный метод минимизации с выводом таблицы.
        """
        print("\n" + "=" * 70)
        print("РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД")
        print("=" * 70)
        
        # Получаем простые импликанты БЕЗ вывода (чтобы не дублировать)
        implicants = self._get_prime_implicants(verbose=False)
        
        if not implicants or not self.on_sets:
            return "0", [], []
        
        print(f"\nПостроение таблицы покрытия:")
        
        # Получаем конституэнты в читаемом виде
        constitutents = []
        for assignment in self.on_sets:
            binary = self._assignment_to_binary(assignment)
            constitutents.append(self._binary_to_term(binary))
        
        # Строим таблицу покрытия
        cover_table = []
        for impl in implicants:
            row = []
            for assignment in self.on_sets:
                binary = self._assignment_to_binary(assignment)
                covers = 1 if self._covers(impl, binary) else 0
                row.append(covers)
            cover_table.append(row)
        
        # Выводим таблицу
        print(f"\nТаблица покрытия:")
        
        # Определяем ширину столбцов
        impl_width = max(len(self._implicant_to_display(impl)) for impl in implicants) + 2
        const_width = max(len(term) for term in constitutents) + 2
        
        # Заголовок
        header = " " * impl_width + "|"
        for const in constitutents:
            header += f" {const:^{const_width-2}} |"
        print(header)
        print("-" * len(header))
        
        # Строки таблицы
        for i, impl in enumerate(implicants):
            impl_display = self._implicant_to_display(impl)
            row = f" {impl_display:^{impl_width-2}} |"
            for j, val in enumerate(cover_table[i]):
                if val == 1:
                    row += f" {'X':^{const_width-2}} |"
                else:
                    row += f" {' ':^{const_width-2}} |"
            print(row)
        
        print("-" * len(header))
        
        # Находим ядровые импликанты
        core_indices = set()
        for j in range(len(self.on_sets)):
            covering = []
            for i in range(len(implicants)):
                if cover_table[i][j] == 1:
                    covering.append(i)
            if len(covering) == 1:
                core_indices.add(covering[0])
        
        core_implicants = [implicants[i] for i in core_indices]
        
        print(f"\nЯдровые импликанты:")
        for impl in core_implicants:
            print(f"  {self._implicant_to_display(impl)}")
        
        # Формируем результат
        terms = [self._implicant_to_term(impl) for impl in core_implicants]
        sorted_terms = sorted(terms)
        result = " | ".join(sorted_terms)
        
        print(f"\nРезультат минимизации:")
        print(f"  {result}")
        
        return result, core_implicants, cover_table
    
    def minimization_karnaugh(self):
        """
        Табличный метод (карты Карно) с выводом карты.
        """
        print("\n" + "=" * 70)
        print("ТАБЛИЧНЫЙ МЕТОД (КАРТА КАРНО)")
        print("=" * 70)
        
        # Строим карту Карно
        if self.n == 2:
            k_map = self._build_karnaugh_2()
            self._print_karnaugh_2(k_map)
            groups = self._find_groups_2(k_map)
        elif self.n == 3:
            k_map = self._build_karnaugh_3()
            self._print_karnaugh_3(k_map)
            groups = self._find_groups_3(k_map)
        elif self.n == 4:
            k_map = self._build_karnaugh_4()
            self._print_karnaugh_4(k_map)
            groups = self._find_groups_4(k_map)
        else:
            return "Метод Карно поддерживается для 2-4 переменных", []
        
        print(f"\nВыделенные области:")
        for i, group in enumerate(groups, 1):
            term = self._group_to_term(group)
            print(f"  Область {i}: {self._group_description(group)} => {term}")
        
        # Формируем выражение
        terms = []
        for group in groups:
            term = self._group_to_term(group)
            if term and term not in terms:
                terms.append(term)
        
        if not terms:
            return "0", k_map
        
        sorted_terms = sorted(terms)
        result = " ∨ ".join(sorted_terms)
        
        print(f"\nМинимизированная ДНФ:")
        print(f"  {result}")
        
        return result, k_map
    
    def _build_karnaugh_2(self):
        """Строит карту Карно для 2 переменных"""
        k_map = [[0, 0], [0, 0]]
        
        for assignment in self.on_sets:
            a = 1 if assignment[self.variables[0]] else 0
            b = 1 if assignment[self.variables[1]] else 0
            if a == 0 and b == 0:
                k_map[0][0] = 1
            elif a == 0 and b == 1:
                k_map[0][1] = 1
            elif a == 1 and b == 1:
                k_map[1][1] = 1
            elif a == 1 and b == 0:
                k_map[1][0] = 1
        
        return k_map
    
    def _build_karnaugh_3(self):
        """Строит карту Карно для 3 переменных"""
        k_map = [[0, 0, 0, 0], [0, 0, 0, 0]]
        
        for assignment in self.on_sets:
            a = 1 if assignment[self.variables[0]] else 0
            b = 1 if assignment[self.variables[1]] else 0
            c = 1 if assignment[self.variables[2]] else 0
            
            if b == 0 and c == 0:
                idx = 0
            elif b == 0 and c == 1:
                idx = 1
            elif b == 1 and c == 1:
                idx = 2
            else:
                idx = 3
            
            k_map[a][idx] = 1
        
        return k_map
    
    def _build_karnaugh_4(self):
        """Строит карту Карно для 4 переменных"""
        k_map = [[0, 0, 0, 0] for _ in range(4)]
        
        for assignment in self.on_sets:
            a = 1 if assignment[self.variables[0]] else 0
            b = 1 if assignment[self.variables[1]] else 0
            c = 1 if assignment[self.variables[2]] else 0
            d = 1 if assignment[self.variables[3]] else 0
            
            if a == 0 and b == 0:
                row = 0
            elif a == 0 and b == 1:
                row = 1
            elif a == 1 and b == 1:
                row = 2
            else:
                row = 3
            
            if c == 0 and d == 0:
                col = 0
            elif c == 0 and d == 1:
                col = 1
            elif c == 1 and d == 1:
                col = 2
            else:
                col = 3
            
            k_map[row][col] = 1
        
        return k_map
    
    def _print_karnaugh_2(self, k_map):
        """Выводит карту Карно для 2 переменных"""
        print(f"\nКарта Карно для {self.variables[0]}, {self.variables[1]}:")
        print(f"      {self.variables[1]}=0  {self.variables[1]}=1")
        print(f"{self.variables[0]}=0    {k_map[0][0]}     {k_map[0][1]}")
        print(f"{self.variables[0]}=1    {k_map[1][0]}     {k_map[1][1]}")
    
    def _print_karnaugh_3(self, k_map):
        """Выводит карту Карно для 3 переменных"""
        print(f"\nКарта Карно для {self.variables[0]}, {self.variables[1]}, {self.variables[2]}:")
        print(f"        {self.variables[1]}{self.variables[2]}=00  {self.variables[1]}{self.variables[2]}=01  {self.variables[1]}{self.variables[2]}=11  {self.variables[1]}{self.variables[2]}=10")
        print(f"{self.variables[0]}=0        {k_map[0][0]}       {k_map[0][1]}       {k_map[0][2]}       {k_map[0][3]}")
        print(f"{self.variables[0]}=1        {k_map[1][0]}       {k_map[1][1]}       {k_map[1][2]}       {k_map[1][3]}")
    
    def _print_karnaugh_4(self, k_map):
        """Выводит карту Карно для 4 переменных"""
        print(f"\nКарта Карно для {self.variables[0]}, {self.variables[1]}, {self.variables[2]}, {self.variables[3]}:")
        print(f"        {self.variables[2]}{self.variables[3]}=00  {self.variables[2]}{self.variables[3]}=01  {self.variables[2]}{self.variables[3]}=11  {self.variables[2]}{self.variables[3]}=10")
        print(f"{self.variables[0]}{self.variables[1]}=00    {k_map[0][0]}       {k_map[0][1]}       {k_map[0][2]}       {k_map[0][3]}")
        print(f"{self.variables[0]}{self.variables[1]}=01    {k_map[1][0]}       {k_map[1][1]}       {k_map[1][2]}       {k_map[1][3]}")
        print(f"{self.variables[0]}{self.variables[1]}=11    {k_map[2][0]}       {k_map[2][1]}       {k_map[2][2]}       {k_map[2][3]}")
        print(f"{self.variables[0]}{self.variables[1]}=10    {k_map[3][0]}       {k_map[3][1]}       {k_map[3][2]}       {k_map[3][3]}")
    
    def _find_groups_2(self, k_map):
        """Находит группы в карте Карно 2x2"""
        groups = []
        
        # Проверяем группу из 4 клеток
        if all(k_map[i][j] == 1 for i in range(2) for j in range(2)):
            groups.append([(0,0), (0,1), (1,0), (1,1)])
            return groups
        
        # Проверяем группы из 2 клеток
        for i in range(2):
            for j in range(2):
                if k_map[i][j] == 1:
                    # Проверяем соседа справа
                    if k_map[i][(j+1)%2] == 1:
                        groups.append([(i, j), (i, (j+1)%2)])
                    # Проверяем соседа снизу
                    elif k_map[(i+1)%2][j] == 1:
                        groups.append([(i, j), ((i+1)%2, j)])
                    else:
                        groups.append([(i, j)])
        
        # Удаляем дубликаты
        unique_groups = []
        for group in groups:
            if sorted(group) not in [sorted(g) for g in unique_groups]:
                unique_groups.append(group)
        
        return unique_groups
    
    def _find_groups_3(self, k_map):
        """Находит группы в карте Карно 2x4"""
        groups = []
        used = [[False] * 4 for _ in range(2)]
        
        # Проверяем группы из 8 клеток (вся карта)
        if all(k_map[i][j] == 1 for i in range(2) for j in range(4)):
            groups.append([(i, j) for i in range(2) for j in range(4)])
            return groups
        
        # Проверяем группы из 4 клеток
        # По горизонтали (2x2)
        for i in range(2):
            for j in range(4):
                if not used[i][j] and k_map[i][j] == 1:
                    # Ищем группу 2x2
                    if k_map[i][(j+1)%4] == 1 and k_map[(i+1)%2][j] == 1 and k_map[(i+1)%2][(j+1)%4] == 1:
                        group = [(i, j), (i, (j+1)%4), ((i+1)%2, j), ((i+1)%2, (j+1)%4)]
                        for pos in group:
                            used[pos[0]][pos[1]] = True
                        groups.append(group)
        
        # Проверяем группы из 2 клеток
        for i in range(2):
            for j in range(4):
                if k_map[i][j] == 1 and not used[i][j]:
                    # По горизонтали
                    if k_map[i][(j+1)%4] == 1 and not used[i][(j+1)%4]:
                        groups.append([(i, j), (i, (j+1)%4)])
                        used[i][j] = used[i][(j+1)%4] = True
                    # По вертикали
                    elif k_map[(i+1)%2][j] == 1 and not used[(i+1)%2][j]:
                        groups.append([(i, j), ((i+1)%2, j)])
                        used[i][j] = used[(i+1)%2][j] = True
                    else:
                        groups.append([(i, j)])
                        used[i][j] = True
        
        return groups
    
    def _find_groups_4(self, k_map):
        """Находит группы в карте Карно 4x4"""
        groups = []
        used = [[False] * 4 for _ in range(4)]
        
        # Проверяем группы из 16 клеток (вся карта)
        if all(k_map[i][j] == 1 for i in range(4) for j in range(4)):
            groups.append([(i, j) for i in range(4) for j in range(4)])
            return groups
        
        # Проверяем группы из 8 клеток
        for i in range(4):
            for j in range(4):
                if not used[i][j] and k_map[i][j] == 1:
                    # Ищем группу 2x4
                    if i + 1 < 4:
                        if all(k_map[i][j2] == 1 and k_map[i+1][j2] == 1 for j2 in range(4)):
                            group = [(i, j2) for j2 in range(4)] + [(i+1, j2) for j2 in range(4)]
                            for pos in group:
                                used[pos[0]][pos[1]] = True
                            groups.append(group)
                            continue
        
        # Проверяем группы из 4 клеток
        for i in range(4):
            for j in range(4):
                if k_map[i][j] == 1 and not used[i][j]:
                    # Ищем группу 2x2
                    if i + 1 < 4 and j + 1 < 4:
                        if all(k_map[i+di][j+dj] == 1 for di in range(2) for dj in range(2)):
                            group = [(i+di, j+dj) for di in range(2) for dj in range(2)]
                            for pos in group:
                                used[pos[0]][pos[1]] = True
                            groups.append(group)
                            continue
        
        # Проверяем оставшиеся единицы
        for i in range(4):
            for j in range(4):
                if k_map[i][j] == 1 and not used[i][j]:
                    groups.append([(i, j)])
        
        return groups
    
    def _group_description(self, group):
        """Возвращает описание группы для вывода"""
        if len(group) == 1:
            return "одиночная клетка"
        elif len(group) == 2:
            return "пара клеток"
        elif len(group) == 4:
            return "прямоугольник 2x2"
        elif len(group) == 8:
            return "прямоугольник 2x4"
        else:
            return f"группа из {len(group)} клеток"
    
    def _group_to_term(self, group):
        """Преобразует группу в терм"""
        if not group:
            return None
        
        # Для 2 переменных
        if self.n == 2:
            rows = set(p[0] for p in group)
            cols = set(p[1] for p in group)
            
            term_parts = []
            if len(rows) == 1:
                row = next(iter(rows))
                if row == 0:
                    term_parts.append(f"¬{self.variables[0]}")
                else:
                    term_parts.append(self.variables[0])
            
            if len(cols) == 1:
                col = next(iter(cols))
                if col == 0:
                    term_parts.append(f"¬{self.variables[1]}")
                else:
                    term_parts.append(self.variables[1])
            
            if not term_parts:
                return "1"
            return "&".join(term_parts) if len(term_parts) > 1 else term_parts[0]
        
        # Для 3 переменных
        elif self.n == 3:
            rows = set(p[0] for p in group)
            cols = set(p[1] for p in group)
            
            term_parts = []
            
            if len(rows) == 1:
                row = next(iter(rows))
                if row == 0:
                    term_parts.append(f"¬{self.variables[0]}")
                else:
                    term_parts.append(self.variables[0])
            
            # Для столбцов нужно определить, какие переменные фиксированы
            if len(cols) == 1:
                col = next(iter(cols))
                if col == 0:
                    term_parts.append(f"¬{self.variables[1]} & ¬{self.variables[2]}")
                elif col == 1:
                    term_parts.append(f"¬{self.variables[1]} & {self.variables[2]}")
                elif col == 2:
                    term_parts.append(f"{self.variables[1]} & {self.variables[2]}")
                elif col == 3:
                    term_parts.append(f"{self.variables[1]} & ¬{self.variables[2]}")
            elif len(cols) == 2:
                # Проверяем, какие биты фиксированы
                if 0 in cols and 1 in cols:
                    term_parts.append(f"¬{self.variables[1]}")
                elif 2 in cols and 3 in cols:
                    term_parts.append(self.variables[1])
                elif 0 in cols and 3 in cols:
                    term_parts.append(f"¬{self.variables[2]}")
                elif 1 in cols and 2 in cols:
                    term_parts.append(self.variables[2])
            
            if not term_parts:
                return "1"
            return "&".join(term_parts) if len(term_parts) > 1 else term_parts[0]
        
        # Для 4 переменных
        elif self.n == 4:
            rows = set(p[0] for p in group)
            cols = set(p[1] for p in group)
            
            term_parts = []
            
            # Анализируем строки (переменные a,b)
            if len(rows) == 1:
                row = next(iter(rows))
                if row == 0:
                    term_parts.append(f"¬{self.variables[0]} & ¬{self.variables[1]}")
                elif row == 1:
                    term_parts.append(f"¬{self.variables[0]} & {self.variables[1]}")
                elif row == 2:
                    term_parts.append(f"{self.variables[0]} & {self.variables[1]}")
                elif row == 3:
                    term_parts.append(f"{self.variables[0]} & ¬{self.variables[1]}")
            elif len(rows) == 2:
                if 0 in rows and 1 in rows:
                    term_parts.append(f"¬{self.variables[0]}")
                elif 2 in rows and 3 in rows:
                    term_parts.append(self.variables[0])
                elif 0 in rows and 3 in rows:
                    term_parts.append(f"¬{self.variables[1]}")
                elif 1 in rows and 2 in rows:
                    term_parts.append(self.variables[1])
            
            # Анализируем столбцы (переменные c,d)
            if len(cols) == 1:
                col = next(iter(cols))
                if col == 0:
                    term_parts.append(f"¬{self.variables[2]} & ¬{self.variables[3]}")
                elif col == 1:
                    term_parts.append(f"¬{self.variables[2]} & {self.variables[3]}")
                elif col == 2:
                    term_parts.append(f"{self.variables[2]} & {self.variables[3]}")
                elif col == 3:
                    term_parts.append(f"{self.variables[2]} & ¬{self.variables[3]}")
            elif len(cols) == 2:
                if 0 in cols and 1 in cols:
                    term_parts.append(f"¬{self.variables[2]}")
                elif 2 in cols and 3 in cols:
                    term_parts.append(self.variables[2])
                elif 0 in cols and 3 in cols:
                    term_parts.append(f"¬{self.variables[3]}")
                elif 1 in cols and 2 in cols:
                    term_parts.append(self.variables[3])
            
            if not term_parts:
                return "1"
            return "&".join(term_parts) if len(term_parts) > 1 else term_parts[0]
        
        return "1"