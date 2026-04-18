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

    # ---------- Вспомогательные методы ----------
    def _assignment_to_binary(self, assignment):
        return ''.join([str(int(assignment[var])) for var in self.variables])

    def _assignment_to_binary_sknf(self, assignment):
        return ''.join([str(int(assignment[var])) for var in self.variables])

    def _binary_to_term(self, binary):
        term_parts = []
        for i, val in enumerate(binary):
            if val == '0':
                term_parts.append(f'¬{self.variables[i]}')
            elif val == '1':
                term_parts.append(self.variables[i])
        return '(' + ''.join(term_parts) + ')'

    def _term_to_sknf(self, binary):
        term_parts = []
        for i, val in enumerate(binary):
            if val == '0':
                term_parts.append(self.variables[i])
            else:
                term_parts.append(f'!{self.variables[i]}')
        return '(' + '|'.join(term_parts) + ')'

    def _implicant_to_term(self, implicant):
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

    def _implicant_to_cnf_term(self, implicant):
        if implicant.count('X') == self.n:
            return "0"
        term_parts = []
        for i, val in enumerate(implicant):
            if val == '0':
                term_parts.append(self.variables[i])
            elif val == '1':
                term_parts.append(f"!{self.variables[i]}")
        term_parts.sort()
        return "|".join(term_parts)

    def _implicant_to_display(self, implicant):
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
        return impl1[:pos] + 'X' + impl1[pos+1:]

    def _covers(self, implicant, binary):
        for i in range(len(implicant)):
            if implicant[i] != 'X' and implicant[i] != binary[i]:
                return False
        return True

    def _get_condition(self, impl):
        conditions = []
        for i, val in enumerate(impl):
            if val == '0':
                conditions.append(f"{self.variables[i]}=0")
            elif val == '1':
                conditions.append(f"{self.variables[i]}=1")
        return ", ".join(conditions)

    # ---------- Внутренние методы получения простых импликант ----------
    def _get_prime_implicants(self, verbose=False):
        current_impls = [self._assignment_to_binary(a) for a in self.on_sets]
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
            for i in range(len(current_impls)):
                for j in range(i + 1, len(current_impls)):
                    can_glue, pos = self._can_glue(current_impls[i], current_impls[j])
                    if can_glue:
                        glued = self._glue(current_impls[i], current_impls[j], pos)
                        used[i] = used[j] = True
                        if glued not in next_impls:
                            next_impls.append(glued)
                            glued_pairs.append((current_impls[i], current_impls[j], glued, pos))
            if verbose:
                for impl1, impl2, glued, pos in glued_pairs:
                    term1 = self._binary_to_term(impl1)
                    term2 = self._binary_to_term(impl2)
                    res = self._implicant_to_display(glued)
                    var = self.variables[pos]
                    print(f"  {term1} ∨ {term2} => ({res})  [по переменной {var}]")
            for i in range(len(current_impls)):
                if not used[i] and current_impls[i] not in all_implicants:
                    all_implicants.append(current_impls[i])
            if not next_impls:
                break
            if verbose:
                print(f"\nРезультат склеивания уровня {level}:")
                result_terms = [self._implicant_to_display(impl) for impl in next_impls]
                print(f"  {', '.join(result_terms)}")
                print(f"  {[tuple('X' if c=='X' else int(c) for c in impl) for impl in next_impls]}")
                print(f"\nЭтап склеивания (уровень {level+1}):")
            current_impls = next_impls
            level += 1
        for impl in current_impls:
            if impl not in all_implicants:
                all_implicants.append(impl)
        if verbose:
            print(f"\nРезультат после всех склеиваний:")
            result_terms = [self._implicant_to_display(impl) for impl in all_implicants]
            print(f"  {', '.join(result_terms)}")
        return all_implicants

    def _get_prime_implicants_cnf(self, verbose=False):
        off_sets = self.truth_table.get_off_sets()
        current_impls = [self._assignment_to_binary_sknf(a) for a in off_sets]
        if not current_impls:
            return []
        all_implicants = []
        level = 1
        if verbose:
            print(f"\nИсходная СКНФ:")
            terms = [self._term_to_sknf(impl) for impl in current_impls]
            print(f"  {', '.join(terms)}")
            print(f"  {[tuple(int(b) for b in impl) for impl in current_impls]}")
            print(f"\nЭтап склеивания (уровень {level}):")
        while True:
            used = [False] * len(current_impls)
            next_impls = []
            glued_pairs = []
            for i in range(len(current_impls)):
                for j in range(i + 1, len(current_impls)):
                    can_glue, pos = self._can_glue(current_impls[i], current_impls[j])
                    if can_glue:
                        glued = self._glue(current_impls[i], current_impls[j], pos)
                        used[i] = used[j] = True
                        if glued not in next_impls:
                            next_impls.append(glued)
                            glued_pairs.append((current_impls[i], current_impls[j], glued, pos))
            if verbose:
                for impl1, impl2, glued, pos in glued_pairs:
                    term1 = self._term_to_sknf(impl1)
                    term2 = self._term_to_sknf(impl2)
                    res = self._implicant_to_display(glued)
                    var = self.variables[pos]
                    print(f"  {term1} & {term2} => ({res})  [по переменной {var}]")
            for i in range(len(current_impls)):
                if not used[i] and current_impls[i] not in all_implicants:
                    all_implicants.append(current_impls[i])
            if not next_impls:
                break
            if verbose:
                print(f"\nРезультат склеивания уровня {level}:")
                result_terms = [self._implicant_to_display(impl) for impl in next_impls]
                print(f"  {', '.join(result_terms)}")
                print(f"  {[tuple('X' if c=='X' else int(c) for c in impl) for impl in next_impls]}")
                print(f"\nЭтап склеивания (уровень {level+1}):")
            current_impls = next_impls
            level += 1
        for impl in current_impls:
            if impl not in all_implicants:
                all_implicants.append(impl)
        if verbose:
            print(f"\nРезультат после всех склеиваний:")
            result_terms = [self._implicant_to_display(impl) for impl in all_implicants]
            print(f"  {', '.join(result_terms)}")
        return all_implicants

    # ---------- Удаление лишних импликант ----------
    def _remove_redundant_implicants_with_output(self, implicants):
        if not implicants or not self.on_sets:
            return implicants
        essential = []
        for i, impl in enumerate(implicants):
            impl_disp = self._implicant_to_display(impl)
            is_essential = False
            for assignment in self.on_sets:
                binary = self._assignment_to_binary(assignment)
                if self._covers(impl, binary):
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
                print(f"  {impl_disp} = 1, когда {self._get_condition(impl)} - не лишняя")
            else:
                print(f"  {impl_disp} = 1, когда {self._get_condition(impl)} - лишняя")
        return essential if essential else implicants

    def _remove_redundant_implicants_cnf(self, implicants):
        off_sets = self.truth_table.get_off_sets()
        if not implicants or not off_sets:
            return implicants
        essential = []
        for i, impl in enumerate(implicants):
            impl_disp = self._implicant_to_display(impl)
            is_essential = False
            for assignment in off_sets:
                binary = self._assignment_to_binary_sknf(assignment)
                if self._covers(impl, binary):
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
                print(f"  {impl_disp} = 0, когда {self._get_condition(impl)} - не лишний")
            else:
                print(f"  {impl_disp} = 0, когда {self._get_condition(impl)} - лишний")
        return essential if essential else implicants

    # ---------- Публичные методы для ДНФ ----------
    def minimization_calculated(self):
        print("\n" + "=" * 70)
        print("РАСЧЕТНЫЙ МЕТОД (МЕТОД КВАЙНА) ДЛЯ ДНФ")
        print("=" * 70)
        implicants = self._get_prime_implicants(verbose=True)
        if not implicants:
            return "0", []
        print(f"\nПроверка на лишние импликанты:")
        essential = self._remove_redundant_implicants_with_output(implicants)
        terms = [self._implicant_to_term(impl) for impl in essential]
        result = " | ".join(sorted(terms))
        print(f"\nРезультат после удаления лишних импликант:")
        print(f"  {result}")
        return result, essential

    def minimization_table(self):
        print("\n" + "=" * 70)
        print("РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД ДЛЯ ДНФ")
        print("=" * 70)
        implicants = self._get_prime_implicants(verbose=False)
        if not implicants or not self.on_sets:
            return "0", [], []
        print(f"\nПостроение таблицы покрытия:")
        constitutents = [self._binary_to_term(self._assignment_to_binary(a)) for a in self.on_sets]
        cover_table = []
        for impl in implicants:
            row = [1 if self._covers(impl, self._assignment_to_binary(a)) else 0 for a in self.on_sets]
            cover_table.append(row)
        impl_width = max(len(self._implicant_to_display(impl)) for impl in implicants) + 2
        const_width = max(len(term) for term in constitutents) + 2
        header = " " * impl_width + "|"
        for const in constitutents:
            header += f" {const:^{const_width-2}} |"
        print(header)
        print("-" * len(header))
        for i, impl in enumerate(implicants):
            impl_disp = self._implicant_to_display(impl)
            row = f" {impl_disp:^{impl_width-2}} |"
            for val in cover_table[i]:
                row += f" {'X':^{const_width-2}} |" if val else f" {' ':^{const_width-2}} |"
            print(row)
        print("-" * len(header))
        core_indices = set()
        for j in range(len(self.on_sets)):
            covering = [i for i in range(len(implicants)) if cover_table[i][j]]
            if len(covering) == 1:
                core_indices.add(covering[0])
        core_implicants = [implicants[i] for i in core_indices]
        print(f"\nЯдровые импликанты:")
        for impl in core_implicants:
            print(f"  {self._implicant_to_display(impl)}")
        terms = [self._implicant_to_term(impl) for impl in core_implicants]
        result = " | ".join(sorted(terms))
        print(f"\nРезультат минимизации ДНФ:")
        print(f"  {result}")
        return result, core_implicants, cover_table

    # ---------- Публичные методы для КНФ ----------
    def minimization_calculated_cnf(self):
        print("\n" + "=" * 70)
        print("РАСЧЕТНЫЙ МЕТОД ДЛЯ КНФ (МЕТОД КВАЙНА)")
        print("=" * 70)
        implicants = self._get_prime_implicants_cnf(verbose=True)
        if not implicants:
            return "1", []
        print(f"\nПроверка на лишние импликанты:")
        essential = self._remove_redundant_implicants_cnf(implicants)
        terms = [self._implicant_to_cnf_term(impl) for impl in essential]
        result = " & ".join(sorted(terms))
        print(f"\nРезультат после удаления лишних импликант:")
        print(f"  {result}")
        return result, essential

    def minimization_table_cnf(self):
        print("\n" + "=" * 70)
        print("РАСЧЕТНО-ТАБЛИЧНЫЙ МЕТОД ДЛЯ КНФ")
        print("=" * 70)
        implicants = self._get_prime_implicants_cnf(verbose=False)
        off_sets = self.truth_table.get_off_sets()
        if not implicants or not off_sets:
            return "1", [], []
        print(f"\nПостроение таблицы покрытия:")
        constitutents = [self._term_to_sknf(self._assignment_to_binary_sknf(a)) for a in off_sets]
        cover_table = []
        for impl in implicants:
            row = [1 if self._covers(impl, self._assignment_to_binary_sknf(a)) else 0 for a in off_sets]
            cover_table.append(row)
        impl_width = max(len(self._implicant_to_display(impl)) for impl in implicants) + 2
        const_width = max(len(term) for term in constitutents) + 2
        header = " " * impl_width + "|"
        for const in constitutents:
            header += f" {const:^{const_width-2}} |"
        print(header)
        print("-" * len(header))
        for i, impl in enumerate(implicants):
            impl_disp = self._implicant_to_display(impl)
            row = f" {impl_disp:^{impl_width-2}} |"
            for val in cover_table[i]:
                row += f" {'X':^{const_width-2}} |" if val else f" {' ':^{const_width-2}} |"
            print(row)
        print("-" * len(header))
        core_indices = set()
        for j in range(len(off_sets)):
            covering = [i for i in range(len(implicants)) if cover_table[i][j]]
            if len(covering) == 1:
                core_indices.add(covering[0])
        core_implicants = [implicants[i] for i in core_indices]
        print(f"\nЯдровые импликанты:")
        for impl in core_implicants:
            print(f"  {self._implicant_to_display(impl)}")
        terms = [self._implicant_to_cnf_term(impl) for impl in core_implicants]
        result = " & ".join(sorted(terms))
        print(f"\nРезультат минимизации КНФ:")
        print(f"  {result}")
        return result, core_implicants, cover_table

    # ---------- Карты Карно для ДНФ ----------
    def minimization_karnaugh(self):
        print("\n" + "=" * 70)
        print("ТАБЛИЧНЫЙ МЕТОД ДЛЯ ДНФ (КАРТА КАРНО)")
        print("=" * 70)
        
        # Обработка константных функций
        if self.n == 1:
            if len(self.on_sets) == 0:
                return "0", []
            elif len(self.on_sets) == 2:
                return "1", []
            elif self.on_sets[0][self.variables[0]] == True:
                return self.variables[0], []
            else:
                return f"!{self.variables[0]}", []
        
        # Для 5 переменных
        if self.n == 5:
            k_map = self._build_karnaugh_5()
            self._print_karnaugh_5(k_map)
            
            cells = []
            for i in range(4):
                for j in range(8):
                    if k_map[i][j] == 1:
                        cells.append((i, j))
            
            if not cells:
                return "0", k_map
            
            rectangles = self._get_all_rectangles_5(k_map)
            cover = self._minimal_cover_exact_5(cells, rectangles)
            
            print(f"\nВыделенные области (единицы):")
            terms = []
            for i, rect in enumerate(cover, 1):
                term = self._group_to_dnf_term_5(rect)
                if term:
                    term = term.replace(" & ", "&")
                    terms.append(term)
                    print(f"  Область {i}: группа из {len(rect)} клеток => {term}")
            result = " ∨ ".join(sorted(terms))
            print(f"\nМинимизированная ДНФ:")
            print(f"  {result}")
            return result, k_map
        
        if self.n not in (2,3,4):
            return "Метод Карно поддерживается для 2-5 переменных", []
        
        # Для 2-4 переменных
        if self.n == 2:
            k_map = self._build_karnaugh_2()
            self._print_karnaugh_2(k_map)
        elif self.n == 3:
            k_map = self._build_karnaugh_3()
            self._print_karnaugh_3(k_map)
        else:
            k_map = self._build_karnaugh_4()
            self._print_karnaugh_4(k_map)
        
        cells = [(i,j) for i in range(len(k_map)) for j in range(len(k_map[0])) if k_map[i][j]==1]
        if not cells:
            return "0", k_map
        
        rectangles = self._get_all_rectangles(k_map)
        cover = self._minimal_cover_exact(cells, rectangles)
        
        print(f"\nВыделенные области (единицы):")
        terms = []
        for i, rect in enumerate(cover, 1):
            term = self._group_to_dnf_term(rect)
            if term:
                term = term.replace(" & ", "&")
                terms.append(term)
                print(f"  Область {i}: {self._group_description(rect)} => {term}")
        result = " ∨ ".join(sorted(terms))
        print(f"\nМинимизированная ДНФ:")
        print(f"  {result}")
        return result, k_map

    # ---------- Карты Карно для КНФ ----------
    def minimization_karnaugh_cnf(self):
        print("\n" + "=" * 70)
        print("ТАБЛИЧНЫЙ МЕТОД ДЛЯ КНФ (КАРТА КАРНО)")
        print("=" * 70)
        
        off_sets = self.truth_table.get_off_sets()
        
        # Обработка константных функций
        if self.n == 1:
            if len(off_sets) == 0:
                return "1", []
            elif len(off_sets) == 2:
                return "0", []
            elif off_sets[0][self.variables[0]] == True:
                return f"!{self.variables[0]}", []
            else:
                return self.variables[0], []
        
        # Для 5 переменных
        if self.n == 5:
            original_on_sets = self.on_sets
            self.on_sets = off_sets
            k_map = self._build_karnaugh_5()
            self._print_karnaugh_5(k_map)
            self.on_sets = original_on_sets
            
            cells = []
            for i in range(4):
                for j in range(8):
                    if k_map[i][j] == 1:
                        cells.append((i, j))
            
            if not cells:
                return "1", k_map
            
            rectangles = self._get_all_rectangles_5(k_map)
            cover = self._minimal_cover_exact_5(cells, rectangles)
            
            print(f"\nВыделенные области (нули функции):")
            terms = []
            for i, rect in enumerate(cover, 1):
                disjunct = self._group_to_cnf_term_5(rect)
                if disjunct:
                    terms.append(disjunct)
                    print(f"  Область {i}: группа из {len(rect)} клеток => {disjunct}")
            result = " & ".join(sorted(terms))
            print(f"\nМинимизированная КНФ:")
            print(f"  {result}")
            return result, k_map
        
        if self.n not in (2,3,4):
            return "Метод Карно поддерживается для 2-5 переменных", []
        
        # Для 2-4 переменных
        original_on_sets = self.on_sets
        self.on_sets = off_sets
        
        if self.n == 2:
            k_map = self._build_karnaugh_2()
            self._print_karnaugh_2(k_map)
        elif self.n == 3:
            k_map = self._build_karnaugh_3()
            self._print_karnaugh_3(k_map)
        else:
            k_map = self._build_karnaugh_4()
            self._print_karnaugh_4(k_map)
        
        self.on_sets = original_on_sets
        
        cells = [(i,j) for i in range(len(k_map)) for j in range(len(k_map[0])) if k_map[i][j]==1]
        if not cells:
            return "1", k_map
        
        rectangles = self._get_all_rectangles(k_map)
        cover = self._minimal_cover_exact(cells, rectangles)
        
        print(f"\nВыделенные области (нули функции):")
        terms = []
        for i, rect in enumerate(cover, 1):
            disjunct = self._group_to_cnf_term(rect)
            if disjunct:
                terms.append(disjunct)
                print(f"  Область {i}: {self._group_description(rect)} => {disjunct}")
        result = " & ".join(sorted(terms))
        print(f"\nМинимизированная КНФ:")
        print(f"  {result}")
        return result, k_map

    # ---------- Построение карт Карно (2-4 переменные) ----------
    def _build_karnaugh_2(self):
        k_map = [[0,0],[0,0]]
        for a in self.on_sets:
            x = 1 if a[self.variables[0]] else 0
            y = 1 if a[self.variables[1]] else 0
            if x==0 and y==0: k_map[0][0]=1
            elif x==0 and y==1: k_map[0][1]=1
            elif x==1 and y==1: k_map[1][1]=1
            elif x==1 and y==0: k_map[1][0]=1
        return k_map

    def _build_karnaugh_3(self):
        k_map = [[0,0,0,0],[0,0,0,0]]
        for a in self.on_sets:
            x = 1 if a[self.variables[0]] else 0
            y = 1 if a[self.variables[1]] else 0
            z = 1 if a[self.variables[2]] else 0
            if y==0 and z==0: col=0
            elif y==0 and z==1: col=1
            elif y==1 and z==1: col=2
            else: col=3
            k_map[x][col]=1
        return k_map

    def _build_karnaugh_4(self):
        k_map = [[0,0,0,0] for _ in range(4)]
        for a in self.on_sets:
            a_val = 1 if a[self.variables[0]] else 0
            b_val = 1 if a[self.variables[1]] else 0
            c_val = 1 if a[self.variables[2]] else 0
            d_val = 1 if a[self.variables[3]] else 0
            if a_val==0 and b_val==0: row=0
            elif a_val==0 and b_val==1: row=1
            elif a_val==1 and b_val==1: row=2
            else: row=3
            if c_val==0 and d_val==0: col=0
            elif c_val==0 and d_val==1: col=1
            elif c_val==1 and d_val==1: col=2
            else: col=3
            k_map[row][col]=1
        return k_map

    def _print_karnaugh_2(self, k_map):
        print(f"\nКарта Карно для {self.variables[0]}, {self.variables[1]}:")
        print(f"      {self.variables[1]}=0  {self.variables[1]}=1")
        print(f"{self.variables[0]}=0    {k_map[0][0]}     {k_map[0][1]}")
        print(f"{self.variables[0]}=1    {k_map[1][0]}     {k_map[1][1]}")

    def _print_karnaugh_3(self, k_map):
        print(f"\nКарта Карно для {self.variables[0]}, {self.variables[1]}, {self.variables[2]}:")
        print(f"        {self.variables[1]}{self.variables[2]}=00  {self.variables[1]}{self.variables[2]}=01  {self.variables[1]}{self.variables[2]}=11  {self.variables[1]}{self.variables[2]}=10")
        print(f"{self.variables[0]}=0        {k_map[0][0]}       {k_map[0][1]}       {k_map[0][2]}       {k_map[0][3]}")
        print(f"{self.variables[0]}=1        {k_map[1][0]}       {k_map[1][1]}       {k_map[1][2]}       {k_map[1][3]}")

    def _print_karnaugh_4(self, k_map):
        print(f"\nКарта Карно для {self.variables[0]}, {self.variables[1]}, {self.variables[2]}, {self.variables[3]}:")
        print(f"        {self.variables[2]}{self.variables[3]}=00  {self.variables[2]}{self.variables[3]}=01  {self.variables[2]}{self.variables[3]}=11  {self.variables[2]}{self.variables[3]}=10")
        print(f"{self.variables[0]}{self.variables[1]}=00    {k_map[0][0]}       {k_map[0][1]}       {k_map[0][2]}       {k_map[0][3]}")
        print(f"{self.variables[0]}{self.variables[1]}=01    {k_map[1][0]}       {k_map[1][1]}       {k_map[1][2]}       {k_map[1][3]}")
        print(f"{self.variables[0]}{self.variables[1]}=11    {k_map[2][0]}       {k_map[2][1]}       {k_map[2][2]}       {k_map[2][3]}")
        print(f"{self.variables[0]}{self.variables[1]}=10    {k_map[3][0]}       {k_map[3][1]}       {k_map[3][2]}       {k_map[3][3]}")

    # ---------- Карты Карно для 5 переменных (таблица 4x8) ----------
    def _build_karnaugh_5(self):
        """Строит карту Карно 4x8 для 5 переменных (ab - строки, cde - столбцы, код Грея)"""
        k_map = [[0,0,0,0,0,0,0,0] for _ in range(4)]
        
        # Порядок столбцов в коде Грея для cde
        col_order = [
            (0,0,0),  # 0: 000
            (0,0,1),  # 1: 001
            (0,1,1),  # 3: 011
            (0,1,0),  # 2: 010
            (1,1,0),  # 6: 110
            (1,1,1),  # 7: 111
            (1,0,1),  # 5: 101
            (1,0,0)   # 4: 100
        ]
        
        # Порядок строк в коде Грея для ab
        row_order = [
            (0,0),  # 0: 00
            (0,1),  # 1: 01
            (1,1),  # 3: 11
            (1,0)   # 2: 10
        ]
        
        for a in self.on_sets:
            a_val = 1 if a[self.variables[0]] else 0
            b_val = 1 if a[self.variables[1]] else 0
            c_val = 1 if a[self.variables[2]] else 0
            d_val = 1 if a[self.variables[3]] else 0
            e_val = 1 if a[self.variables[4]] else 0
            
            # Находим индекс строки
            for row_idx, (ra, rb) in enumerate(row_order):
                if ra == a_val and rb == b_val:
                    row = row_idx
                    break
            
            # Находим индекс столбца
            for col_idx, (rc, rd, re) in enumerate(col_order):
                if rc == c_val and rd == d_val and re == e_val:
                    col = col_idx
                    break
            
            k_map[row][col] = 1
        
        return k_map

    def _print_karnaugh_5(self, k_map):
        """Выводит карту Карно 4x8 для 5 переменных"""
        print(f"\nКарта Карно для {self.variables[0]}, {self.variables[1]}, {self.variables[2]}, {self.variables[3]}, {self.variables[4]}:")
        
        # Заголовки столбцов
        col_headers = ["000", "001", "011", "010", "110", "111", "101", "100"]
        print(f"\nab \\ cde\t", end="")
        for h in col_headers:
            print(f"{h}\t", end="")
        print()
        
        # Строки
        row_headers = ["00", "01", "11", "10"]
        for i, row_header in enumerate(row_headers):
            print(f"{row_header}\t", end="")
            for j in range(8):
                print(f"{k_map[i][j]}\t", end="")
            print()

    # ---------- Поиск прямоугольников для 5 переменных ----------
    def _get_all_rectangles_5(self, k_map):
        """Находит все возможные прямоугольники в карте 4x8"""
        rows, cols = 4, 8
        rectangles = []
        
        # Все возможные размеры прямоугольников (степени двойки)
        row_sizes = [1, 2, 4]
        col_sizes = [1, 2, 4, 8]
        
        for h in row_sizes:
            for w in col_sizes:
                for r0 in range(rows):
                    for c0 in range(cols):
                        cells = []
                        valid = True
                        for dr in range(h):
                            for dc in range(w):
                                r = (r0 + dr) % rows
                                c = (c0 + dc) % cols
                                if k_map[r][c] == 1:
                                    cells.append((r, c))
                                else:
                                    valid = False
                                    break
                            if not valid:
                                break
                        if valid and cells:
                            cells.sort()
                            if cells not in rectangles:
                                rectangles.append(cells)
        return rectangles

    # ---------- Минимальное покрытие для 5 переменных ----------
    def _minimal_cover_exact_5(self, cells, rectangles):
        """Находит минимальное покрытие для 5 переменных"""
        if not cells:
            return []
        
        cell_index = {cell: i for i, cell in enumerate(cells)}
        n = len(cells)
        rect_masks = []
        
        for rect in rectangles:
            mask = 0
            for cell in rect:
                if cell in cell_index:
                    mask |= 1 << cell_index[cell]
            if mask != 0:
                rect_masks.append(mask)
        
        if not rect_masks:
            return []
        
        # Жадный алгоритм
        uncovered = (1 << n) - 1
        cover = []
        
        while uncovered:
            best_mask = 0
            best_idx = -1
            for i, mask in enumerate(rect_masks):
                covered = bin(mask & uncovered).count('1')
                if covered > best_mask:
                    best_mask = covered
                    best_idx = i
            if best_idx == -1:
                break
            cover.append(rectangles[best_idx])
            uncovered &= ~rect_masks[best_idx]
        
        return cover

    # ---------- Преобразование группы в терм для 5 переменных (ДНФ) ----------
    def _group_to_dnf_term_5(self, group):
        """Преобразует группу клеток в терм ДНФ для 5 переменных"""
        if not group:
            return None
        
        # Порядок строк и столбцов
        row_order = [(0,0), (0,1), (1,1), (1,0)]  # ab: 00,01,11,10
        col_order = [
            (0,0,0), (0,0,1), (0,1,1), (0,1,0),
            (1,1,0), (1,1,1), (1,0,1), (1,0,0)
        ]  # cde в коде Грея
        
        rows = set(p[0] for p in group)
        cols = set(p[1] for p in group)
        
        parts = []
        
        # Переменные a, b
        if len(rows) == 1:
            r = next(iter(rows))
            a_val, b_val = row_order[r]
            if a_val == 0 and b_val == 0:
                parts.append(f"¬{self.variables[0]} & ¬{self.variables[1]}")
            elif a_val == 0 and b_val == 1:
                parts.append(f"¬{self.variables[0]} & {self.variables[1]}")
            elif a_val == 1 and b_val == 1:
                parts.append(f"{self.variables[0]} & {self.variables[1]}")
            else:  # (1,0)
                parts.append(f"{self.variables[0]} & ¬{self.variables[1]}")
        elif len(rows) == 2:
            rows_list = sorted(rows)
            if rows_list == [0,1]:
                parts.append(f"¬{self.variables[0]}")
            elif rows_list == [2,3]:
                parts.append(self.variables[0])
            elif rows_list == [0,3]:
                parts.append(f"¬{self.variables[1]}")
            elif rows_list == [1,2]:
                parts.append(self.variables[1])
        
        # Переменные c, d, e
        if len(cols) == 1:
            c = next(iter(cols))
            c_val, d_val, e_val = col_order[c]
            if c_val == 0 and d_val == 0 and e_val == 0:
                parts.append(f"¬{self.variables[2]} & ¬{self.variables[3]} & ¬{self.variables[4]}")
            elif c_val == 0 and d_val == 0 and e_val == 1:
                parts.append(f"¬{self.variables[2]} & ¬{self.variables[3]} & {self.variables[4]}")
            elif c_val == 0 and d_val == 1 and e_val == 1:
                parts.append(f"¬{self.variables[2]} & {self.variables[3]} & {self.variables[4]}")
            elif c_val == 0 and d_val == 1 and e_val == 0:
                parts.append(f"¬{self.variables[2]} & {self.variables[3]} & ¬{self.variables[4]}")
            elif c_val == 1 and d_val == 1 and e_val == 0:
                parts.append(f"{self.variables[2]} & {self.variables[3]} & ¬{self.variables[4]}")
            elif c_val == 1 and d_val == 1 and e_val == 1:
                parts.append(f"{self.variables[2]} & {self.variables[3]} & {self.variables[4]}")
            elif c_val == 1 and d_val == 0 and e_val == 1:
                parts.append(f"{self.variables[2]} & ¬{self.variables[3]} & {self.variables[4]}")
            else:  # (1,0,0)
                parts.append(f"{self.variables[2]} & ¬{self.variables[3]} & ¬{self.variables[4]}")
        elif len(cols) == 2:
            cols_list = sorted(cols)
            # Определяем, какая переменная фиксирована
            # Проверяем c
            c_vals = set(col_order[c][0] for c in cols_list)
            if len(c_vals) == 1:
                if 0 in c_vals:
                    parts.append(f"¬{self.variables[2]}")
                else:
                    parts.append(self.variables[2])
            else:
                # Проверяем d
                d_vals = set(col_order[c][1] for c in cols_list)
                if len(d_vals) == 1:
                    if 0 in d_vals:
                        parts.append(f"¬{self.variables[3]}")
                    else:
                        parts.append(self.variables[3])
                else:
                    # Проверяем e
                    e_vals = set(col_order[c][2] for c in cols_list)
                    if len(e_vals) == 1:
                        if 0 in e_vals:
                            parts.append(f"¬{self.variables[4]}")
                        else:
                            parts.append(self.variables[4])
        elif len(cols) == 4:
            # Все 4 столбца в одной группе по горизонтали
            parts.append("1")
        
        if not parts:
            return "1"
        return " & ".join(parts)

    # ---------- Преобразование группы в дизъюнкт для 5 переменных (КНФ) ----------
    def _group_to_cnf_term_5(self, group):
        """Преобразует группу клеток в дизъюнкт КНФ для 5 переменных"""
        if not group:
            return None
        
        # Порядок строк и столбцов
        row_order = [(0,0), (0,1), (1,1), (1,0)]
        col_order = [
            (0,0,0), (0,0,1), (0,1,1), (0,1,0),
            (1,1,0), (1,1,1), (1,0,1), (1,0,0)
        ]
        
        # Собираем значения для каждой переменной
        values_per_var = [[] for _ in range(5)]
        
        for (row, col) in group:
            a_val, b_val = row_order[row]
            c_val, d_val, e_val = col_order[col]
            values_per_var[0].append(a_val)
            values_per_var[1].append(b_val)
            values_per_var[2].append(c_val)
            values_per_var[3].append(d_val)
            values_per_var[4].append(e_val)
        
        parts = []
        for idx in range(5):
            if len(set(values_per_var[idx])) == 1:
                val = values_per_var[idx][0]
                if val == 0:
                    parts.append(self.variables[idx])
                else:
                    parts.append(f"!{self.variables[idx]}")
        
        if not parts:
            return "0"
        return "(" + "|".join(parts) + ")"

    # ---------- Общие методы для карт Карно (2-4 переменные) ----------
    def _get_all_rectangles(self, k_map):
        rows = len(k_map)
        cols = len(k_map[0])
        rectangles = []
        sizes = []
        for h in [1,2,4,8,16]:
            if h <= rows: sizes.append(h)
        for w in [1,2,4,8,16]:
            if w <= cols: sizes.append(w)
        size_pairs = set()
        for h in sizes:
            for w in sizes:
                if h*w <= rows*cols:
                    size_pairs.add((h,w))
        for h,w in size_pairs:
            for r0 in range(rows):
                for c0 in range(cols):
                    cells = []
                    valid = True
                    for dr in range(h):
                        for dc in range(w):
                            r = (r0 + dr) % rows
                            c = (c0 + dc) % cols
                            if k_map[r][c] == 1:
                                cells.append((r,c))
                            else:
                                valid = False
                                break
                        if not valid: break
                    if valid and cells:
                        cells.sort()
                        if cells not in rectangles:
                            rectangles.append(cells)
        return rectangles

    def _minimal_cover_exact(self, cells, rectangles):
        if not cells:
            return []
        cell_index = {cell: i for i, cell in enumerate(cells)}
        n = len(cells)
        rect_masks = []
        for rect in rectangles:
            mask = 0
            for cell in rect:
                if cell in cell_index:
                    mask |= 1 << cell_index[cell]
            if mask != 0:
                rect_masks.append(mask)
        if not rect_masks:
            return []
        
        if len(rect_masks) > 30:
            uncovered = (1 << n) - 1
            cover = []
            while uncovered:
                best_mask = 0
                best_idx = -1
                for i, mask in enumerate(rect_masks):
                    covered = bin(mask & uncovered).count('1')
                    if covered > best_mask:
                        best_mask = covered
                        best_idx = i
                if best_idx == -1: break
                cover.append(rectangles[best_idx])
                uncovered &= ~rect_masks[best_idx]
            return cover
        
        best = None
        best_size = n+1
        k = len(rect_masks)
        for subset in range(1 << k):
            mask = 0
            count = 0
            for i in range(k):
                if subset & (1 << i):
                    mask |= rect_masks[i]
                    count += 1
            if mask == (1 << n) - 1:
                if best is None or count < best_size:
                    best = subset
                    best_size = count
        if best is not None:
            return [rectangles[i] for i in range(k) if best & (1 << i)]
        return []

    def _group_to_dnf_term(self, group):
        if not group:
            return None
        if self.n == 2:
            rows = set(p[0] for p in group)
            cols = set(p[1] for p in group)
            parts = []
            if len(rows) == 1:
                r = next(iter(rows))
                parts.append(f"¬{self.variables[0]}" if r==0 else self.variables[0])
            if len(cols) == 1:
                c = next(iter(cols))
                parts.append(f"¬{self.variables[1]}" if c==0 else self.variables[1])
            if not parts: return "1"
            return " & ".join(parts)
        elif self.n == 3:
            rows = set(p[0] for p in group)
            cols = set(p[1] for p in group)
            parts = []
            if len(rows) == 1:
                r = next(iter(rows))
                parts.append(f"¬{self.variables[0]}" if r==0 else self.variables[0])
            if len(cols) == 1:
                c = next(iter(cols))
                if c == 0: parts.append(f"¬{self.variables[1]} & ¬{self.variables[2]}")
                elif c == 1: parts.append(f"¬{self.variables[1]} & {self.variables[2]}")
                elif c == 2: parts.append(f"{self.variables[1]} & {self.variables[2]}")
                elif c == 3: parts.append(f"{self.variables[1]} & ¬{self.variables[2]}")
            elif len(cols) == 2:
                if 0 in cols and 1 in cols: parts.append(f"¬{self.variables[1]}")
                elif 2 in cols and 3 in cols: parts.append(self.variables[1])
                elif 0 in cols and 3 in cols: parts.append(f"¬{self.variables[2]}")
                elif 1 in cols and 2 in cols: parts.append(self.variables[2])
            if not parts: return "1"
            return " & ".join(parts)
        elif self.n == 4:
            rows = set(p[0] for p in group)
            cols = set(p[1] for p in group)
            parts = []
            if len(rows) == 1:
                r = next(iter(rows))
                if r == 0: parts.append(f"¬{self.variables[0]} & ¬{self.variables[1]}")
                elif r == 1: parts.append(f"¬{self.variables[0]} & {self.variables[1]}")
                elif r == 2: parts.append(f"{self.variables[0]} & {self.variables[1]}")
                elif r == 3: parts.append(f"{self.variables[0]} & ¬{self.variables[1]}")
            elif len(rows) == 2:
                if 0 in rows and 1 in rows: parts.append(f"¬{self.variables[0]}")
                elif 2 in rows and 3 in rows: parts.append(self.variables[0])
                elif 0 in rows and 3 in rows: parts.append(f"¬{self.variables[1]}")
                elif 1 in rows and 2 in rows: parts.append(self.variables[1])
            if len(cols) == 1:
                c = next(iter(cols))
                if c == 0: parts.append(f"¬{self.variables[2]} & ¬{self.variables[3]}")
                elif c == 1: parts.append(f"¬{self.variables[2]} & {self.variables[3]}")
                elif c == 2: parts.append(f"{self.variables[2]} & {self.variables[3]}")
                elif c == 3: parts.append(f"{self.variables[2]} & ¬{self.variables[3]}")
            elif len(cols) == 2:
                if 0 in cols and 1 in cols: parts.append(f"¬{self.variables[2]}")
                elif 2 in cols and 3 in cols: parts.append(self.variables[2])
                elif 0 in cols and 3 in cols: parts.append(f"¬{self.variables[3]}")
                elif 1 in cols and 2 in cols: parts.append(self.variables[3])
            if not parts: return "1"
            return " & ".join(parts)
        return "1"

    def _group_to_cnf_term(self, group):
        if not group:
            return None
        values_per_var = [[] for _ in range(self.n)]
        for (row, col) in group:
            if self.n == 2:
                vals = [row, col]
            elif self.n == 3:
                b = 1 if col in (2,3) else 0
                c = 1 if col in (1,2) else 0
                vals = [row, b, c]
            elif self.n == 4:
                a = 1 if row in (2,3) else 0
                b = 1 if row in (1,2) else 0
                c = 1 if col in (2,3) else 0
                d = 1 if col in (1,2) else 0
                vals = [a, b, c, d]
            else:
                return None
            for idx, v in enumerate(vals):
                values_per_var[idx].append(v)
        parts = []
        for idx in range(self.n):
            if len(set(values_per_var[idx])) == 1:
                val = values_per_var[idx][0]
                if val == 0:
                    parts.append(self.variables[idx])
                else:
                    parts.append(f"!{self.variables[idx]}")
        if not parts:
            return "0"
        return "(" + "|".join(parts) + ")"

    def _group_description(self, group):
        l = len(group)
        if l == 1: return "одиночная клетка"
        if l == 2: return "пара клеток"
        if l == 4: return "прямоугольник 2x2"
        if l == 8: return "прямоугольник 2x4"
        if l == 16: return "прямоугольник 4x4"
        return f"группа из {l} клеток"
