def solve_sudoku_csp(sudoku_board, cage_info):
    variables = {}
    domains = {}
    constraints = []

    # Define variables and domains
    for i in range(9):
        for j in range(9):
            variables[(i, j)] = range(1, 10)
            domains[(i, j)] = range(1, 10)

    # Define constraints for rows and columns
    for i in range(9):
        for j in range(9):
            for k in range(j + 1, 9):
                constraints.append(((i, j), (i, k)))
                constraints.append(((j, i), (k, i)))

    # Define constraints for 3x3 squares
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            for x in range(3):
                for y in range(3):
                    for a in range(3):
                        for b in range(3):
                            if x != a or y != b:
                                constraints.append(((i+x, j+y), (i+a, j+b)))

    # Define constraints for cage totals
    for cage in cage_info:
        cells, total_value = cage
        cage_cells = [(i // 9 * 10 + i % 9, j // 9 * 10 + j % 9) for i in cells for j in cells]
        constraints.append((cage_cells, total_value))

    # Solve CSP
    solution = backtracking_search(variables, domains, constraints)
    if solution:
        for i in range(9):
            for j in range(9):
                sudoku_board[i][j] = solution[(i, j)]
        return sudoku_board
    else:
        return None

def backtracking_search(variables, domains, constraints):
    assignment = {}
    return recursive_backtracking(assignment, variables, domains, constraints)

def recursive_backtracking(assignment, variables, domains, constraints):
    if len(assignment) == len(variables):
        return assignment

    var = select_unassigned_variable(assignment, variables)
    for value in order_domain_values(var, assignment, variables, domains):
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value
            result = recursive_backtracking(assignment, variables, domains, constraints)
            if result:
                return result
            assignment.pop(var)
    return None

def select_unassigned_variable(assignment, variables):
    for var in variables:
        if var not in assignment:
            return var

def order_domain_values(var, assignment, variables, domains):
    return domains[var]

def is_consistent(var, value, assignment, constraints):
    for other_var in assignment:
        if (var, other_var) in constraints or (other_var, var) in constraints:
            if assignment[other_var] == value:
                return False
    return True
