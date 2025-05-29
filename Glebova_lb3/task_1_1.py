DEBUG = True

def min_edit_cost(replace_cost, insert_cost, delete_cost, s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + delete_cost
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + insert_cost

    if DEBUG:
        print("\nНачальная матрица:")
        for row in dp:
            print(row)
        print("\nПроцесс заполнения:")

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
                if DEBUG:
                    print(f"Совпадение: s1[{i-1}]='{s1[i-1]}' == s2[{j-1}]='{s2[j-1]}'")
            else:
                replace = dp[i-1][j-1] + replace_cost
                insert = dp[i][j-1] + insert_cost
                delete = dp[i-1][j] + delete_cost
                dp[i][j] = min(replace, insert, delete)
                if DEBUG:
                    print(f"Несовпадение: s1[{i-1}]='{s1[i-1]}', s2[{j-1}]='{s2[j-1]}'")
                    print(f"  Варианты: replace={replace}, insert={insert}, delete={delete}")
        
        if DEBUG:
            print(f"После строки {i}:")
            for row in dp:
                print(row)
            print()

    if DEBUG:
        print("Итоговая матрица:")
        for row in dp:
            print(row)
        print(f"\nМинимальная стоимость: {dp[m][n]}")

    return dp[m][n]

replace_cost, insert_cost, delete_cost = map(int, input().split())
s1 = input()
s2 = input()
print(min_edit_cost(replace_cost, insert_cost, delete_cost, s1, s2))