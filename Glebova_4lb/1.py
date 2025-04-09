DEBUG = True


def compute_lps_array(pattern):
    lps = [0] * len(pattern)
    length = 0
    for i in range(1, len(pattern)):
        if DEBUG:
            print(f"\nШаг {i}:")
            print(f"  Сравниваем pattern[{i}]='{pattern[i]}' и pattern[{length}]='{pattern[length]}'")
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            if DEBUG:
                print(f"  Совпадение! Увеличиваем length до {length}")
                print(f"  lps[{i}] = {length}")
        else:
            if length != 0:
                if DEBUG:
                    print(f"  Несовпадение! length={length} != 0, берем lps[{length-1}]={lps[length-1]}")
                length = lps[length - 1]
                if DEBUG:
                    print(f"  Новый length = {length}")
            else:
                lps[i] = 0
                if DEBUG:
                    print(f"  Несовпадение! length=0, lps[{i}] = 0")
    if DEBUG:
        print("\nИтоговый массив lps:", lps)
    return lps


def kmp_search(pattern, text):
    if DEBUG:
        print("\n=== Начало поиска KMP ===")
        print(f"Шаблон: '{pattern}'")
        print(f"Текст:  '{text}'")

    lps = compute_lps_array(pattern)
    i = 0
    j = 0
    pattern_len = len(pattern)
    text_len = len(text)
    occurrences = []

    while i < text_len:
        if DEBUG:
            print(f"\nШаг i={i}, j={j}:")
            print(f"  Сравниваем pattern[{j}]='{pattern[j]}' и text[{i}]='{text[i]}'")
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if DEBUG:
                print(f"  Совпадение! Увеличиваем i до {i}, j до {j}")
            if j == pattern_len:
                occurrences.append(i - j)
                if DEBUG:
                    print(f"  Полное совпадение! Найдено вхождение на позиции {i - j}")
                j = lps[j - 1]
                if DEBUG:
                    print(f"  Сдвигаем j на lps[{j}]={lps[j]}")
        else:
            if j != 0:
                if DEBUG:
                    print(f"  Несовпадение! j={j} != 0, берем lps[{j-1}]={lps[j-1]}")
                j = lps[j - 1]
            else:
                if DEBUG:
                    print(f"  Несовпадение! j=0, увеличиваем i до {i + 1}")
                i += 1
    if DEBUG:
        print("\n=== Поиск завершен ===")
        print("Найденные вхождения:", occurrences)
    return occurrences


P = input()
T = input()

result = kmp_search(P, T)

if result:
    print(','.join(map(str, result)))
else:
    print(-1)
