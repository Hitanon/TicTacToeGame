import random


def generate_winning_boards():
    positions = []
    # Rows
    positions += [[i + j for j in range(3)] for i in range(0, 9, 3)]
    # Columns
    positions += [[i + j for i in range(0, 9, 3)] for j in range(3)]
    # Diagonals
    positions += [[0, 4, 8], [2, 4, 6]]

    winning_boards = []
    for pos in positions:
        board = [" " for i in range(9)]
        for i in pos:
            board[i] = "X"
        winning_boards.append(board)

    return winning_boards


def generate_draw_boards(num_states=1):
    draw_boards = []
    for i in range(num_states):
        state = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
        random.shuffle(state)
        draw_boards.append(state)
    return draw_boards


def generate_not_draw_boards(num_states=1):
    not_draw_boards = generate_draw_boards(num_states)
    for board in not_draw_boards:
        positions = set(random.sample(range(9), k=random.randint(1, 8)))
        for pos in positions:
            board[pos] = " "
    return not_draw_boards
