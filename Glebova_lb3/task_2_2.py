DEBUG = True

def extended_levenshtein(s, t, del_cost=1, ins_cost=1, repl_cost=1, trans_repl_cost=1):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + del_cost
        if DEBUG:
            print(f"Инициализация dp[{i}][0] = {dp[i][0]} (удаление первых {i} символов из '{s[:i]}')")
    
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + ins_cost
        if DEBUG:
            print(f"Инициализация dp[0][{j}] = {dp[0][j]} (вставка первых {j} символов '{t[:j]}')")

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
                delete = dp[i-1][j] + del_cost
                insert = dp[i][j-1] + ins_cost
                replace = dp[i-1][j-1] + repl_cost
                dp[i][j] = min(delete, insert, replace)
                if DEBUG:
                    print(f"\nОбрабатываем s[{i-1}]='{s[i-1]}' и t[{j-1}]='{t[j-1]}'")
                    print(f"Варианты: удаление={delete}, вставка={insert}, замена={replace}")
                    print(f"Выбрано минимальное: {dp[i][j]}")

            if i > 1 and j > 1:
                if s[i-2] == t[j-1] and s[i-1] == t[j-2]:
                    trans_cost = dp[i-2][j-2] + trans_repl_cost
                    dp[i][j] = min(dp[i][j], trans_cost)
                    if DEBUG:
                        print(f"Транспозиция: s[{i-2}{i-1}]='{s[i-2]}{s[i-1]}' ↔ t[{j-2}{j-1}]='{t[j-2]}{t[j-1]}'")
                        print(f"Стоимость транспозиции: {trans_cost}")
                elif s[i-2] != t[j-1] or s[i-1] != t[j-2]:
                    trans_cost = dp[i-2][j-2] + trans_repl_cost + repl_cost
                    dp[i][j] = min(dp[i][j], trans_cost)
                    if DEBUG:
                        print(f"Транспозиция с заменой: s[{i-2}{i-1}]='{s[i-2]}{s[i-1]}' ↔ t[{j-2}{j-1}]='{t[j-2]}{t[j-1]}'")
                        print(f"Стоимость транспозиции с заменой: {trans_cost}")

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
        print(f"\nМинимальное расстояние: {dp[m][n]}")

    return dp[m][n]

s = input()
t = input()
del_cost = 1
ins_cost = 1
repl_cost = 1
trans_repl_cost = 1
print(extended_levenshtein(s, t, del_cost, ins_cost, repl_cost, trans_repl_cost))