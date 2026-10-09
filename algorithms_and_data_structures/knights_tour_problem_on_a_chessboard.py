#2.6 Задача обхода конём шахматной доски

#
#Рекурсивный поиск с возвратом (backtracking) и эвристикой Варнсдорфа для нахождения тура коня на шахматной доске.
#

KNIGHT_MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)]
#Список всех возможных ходов коня, каждая пара это изменение координат клетки (dx, dy)

def knights_tour(n, start=(0, 0), warnsdorff=False):
    # n - Размер стороны доски. Например, для доски 8x8 n = 8
    # start - начальная позиция коня на доске (x, y)
    #warnsdorff - использовать ли эвристику Варнсдорфа (True/False)

    board = [[-1] * n for _ in range(n)]
    #генератор доски n x n, где -1 означает, что клетка не посещена



    def free(x, y):
        return 0 <= x < n and 0 <= y < n and board[x][y] == -1
    #Проверка, свободна ли клетка (x, y) для хода коня


    def degree(x, y):                             # число свободных ходов из клетки
        return sum(free(x + dx, y + dy) for dx, dy in KNIGHT_MOVES)
    #проверка количества возможных ходов коня из клетки (x, y)


    def solve(x, y, step):                        
        if step == n * n:                         # все клетки пройдены
            return True
        cand = [(x + dx, y + dy) for dx, dy in KNIGHT_MOVES if free(x + dx, y + dy)] #поиск всех возможных ходов коня из клетки (x, y)
        if warnsdorff:                            
            cand.sort(key=lambda p: degree(*p))     # сортировка по количеству возможных ходов из каждой клетки (эвристика Варнсдорфа)
        for nx, ny in cand:
            board[nx][ny] = step                  # пробный ход
            if solve(nx, ny, step + 1):
                return True                       # если найден путь, возвращаем True
            board[nx][ny] = -1                    # если путь не найден, откатываемся (backtrack)
        return False
    #постройка маршрута обхода коня с помощью рекурсии и возврата (backtracking)


    board[start[0]][start[1]] = 0       #начальная клетка коня помечается как посещённая (0)
    return board if solve(start[0], start[1], 1) else None  #если найден путь, возвращаем доску с маршрутом, иначе None


def check_tour(board):

    #Проверка корректности тура коня на шахматной доске. Проверяет, что все клетки посещены и что каждый ход коня допустим.
    
    n = len(board)
    pos = {board[x][y]: (x, y) for x in range(n) for y in range(n)}
    if sorted(pos) != list(range(n * n)):
        return False            #Проверка, что все клетки посещены 
    for k in range(n * n - 1):
        dx = abs(pos[k][0] - pos[k + 1][0])
        dy = abs(pos[k][1] - pos[k + 1][1])
        if (dx, dy) not in ((1, 2), (2, 1)):
            return False
    return True             #Проверка, что каждый ход коня допустим


def knight_summary(n, warnsdorff):
    try:
        board = knights_tour(n, (0, 0), warnsdorff)
    except RecursionError:
        return "Ошибка: превышена максимальная глубина рекурсии"
    return "тур не найден" if board is None else \
        "тур найден, проверка: " + str(check_tour(board))




#
#Итеративный поиск с возвратом (backtracking) и эвристикой Варнсдорфа для нахождения тура коня на шахматной доске.
#




def knights_tour_iterative(n, start=(0, 0), warnsdorff=False):
    # Создаём доску
    if n <= 0:
        return None

    sx, sy = start
    if not (0 <= sx < n and 0 <= sy < n):
        return None

    board = [[-1] * n for _ in range(n)]

    def free(x, y):
        return (
            0 <= x < n
            and 0 <= y < n
            and board[x][y] == -1
        )

    def degree(x, y):
        return sum(
            free(x + dx, y + dy)
            for dx, dy in KNIGHT_MOVES
        )

    def candidates(x, y):
        # Получаем возможные следующие ходы
        cand = [
            (x + dx, y + dy)
            for dx, dy in KNIGHT_MOVES
            if free(x + dx, y + dy)
        ]

        # Эвристика Варнсдорфа
        if warnsdorff:
            cand.sort(key=lambda p: degree(*p))

        return cand

    # Начальная клетка
    board[sx][sy] = 0

    # Каждый элемент стека:
    # [x, y, список возможных ходов, индекс следующего кандидата]
    stack = [
        [sx, sy, candidates(sx, sy), 0]
    ]

    # Итеративный поиск с возвратом
    while stack:

        # Все клетки посещены
        if len(stack) == n * n:
            return board

        x, y, cand, index = stack[-1]

        # Все варианты из текущей клетки проверены
        if index >= len(cand):
            stack.pop()

            # Отменяем ход, если вернулись к предыдущей клетке
            if stack:
                board[x][y] = -1

            continue

        # Берём следующего кандидата
        nx, ny = cand[index]

        # Запоминаем, какой вариант будем проверять дальше
        stack[-1][3] += 1

        if free(nx, ny):
            # Делаем ход
            board[nx][ny] = len(stack)

            # Сохраняем новое состояние поиска
            stack.append([
                nx,
                ny,
                candidates(nx, ny),
                0
            ])

    # Все варианты исчерпаны
    return None


def check_tour_iterative(board):
    # Независимая проверка найденного тура
    n = len(board)

    pos = {
        board[x][y]: (x, y)
        for x in range(n)
        for y in range(n)
    }

    if sorted(pos) != list(range(n * n)):
        return False

    for k in range(n * n - 1):
        dx = abs(pos[k][0] - pos[k + 1][0])
        dy = abs(pos[k][1] - pos[k + 1][1])

        if (dx, dy) not in ((1, 2), (2, 1)):
            return False

    return True

def knight_summary_iterative(n, warnsdorff):
    board = knights_tour_iterative(
        n,
        start=(0, 0),
        warnsdorff=warnsdorff
    )

    if board is None:
        return "тур не найден"

    return "тур найден, проверка: " + str(check_tour_iterative(board))

parametr_a=98
parametr_b=True

print(f"Рекурсивный поиск: {knight_summary(10, parametr_b)}")

print(f"Рекурсивный поиск: {knight_summary(parametr_a, parametr_b)}")

print(f"Итеративный поиск: {knight_summary_iterative(parametr_a, parametr_b)}")