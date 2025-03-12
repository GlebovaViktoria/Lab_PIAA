from copy import deepcopy, copy

DEBUG = True


class IntermediateSolution:
    def __init__(self, n, m):
        self.square = 0
        self.squares_matrix = [[0]*m for _ in range(n)]
        self.squares = []

    def get_child(self, n, m, square):
        new_matrix = deepcopy(self.squares_matrix)
        for x in range(square[0], square[0] + square[2]):
            for y in range(square[1], square[1] + square[2]):
                new_matrix[y][x] = 1
        new_squares = copy(self.squares)
        new_squares.append(square)
        new_square = self.square + square[2]**2
        child = IntermediateSolution(n, m)
        child.square = new_square
        child.squares_matrix = new_matrix
        child.squares = new_squares

        if DEBUG:
            print(f"Создан новый дочерний элемент с квадратом: ({square[0] + 1}, {square[1] + 1}, {square[2]})")
            print("Текущее состояние матрицы:")
            for row in child.squares_matrix:
                print(" ".join(map(str, row)))
            print(f"Текущая площадь: {child.square}")
            print(f"Текущие квадраты: {[(sq[0] + 1, sq[1] + 1, sq[2]) for sq in child.squares]}")
            print("----------------------------------------")

        return child


def check_square(matrix, square):
    for y in range(square[1], square[1] + square[2]):
        for x in range(square[0], square[0] + square[2]):
            if matrix[y][x] == 1:
                if DEBUG:
                    print(f"Квадрат ({square[0] + 1}, {square[1] + 1}, {square[2]}) не может быть размещен: пересечение с уже занятой клеткой.")
                return False
    if DEBUG:
        print(f"Квадрат ({square[0] + 1}, {square[1] + 1}, {square[2]}) может быть размещен.")
    return True


def get_children(n, m, solution):
    stack = []
    for y in range(n):
        for x in range(m):
            for max_side in range(min(m - x, n - y), 0, -1):
                if max_side >= min(m, n):
                    continue
                if check_square(solution.squares_matrix, (x, y, max_side)):
                    for side in range(1, max_side + 1):
                        stack.append(solution.get_child(n, m, (x, y, side)))
                    if DEBUG:
                        print(f"Найдены дочерние элементы для позиции ({x + 1}, {y + 1}) с максимальной стороной {max_side}.")
                    return stack
    if DEBUG:
        print("Дочерние элементы не найдены.")
    return stack


def get_solution(n, m):
    start_solution = IntermediateSolution(n, m)

    if DEBUG:
        print("Начальное состояние матрицы:")
        for row in start_solution.squares_matrix:
            print(" ".join(map(str, row)))
        print("----------------------------------------")

    mx = 2
    limit_stack = [start_solution]
    mn = None
    mn_k = 0
    while True:
        stack = limit_stack
        limit_stack = []
        while stack:
            solution = stack.pop()
            if solution.square == n*m:
                if DEBUG:
                    print("Найдено решение, покрывающее всю столешницу.")
                print(len(solution.squares))
                for x in solution.squares:
                    print(x[0] + 1, x[1] + 1, x[2])
                mn = len(solution.squares)
                mn_k += 1
            if mn is not None and len(solution.squares) == mn:
                if DEBUG:
                    print(f"Пропуск решения с количеством квадратов {mn}, так как уже найдено минимальное решение.")
                continue
            if len(solution.squares) == mx:
                if DEBUG:
                    print(f"Достигнут предел количества квадратов: {mx}. Решение добавлено в стек для дальнейшего анализа.")
                limit_stack.append(solution)
                continue
            children = get_children(n, m, solution)
            if DEBUG:
                print(f"Добавлено {len(children)} дочерних элементов в стек.")
            stack.extend(children)
        if mn is not None:
            if DEBUG:
                print(f"Общее количество решений с минимальным количеством квадратов: {mn_k}")
            return
        if DEBUG:
            print(f"Увеличиваем предел количества квадратов с {mx} до {mx + 1}.")
        mx += 1


n, m = map(int, input().split())
get_solution(n, m)