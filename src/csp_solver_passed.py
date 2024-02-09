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



def read_input(filename):
    with open(filename, 'r') as file:
        content = file.read().splitlines()

    sudoku_size = 9
    sudoku_board = [list(map(int, row.split())) for row in content[:sudoku_size]]

    num_cages = int(content[sudoku_size])
    print(num_cages)
    cages = []

    for i in range(sudoku_size + 1, sudoku_size + 1 + num_cages):
        cage_info = content[i].split(' > ')
        cage_cells = [(int(cell[0]), int(cell[1])) for cell in cage_info[0].split()]
        cage_sum = int(cage_info[1]) if cage_info[1] else 0  # Handle the case of an empty string
        cages.append({'cells': cage_cells, 'sum': cage_sum})

    return sudoku_board, cages

# Example usage with a file path
file_path = 'input.txt'
sudoku_board, cages = read_input(file_path)


killer_sudoku = KillerSudokuCSP(sudoku_board, cages)
solution = killer_sudoku.get_solution()

for row in solution:
    print(row)
