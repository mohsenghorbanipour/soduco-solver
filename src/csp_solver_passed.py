class KillerSudokuCSP:
    def __init__(self, sudoku_board, cages):
        self.board = sudoku_board
        self.cages = cages

    # Check if 'num' can be placed in the specified cell
    def is_valid(self, row, col, num):
        return (
            self.is_valid_row(row, num) and
            self.is_valid_col(col, num) and
            self.is_valid_nonet(row, col, num) and
            self.is_valid_cage(row, col, num)
        )
    
    # Check if 'num' exist in row
    def is_valid_row(self, row, num):
        return num not in self.board[row]

    # Check if 'num' exist in column
    def is_valid_col(self, col, num):
        return num not in [self.board[row][col] for row in range(9)]

    # Check if 'num' exist in  the specified 3x3 nonet 
    def is_valid_nonet(self, row, col, num):
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        return num not in [
            self.board[start_row + i][start_col + j]
            for i in range(3) for j in range(3)
        ]
    
    # Check if 'num' can placed in a cage
    def is_valid_cage(self, row, col, num):
        for cage in self.cages:
            if (row, col) in cage['cells']:
                total_sum = 0
                for (i, j) in cage['cells']:
                    if (i, j) != (row, col):
                        if(self.board[i][j] == 0): return True
                        total_sum += self.board[i][j]
                return total_sum + num == cage['sum']
        return False
        
    #Finds the first empty cell (cell with value 0) on the board.
    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None, None

    #Solves the Killer Sudoku puzzle using backtracking.
    def solve(self):
        empty_row, empty_col = self.find_empty_cell()

        if empty_row is None:
            return True  # Puzzle solved

        for num in range(1, 10):
            if self.is_valid(empty_row, empty_col, num):
                self.board[empty_row][empty_col] = num

                if self.solve():
                    return True  # Found a solution

                self.board[empty_row][empty_col] = 0  # Backtrack if no solution found

        return False  # No solution found

    def get_solution(self):
        self.solve()
        return self.board



sudoku_board = [
    [0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 0, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 8, 0, 0],
    [4, 0, 0, 9, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 8, 0]
]

cages = [
    {'cells': [(0, 0), (1, 0)], 'sum': 13},
    {'cells': [(0, 1), (1, 1),(2, 1), (2, 2)], 'sum': 21},
    {'cells': [(0, 2), (0, 3), (1, 2)], 'sum': 16},
    {'cells': [(0, 4), (0, 5)], 'sum': 13},
    {'cells': [(0,6), (0, 7)], 'sum': 4},
    {'cells': [(0,8), (1,8)], 'sum': 10},
    {'cells': [(1,3)], 'sum': 6},
    {'cells': [(1,4), (2,4),(2,3),(3,3), (3,2),], 'sum': 23},
    {'cells': [(1,5), (1,6),(1,7)], 'sum': 15},
    {'cells': [(2,0)], 'sum': 2},
    {'cells': [(2,5), (2,6), (2,7)], 'sum': 18},
    {'cells': [(2,8), (3,8), (4,8), (5,8), (3,7), (4,7)], 'sum': 32},
    {'cells': [(3,0), (4,0), (5,0)], 'sum': 21},
    {'cells': [(3,1), (4,1),(4,2),(5,2)], 'sum': 13},
    {'cells': [(3,4)], 'sum': 5},
    {'cells': [(3,5), (3,6)], 'sum': 11},
    {'cells': [(4,3), (4,4), (5,3)], 'sum': 12},
    {'cells': [(4,5), (4,6)], 'sum': 10},
    {'cells': [(5,1), (6,1),(6,2)], 'sum': 19},
    {'cells': [(5,4), (5,5)], 'sum': 13},
    {'cells': [(5,6), (5,7), (6,7)], 'sum': 9},
    {'cells': [(6,0), (7,0)], 'sum': 8},
    {'cells': [(6,3)], 'sum': 1},
    {'cells': [(6,4), (6,5)], 'sum':12},
    {'cells': [(6,6), (7,6), (7,7)], 'sum': 14},
    {'cells': [(6,8)], 'sum': 7},
    {'cells': [(7,1), (8,1), (8,0)], 'sum': 14},
    {'cells': [(7,2), (7,3), (7,4), (8,4)], 'sum': 21},
    {'cells': [(7,5), (8,5)], 'sum': 8},
    {'cells': [(7,8)], 'sum': 5},
    {'cells': [(8,2), (8,3)], 'sum': 12},
    {'cells': [(8,6), (8,7),(8,8)], 'sum': 17},

]


killer_sudoku = KillerSudokuCSP(sudoku_board, cages)
solution = killer_sudoku.get_solution()

for row in solution:
    print(row)
