DEBUG = True

def min_edit_operations(replace_cost, insert_cost, delete_cost, s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + delete_cost
        if DEBUG:
            print(f"Инициализация dp[{i}][0] = {dp[i][0]} (удаление {s1[i-1]})")
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + insert_cost
        if DEBUG:
            print(f"Инициализация dp[0][{j}] = {dp[0][j]} (вставка {s2[j-1]})")

    if DEBUG:
        print("\nНачальная матрица:")
        for row in dp:
            print(' '.join(f"{x:3}" for x in row))

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
                if DEBUG:
                    print(f"Совпадение: s1[{i-1}]='{s1[i-1]}' == s2[{j-1}]='{s2[j-1]}', берем dp[{i-1}][{j-1}]={dp[i-1][j-1]}")
            else:
                replace = dp[i-1][j-1] + replace_cost
                insert = dp[i][j-1] + insert_cost
                delete = dp[i-1][j] + delete_cost
                dp[i][j] = min(replace, insert, delete)
                if DEBUG:
                    print(f"Обработка s1[{i-1}]='{s1[i-1]}', s2[{j-1}]='{s2[j-1]}'")
                    print(f"  replace: {replace}, insert: {insert}, delete: {delete}")
                    print(f"  Выбрано: {dp[i][j]}")

    if DEBUG:
        print("\nЗаполненная матрица:")
        for row in dp:
            print(' '.join(f"{x:3}" for x in row))

    operations = []
    i, j = m, n
    while i > 0 or j > 0:
        if DEBUG:
            print(f"\nТекущая позиция: i={i}, j={j}")
        if i > 0 and j > 0 and s1[i-1] == s2[j-1]:
            operations.append('M')
            if DEBUG:
                print(f"Совпадение: s1[{i-1}]='{s1[i-1]}' == s2[{j-1}]='{s2[j-1]}', операция M")
            i -= 1
            j -= 1
        else:
            if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + replace_cost:
                operations.append('R')
                if DEBUG:
                    print(f"Замена: s1[{i-1}]='{s1[i-1]}' → s2[{j-1}]='{s2[j-1]}', операция R")
                i -= 1
                j -= 1
            elif j > 0 and dp[i][j] == dp[i][j-1] + insert_cost:
                operations.append('I')
                if DEBUG:
                    print(f"Вставка: s2[{j-1}]='{s2[j-1]}', операция I")
                j -= 1
            elif i > 0 and dp[i][j] == dp[i-1][j] + delete_cost:
                operations.append('D')
                if DEBUG:
                    print(f"Удаление: s1[{i-1}]='{s1[i-1]}', операция D")
                i -= 1

    operations.reverse()
    if DEBUG:
        print("\nФинальная последовательность операций:", ''.join(operations))
    return ''.join(operations)

replace_cost, insert_cost, delete_cost = map(int, input().split())
s1 = input()
s2 = input()
operations = min_edit_operations(replace_cost, insert_cost, delete_cost, s1, s2)
print(operations)
print(s1)
print(s2)