from copy import deepcopy, copy

DEBUG = True


class IntermediateSolution:
    def __init__(self, n):
        self.square = 0
        self.squares_matrix = [[0]*n for _ in range(n)]
        self.squares = []

    def get_child(self, n, square):
        new_matrix = deepcopy(self.squares_matrix)
        for x in range(square[0], square[0] + square[2]):
            for y in range(square[1], square[1] + square[2]):
                new_matrix[y][x] = 1
        new_squares = copy(self.squares)
        new_squares.append(square)
        new_square = self.square + square[2]**2
        child = IntermediateSolution(n)
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


def get_start_info(n):
    if n % 2 == 0:
        return 4, n // 2, n // 2

    for d in range(3, int(n**0.5) + 1, 2):
        if n % d == 0:
            d_max = n // d
            top_side = d_max*(d // 2 + 1)
            low_side = n - top_side
            solution_len = 2*top_side // low_side + 2 + (top_side % low_side != 0)*(2*low_side // (top_side - low_side))
            return solution_len, top_side, low_side

    top_side = n // 2 + 1
    low_side = n - top_side
    if n < 13:
        return 6, top_side, low_side
    return 11, top_side, low_side


def check_square(matrix, square):
    for x in range(square[0], square[0] + square[2]):
        if matrix[square[1]][x] == 1:
            if DEBUG:
                print(f"Квадрат ({square[0] + 1}, {square[1] + 1}, {square[2]}) не может быть размещен: пересечение с уже занятой клеткой.")
            return False
    if DEBUG:
        print(f"Квадрат ({square[0] + 1}, {square[1] + 1}, {square[2]}) может быть размещен.")
    return True


def get_children(n, start, solution):
    stack = []
    for y in range(start, n):
        for x in range(start, n):
            for max_side in range(n - max(x, y), 0, -1):
                if check_square(solution.squares_matrix, (x, y, max_side)):
                    for side in range(1, max_side + 1):
                        stack.append(solution.get_child(n, (x, y, side)))
                    if DEBUG:
                        print(f"Найдены дочерние элементы для позиции ({x + 1}, {y + 1}) с максимальной стороной {max_side}.")
                    return stack
    if DEBUG:
        print("Дочерние элементы не найдены.")
    return stack


def get_solution(n):
    mx, big, small = get_start_info(n)
    start_solution = IntermediateSolution(n)
    start_solution = start_solution.get_child(n, (0, 0, big))
    start_solution = start_solution.get_child(n, (0, big, small))
    start_solution = start_solution.get_child(n, (big, 0, small))

    if DEBUG:
        print(f"Начальное решение с квадратами: {[(sq[0] + 1, sq[1] + 1, sq[2]) for sq in start_solution.squares]}")
        print("Начальное состояние матрицы:")
        for row in start_solution.squares_matrix:
            print(" ".join(map(str, row)))
        print("----------------------------------------")

    limit_stack = [start_solution]
    while True:
        stack = limit_stack
        limit_stack = []
        while stack:
            solution = stack.pop()
            if solution.square == n**2:
                if DEBUG:
                    print("Найдено решение, покрывающее всю столешницу.")
                print(len(solution.squares))
                for x in solution.squares:
                    print(x[0] + 1, x[1] + 1, x[2])
                return
            if len(solution.squares) == mx:
                if DEBUG:
                    print(f"Достигнут предел количества квадратов: {mx}. Решение добавлено в стек для дальнейшего анализа.")
                limit_stack.append(solution)
                continue
            children = get_children(n, small, solution)
            if DEBUG:
                print(f"Добавлено {len(children)} дочерних элементов в стек.")
            stack.extend(children)
        if DEBUG:
            print(f"Увеличиваем предел количества квадратов с {mx} до {mx + 1}.")
        mx += 1


get_solution(int(input()))