DEBUG = True

def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = i
        if DEBUG:
            print(f"Инициализация dp[{i}][0] = {i} (удаление первых {i} символов из '{s[:i]}')")
    
    for j in range(1, n + 1):
        dp[0][j] = j
        if DEBUG:
            print(f"Инициализация dp[0][{j}] = {j} (вставка первых {j} символов '{t[:j]}')")

    if DEBUG:
        print("\nНачальная матрица:")
        print("    " + "   ".join(f"'{c}'" if j > 0 else "ε" for j, c in enumerate(" " + t)))
        for i in range(m + 1):
            row_char = f"'{s[i-1]}'" if i > 0 else "ε"
            print(f"{row_char} " + " ".join(f"{dp[i][j]:3}" for j in range(n + 1)))

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
                if DEBUG:
                    print(f"\nСимволы совпадают: s[{i-1}]='{s[i-1]}' == t[{j-1}]='{t[j-1]}'")
                    print(f"Берем значение из dp[{i-1}][{j-1}] = {dp[i-1][j-1]}")
            else:
                delete = dp[i-1][j] + 1
                insert = dp[i][j-1] + 1
                replace = dp[i-1][j-1] + 1
                dp[i][j] = min(delete, insert, replace)
                if DEBUG:
                    print(f"\nОбрабатываем s[{i-1}]='{s[i-1]}' и t[{j-1}]='{t[j-1]}'")
                    print(f"Варианты: удаление={delete}, вставка={insert}, замена={replace}")
                    print(f"Выбрано минимальное: {dp[i][j]}")

        if DEBUG:
            print(f"\nПосле обработки строки s[{i}]='{s[i-1]}':")
            print("    " + "   ".join(f"'{c}'" if j > 0 else "ε" for j, c in enumerate(" " + t)))
            for k in range(m + 1):
                row_char = f"'{s[k-1]}'" if k > 0 else "ε"
                print(f"{row_char} " + " ".join(f"{dp[k][l]:3}" for l in range(n + 1)))

    if DEBUG:
        print("\nИтоговая матрица расстояний:")
        print("    " + "   ".join(f"'{c}'" if j > 0 else "ε" for j, c in enumerate(" " + t)))
        for i in range(m + 1):
            row_char = f"'{s[i-1]}'" if i > 0 else "ε"
            print(f"{row_char} " + " ".join(f"{dp[i][j]:3}" for j in range(n + 1)))
        print(f"\nМинимальное расстояние Левенштейна: {dp[m][n]}")

    return dp[m][n]

s = input()
t = input()
print(levenshtein_distance(s, t))