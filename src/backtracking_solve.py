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
    if len(assignment) == len(variables):
        return assignment

    var = select_unassigned_variable(assignment, variables, constraints)
    for value in order_domain_values(var, assignment, variables, domains, constraints):
        if is_consistent(var, value, assignment, constraints):
            assignment[var] = value
            # Apply forward pruning
            pruned_vars, pruned_domains = forward_pruning(var, value, assignment, variables, domains, constraints)
            if pruned_vars is not None:
                result = recursive_backtracking(assignment, pruned_vars, pruned_domains, constraints, cage_constraints)
                if result:
                    return result
            assignment.pop(var)
    return None

def forward_pruning(var, value, assignment, variables, domains, constraints):
    pruned_vars = variables.copy()
    pruned_domains = domains.copy()

    pruned_vars.pop(var)
    pruned_domains.pop(var)

    for other_var in variables:
        if (var, other_var) in constraints or (other_var, var) in constraints:
            if other_var not in assignment and value in pruned_domains[other_var]:
                pruned_domains[other_var] = [v for v in pruned_domains[other_var] if v != value]
                if not pruned_domains[other_var]:
                    return None, None

    return pruned_vars, pruned_domains

def select_unassigned_variable(assignment, variables, constraints):
    # MRV heuristic
    unassigned_variables = [var for var in variables if var not in assignment]
    if not unassigned_variables:
        return None  # Or handle the case where there are no unassigned variables
    mrv_variable = min(unassigned_variables, key=lambda var: len(variables[var]))
    return mrv_variable

def order_domain_values(var, assignment, variables, domains, constraints):
    # LCV heuristic
    domain_values = domains[var] if var in domains else []
    sorted_values = sorted(domain_values, key=lambda value: count_conflicts(var, value, assignment, variables, domains, constraints))
    return sorted_values

def count_conflicts(var, value, assignment, variables, domains, constraints):
    # Count conflicts for LCV heuristic
    count = 0
    for other_var in assignment:
        if (var, other_var) in constraints or (other_var, var) in constraints:
            if assignment[other_var] == value:
                count += 1
    return count

def is_consistent(var, value, assignment, constraints):
    for other_var in assignment:
        if (var, other_var) in constraints or (other_var, var) in constraints:
            if assignment[other_var] == value:
                return False
    return True

def generate_constraints():
    constraints = []

    # Constraints for rows and columns
    for i in range(9):
        for j in range(9):
            for k in range(j + 1, 9):
                constraints.append((f"cell_{i}_{j}", f"cell_{i}_{k}"))
                constraints.append((f"cell_{j}_{i}", f"cell_{k}_{i}"))

    # Constraints for 3x3 squares
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            for x in range(3):
                for y in range(3):
                    for a in range(3):
                        for b in range(3):
                            if x != a or y != b:
                                constraints.append((f"cell_{i+x}_{j+y}", f"cell_{i+a}_{j+b}"))

    return constraints

