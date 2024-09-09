# Импорт необходимых библиотек
#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

# Определяем игроков: человек (-1) и компьютер (+1)
HUMAN = -1
COMP = +1
# Инициализация пустого игрового поля (3x3)
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(state):
    """
    Оценивает текущее состояние доски.
    Если выиграл компьютер, возвращает +1, если выиграл человек — -1, в случае ничьей — 0.
    Это используется для Minimax для определения, кто выиграл в конкретном состоянии.
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    Проверяет, выиграл ли игрок (человек или компьютер).
    Победное состояние — это три одинаковых символа в строке, столбце или диагонали.
    Возвращает True, если игрок выиграл, иначе False.
    """
    # Все возможные выигрышные комбинации: три строки, три столбца, две диагонали
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    Проверяет, закончилась ли игра (выиграл ли человек или компьютер).
    Возвращает True, если кто-то выиграл, иначе False.
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Возвращает список пустых клеток на доске.
    Это клетки, в которых можно сделать ход.
    """
    cells = []
    # Перебираем каждую клетку доски
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    Проверяет, является ли ход (x, y) допустимым, то есть пуста ли эта клетка.
    Возвращает True, если ход допустим.
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Выполняет ход игрока на доске, если ход допустим.
    Возвращает True, если ход был выполнен успешно.
    """
    if valid_move(x, y):
        board[x][y] = player # Устанавливаем символ игрока в клетку (x, y)
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    Алгоритм Minimax для выбора наилучшего хода.
    Ищет максимальный (или минимальный) результат, учитывая ходы обоих игроков.
    """
    # Определяем начальные лучшие значения для каждого игрока
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    # Если игра закончена или достигнута максимальная глубина (все клетки заполнены)
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    # Перебираем все пустые клетки и проверяем все возможные ходы
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        # Выбираем лучший ход в зависимости от игрока
        if player == COMP:
            if score[2] > best[2]:
                best = score  # максимальное значение
        else:
            if score[2] < best[2]:
                best = score  # минимальное значение

    # Возвращаем наилучший ход
    return best


def clean():
    """
    Очищает консоль. Использует системные команды в зависимости от операционной системы.
    """
    os_name = platform.system().lower() # Определяем операционную систему
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Выводит текущее состояние доски в консоль.
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'
    print('\n' + str_line)
    for row in state:  # Проходим по каждой строке доски
        for cell in row:  # Проходим по каждой клетке строки
            symbol = chars[cell]  # Определяем символ для отображения
            print(f'| {symbol} |', end='')  # Выводим клетку
        print('\n' + str_line)  # После строки выводим разделитель


def ai_turn(c_choice, h_choice):
    """
    Ход компьютера. Выбирает случайный ход, если доска пуста,
    иначе использует Minimax для поиска оптимального хода.
    """
    depth = len(empty_cells(board)) # Оставшиеся пустые клетки
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice) # Отображаем доску

    if depth == 9: # Если это первый ход
        x = choice([0, 1, 2]) # Случайный выбор координат
        y = choice([0, 1, 2])
    else: # В противном случае используем алгоритм Minimax для поиска лучшего хода
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice):
    """
    Ход человека. Ввод координат с проверкой на правильность.
    """
    depth = len(empty_cells(board)) # Оставшиеся пустые клетки
    if depth == 0 or game_over(board):
        return

    move = -1
    # Карта номеров клавиш и соответствующих координат на доске
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9: # Пока ход не будет допустимым (1-9)
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN) # Выполняем ход

            if not can_move: # Если ход недопустим (клетка занята)
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt): # Обрабатываем прерывания
            print('Bye')
            exit()
        except (KeyError, ValueError): # Обрабатываем неправильный ввод
            print('Bad choice')


def main():
    """
    Основная функция, запускающая игру.
    """
    clean()
    h_choice = ''  # Выбор символа игрока (X или O)
    c_choice = ''  # Выбор символа компьютера
    first = ''  # Определяет, кто ходит первым

    # Цикл для получения правильного выбора символа (X или O)
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Цикл для выбора, кто ходит первым (человек или компьютер)
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Основной игровой цикл, продолжается, пока есть свободные клетки и никто не выиграл
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # После окончания игры проверяем результат и выводим сообщение
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()


if __name__ == '__main__':
    main()
