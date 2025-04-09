DEBUG = True


def compute_lps_array(pattern):
    lps = [0] * len(pattern)
    length = 0
    for i in range(1, len(pattern)):
        if DEBUG:
            print(f"\nВычисление lps: Шаг {i}")
            print(f"Сравниваем pattern[{i}]='{pattern[i]}' с pattern[{length}]='{pattern[length]}'")
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            if DEBUG:
                print(f"Совпадение! Устанавливаем lps[{i}] = {length}")
        else:
            if length != 0:
                if DEBUG:
                    print(f"Несовпадение! length={length}, берем lps[{length-1}]={lps[length-1]}")
                length = lps[length - 1]
            else:
                lps[i] = 0
                if DEBUG:
                    print("Несовпадение! length=0, устанавливаем lps[{i}] = 0")
    if DEBUG:
        print("\nИтоговый массив lps:", lps)
    return lps


def kmp_search(pattern, text):
    if DEBUG:
        print("\n=== Начало поиска KMP ===")
        print(f"Ищем '{pattern}' в '{text}'")
        print(f"Длина pattern: {len(pattern)}, длина text: {len(text)}")
    
    lps = compute_lps_array(pattern)
    i = 0
    j = 0
    pattern_len = len(pattern)
    text_len = len(text)

    while i < text_len:
        if DEBUG:
            print(f"\nТекущая позиция: i={i}, j={j}")
            print(f"Сравниваем text[{i}]='{text[i]}' с pattern[{j}]='{pattern[j]}'")
        
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if DEBUG:
                print(f"Совпадение! Переходим к i={i}, j={j}")
            
            if j == pattern_len:
                pos = i - j
                if DEBUG:
                    print(f"\n!!! Найдено полное совпадение на позиции {pos} !!!")
                return pos
        else:
            if j != 0:
                if DEBUG:
                    print(f"Несовпадение! j={j}, используем lps[{j-1}]={lps[j-1]}")
                j = lps[j - 1]
            else:
                if DEBUG:
                    print(f"Несовпадение! j=0, увеличиваем i с {i} до {i+1}")
                i += 1

    if DEBUG:
        print("\nПоиск завершен. Совпадений не найдено.")
    return -1


A = input()
B = input()

if DEBUG:
    print("\n=== Проверка циклического сдвига ===")
    print(f"A: '{A}' (длина {len(A)})")
    print(f"B: '{B}' (длина {len(B)})")

if len(A) == len(B):
    if DEBUG:
        print("\nДлины совпадают, выполняем поиск B в A+A")
        print(f"A+A: '{A*2}'")
    result = kmp_search(B, A*2)
    if DEBUG:
        print("\nРезультат поиска:", result)
    print(result)
else:
    if DEBUG:
        print("\nДлины не совпадают, циклический сдвиг невозможен")
    print(-1)