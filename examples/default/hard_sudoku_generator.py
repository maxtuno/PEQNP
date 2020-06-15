"""
///////////////////////////////////////////////////////////////////////////////
//        Copyright (c) 2012-2020 Oscar Riveros. all rights reserved.        //
//                        oscar.riveros@peqnp.science                        //
//                                                                           //
//   without any restriction, Oscar Riveros reserved rights, patents and     //
//  commercialization of this knowledge or derived directly from this work.  //
///////////////////////////////////////////////////////////////////////////////

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import peqnp as pn


def expand_line(line):
    return line[0] + line[5:9].join([line[1:5] * (base - 1)] * base) + line[9:13]


def show(br):
    import string
    line0 = expand_line('╔═══╤═══╦═══╗')
    line1 = expand_line('║ . │ . ║ . ║')
    line2 = expand_line('╟───┼───╫───╢')
    line3 = expand_line('╠═══╪═══╬═══╣')
    line4 = expand_line('╚═══╧═══╩═══╝')

    symbol = ' ' + string.printable.replace(' ', '').replace('0', '')
    nums = [[''] + [symbol[n] for n in row] for row in br]
    print(line0)
    for r in range(1, side + 1):
        print("".join(n + s for n, s in zip(nums[r - 1], line1.split('.'))))
        print([line2, line3, line4][(r % side == 0) + (r % base == 0)])


def generate_sudoku(bs, empties):
    # pattern for a baseline valid solution
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample

    def shuffle(s):
        return sample(s, len(s))

    r_base = range(bs)
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    for p in map(int, sample(range(squares), empties)):
        board[p // side][p % side] = 0
    return board


if __name__ == '__main__':

    while True:
        base = 3
        side = base * base
        puzzle = np.asarray(generate_sudoku(base, side ** 2 - 28))  # 27 extremely hard long time to search.

        pn.engine(side.bit_length())

        board = np.asarray(pn.matrix(dimensions=(side, side)))
        pn.apply_single(board.flatten(), lambda x: 1 <= x <= side)

        for i in range(side):
            for j in range(side):
                if puzzle[i][j]:
                    assert board[i][j] == puzzle[i][j]

        for c, r in zip(board, board.T):
            pn.all_different(c)
            pn.all_different(r)

        for i in range(base):
            for j in range(base):
                pn.all_different(board[i * base:(i + 1) * base, j * base:(j + 1) * base].flatten())

        solutions = 0
        while pn.satisfy():
            solutions += 1
            if solutions > 1:
                break
        if solutions == 1:
            show(puzzle)
            show(np.vectorize(int)(board))
            break

"""
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║   │   │ 8 ║ 6 │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 4 │   │ 5 ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 1 │ 7 │   ║ 3 │ 2 │ 8 ║   │   │   ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │   │   ║   │ 6 │ 4 ║   │   │ 1 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │ 5 │   ║   │   │   ║   │   │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 6 │ 8 │ 4 ║ 5 │   │   ║ 3 │   │   ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║   │ 1 │ 3 ║   │   │   ║ 5 │ 4 │   ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║ 1 │ 9 │   ║ 8 │   │ 6 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║   │   │   ║   │   │ 7 ║   │   │ 3 ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝
╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗
║ 2 │ 3 │ 8 ║ 6 │ 4 │ 5 ║ 1 │ 7 │ 9 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 4 │ 6 │ 5 ║ 7 │ 1 │ 9 ║ 2 │ 3 │ 8 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 1 │ 7 │ 9 ║ 3 │ 2 │ 8 ║ 4 │ 6 │ 5 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ 3 │ 9 │ 2 ║ 8 │ 6 │ 4 ║ 7 │ 5 │ 1 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 7 │ 5 │ 1 ║ 9 │ 3 │ 2 ║ 6 │ 8 │ 4 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 6 │ 8 │ 4 ║ 5 │ 7 │ 1 ║ 3 │ 9 │ 2 ║
╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣
║ 9 │ 1 │ 3 ║ 2 │ 8 │ 6 ║ 5 │ 4 │ 7 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 5 │ 4 │ 7 ║ 1 │ 9 │ 3 ║ 8 │ 2 │ 6 ║
╟───┼───┼───╫───┼───┼───╫───┼───┼───╢
║ 8 │ 2 │ 6 ║ 4 │ 5 │ 7 ║ 9 │ 1 │ 3 ║
╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝
"""
