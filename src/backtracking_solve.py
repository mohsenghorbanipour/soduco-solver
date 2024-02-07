def solve_sudoku_with_cages(sudoku_board, cage_info):
    variables = {}
    domains = {}
    constraints_list = generate_constraints()  # Generate all constraints

    # Define variables and domains
    for i in range(9):
        for j in range(9):
            variables[f"cell_{i}_{j}"] = range(1, 10)
            domains[f"cell_{i}_{j}"] = range(1, 10)

    # Define constraints for cage totals
    cage_constraints = []
    for cage in cage_info:
        cells, total_value = cage
        cage_cells = [f"cell_{i // 9}_{i % 9}" for i in cells]
        cage_constraints.append((cage_cells, total_value))

    # Solve Sudoku
    solution = recursive_backtracking({}, variables, domains, constraints_list, cage_constraints)
    if solution:
        for i in range(9):
            for j in range(9):
                sudoku_board[i][j] = solution[f"cell_{i}_{j}"]
        return sudoku_board
    else:
        return None

def recursive_backtracking(assignment, variables, domains, constraints, cage_constraints):
    #todo
    return None

def forward_pruning(var, value, assignment, variables, domains, constraints):
    #todo

    return pruned_vars, pruned_domains

def select_unassigned_variable(assignment, variables, constraints):
    #todo
def order_domain_values(var, assignment, variables, domains, constraints):
    #todo

def count_conflicts(var, value, assignment, variables, domains, constraints):
    #todo
    return count

def is_consistent(var, value, assignment, constraints):
   #todo

def generate_constraints():
    #todo
    return constraints

