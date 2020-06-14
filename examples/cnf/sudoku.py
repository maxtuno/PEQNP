import numpy as np
import peqnp.cnf as cnf


def expandLine(line):
    return line[0] + line[5:9].join([line[1:5] * (base - 1)] * base) + line[9:13]


def show(board):
    import string
    line0 = expandLine('╔═══╤═══╦═══╗')
    line1 = expandLine('║ . │ . ║ . ║')
    line2 = expandLine('╟───┼───╫───╢')
    line3 = expandLine('╠═══╪═══╬═══╣')
    line4 = expandLine('╚═══╧═══╩═══╝')

    symbol = ' ' + string.printable.replace(' ', '').replace('0', '')
    nums = [[''] + [symbol[n] for n in row] for row in board]
    print(line0)
    for r in range(1, side + 1):
        print("".join(n + s for n, s in zip(nums[r - 1], line1.split('.'))))
        print([line2, line3, line4][(r % side == 0) + (r % base == 0)])


def generate(base):
    # pattern for a baseline valid solution
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample

    def shuffle(s):
        return sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = (squares * 3) // 4
    for p in map(int, sample(range(squares), empties)):
        board[p // side][p % side] = 0

    show(board)
    return board


base = 4
side = base * base

puzzle = np.asarray(generate(base))

cnf.begin(side.bit_length(), key='sudoku')

board = np.asarray(cnf.matrix(dimensions=(side, side)))
cnf.apply_single(board.flatten(), lambda x: 1 <= x <= side)

for i in range(side):
    for j in range(side):
        if puzzle[i][j]:
            assert board[i][j] == puzzle[i][j]

for c, r in zip(board, board.T):
    cnf.all_different(c)
    cnf.all_different(r)

for i in range(base):
    for j in range(base):
        cnf.all_different(board[i * base:(i + 1) * base, j * base:(j + 1) * base].flatten())

cnf.end({'x_{}'.format(i): b  for i, b in enumerate(board.flatten())})

if cnf.satisfy(solver='java -jar -Xmx4g blue.jar'):
    show(np.vectorize(int)(board))
