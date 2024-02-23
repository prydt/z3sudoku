import z3


def make_variables(r, c):
    vars = dict()
    for r_i in range(r):
        for c_i in range(c):
            for digit in range(1, 10):
                vars[(r_i, c_i, digit)] = z3.Bool(f"{r_i}_{c_i}_{digit}")
    return vars


class SudokuBoard:

    def __init__(self, board) -> None:
        self.board = board
        self.num_rows = len(board)
        self.num_cols = len(board[0])
        self.vars = make_variables(self.num_rows, self.num_cols)

    def get_row(self, r_i):
        return self.board[r_i]

    def get_col(self, c_i):
        return [row[c_i] for row in self.board]

    def get_square(self, r_i, c_i):
        assert r_i in range(3)
        assert c_i in range(3)

        return [val for row in board[r_i : r_i + 3] for val in row[c_i : c_i + 3]]

    def get_var(self, r, c, digit):
        assert digit in range(1, 10)
        return self.vars[(r, c, digit)]

    def get_value(self, r, c):
        return self.board[r][c]


def require_distinct(vars):
    assert len(vars) >= 2

    expr = False
    for i, var in enumerate(vars):
        other_vars_negated = z3.And(*[z3.Not(v) for j, v in enumerate(vars) if j != i])
        expr = z3.Or(expr, z3.And(var, other_vars_negated))

    return expr


def one_digit_per_slot_constraint(board: SudokuBoard):
    expr = True
    for r_i in range(board.num_rows):
        for c_i in range(board.num_cols):
            digit_vars = [board.get_var(r_i, c_i, digit) for digit in range(1, 10)]
            expr = z3.And(expr, require_distinct(digit_vars))

    return expr


def row_constraint(board: SudokuBoard):
    expr = True
    for r_i in range(board.num_rows):
        # per row, require distinct vals
        for digit in range(1, 10):
            vars = [board.get_var(r_i, c_i, digit) for c_i in range(board.num_cols)]
            expr = z3.And(expr, require_distinct(vars))

        # make sure row doesn't contain already set vals
        for c_i in range(board.num_cols):
            digit = board.get_value(r_i, c_i)
            if digit != 0:
                expr = z3.And(expr, board.get_var(r_i, c_i, digit))

    return expr


def col_constraint(board: SudokuBoard):
    expr = True
    for c_i in range(board.num_cols):
        # per col, require distinct vals
        for digit in range(1, 10):
            vars = [board.get_var(r_i, c_i, digit) for r_i in range(board.num_rows)]
            expr = z3.And(expr, require_distinct(vars))

        # make sure row doesn't contain already set vals
        for r_i in range(board.num_rows):
            digit = board.get_value(r_i, c_i)
            if digit != 0:
                expr = z3.And(expr, board.get_var(r_i, c_i, digit))

    return expr


def square_constraint(board: SudokuBoard):
    expr = True

    for r_shift in [0, 3, 6]:
        for c_shift in [0, 3, 6]:
            for digit in range(1, 10):
                vars = [
                    board.get_var(r_i, c_i, digit)
                    for r_i in range(r_shift, r_shift + 3)
                    for c_i in range(c_shift, c_shift + 3)
                ]
                expr = z3.And(expr, require_distinct(vars))
    return expr


if __name__ == "__main__":

    # NYT easy sudoku from Feb 23, 2024
    board_contents = [
        [4, 7, 0, 0, 6, 0, 0, 0, 0],
        [3, 0, 0, 4, 9, 7, 0, 8, 0],
        [0, 0, 6, 3, 8, 0, 1, 7, 0],
        [0, 6, 5, 0, 3, 9, 0, 2, 7],
        [0, 0, 9, 5, 2, 0, 8, 0, 0],
        [0, 0, 2, 0, 0, 0, 5, 0, 1],
        [6, 0, 0, 0, 0, 3, 0, 1, 5],
        [0, 2, 0, 9, 0, 8, 0, 0, 3],
        [9, 0, 3, 0, 5, 6, 0, 0, 0],
    ]

    board = SudokuBoard(board_contents)

    solver = z3.Solver()
    solver.add(one_digit_per_slot_constraint(board))
    solver.add(row_constraint(board))
    solver.add(col_constraint(board))
    solver.add(square_constraint(board))

    check = solver.check()
    if check == z3.sat:
        # we succeeded! -- print solution
        model = solver.model()

        solution_board = [[0] * 9 for _ in range(9)]
        for key in model:
            if model[key]:
                (r, c, digit) = str(key).split("_")
                r = int(r)
                c = int(c)
                digit = int(digit)
                solution_board[r][c] = digit
        for row in solution_board:
            print(row)
