"""Local Search Map Coloring."""
import random
import time
from helper_functions import create_csp_data_from_csv, create_restrictions_dict


def is_conflict(variable, assignment, restrictions):
    """Check if the current assignment causes a conflict."""
    for neighbor in assignment:
        if ((neighbor, variable) in restrictions or (variable, neighbor)
           in restrictions):
            if assignment[neighbor] == assignment[variable]:
                return True
    return False


def count_conflicts(variable, value, assignment, restrictions):
    """Count the number of conflicts if the variable is assigned the value."""
    assignment[variable] = value
    conflict_count = 0
    for neighbor in assignment:
        if ((neighbor, variable) in restrictions or (variable, neighbor)
           in restrictions):
            if assignment[neighbor] == value:
                conflict_count += 1
    del assignment[variable]
    return conflict_count


def min_conflicts(variables, domain, restrictions, max_steps=1000):
    """Min-Conflicts algorithm for solving CSP."""
    # Initialize with a random assignment
    current_assignment = {var: random.choice(list(domain)) for var in
                          variables}

    for step in range(max_steps):
        conflicted_vars = [var for var in variables if is_conflict(
            var, current_assignment, restrictions)]
        if not conflicted_vars:
            return current_assignment

        var = random.choice(conflicted_vars)
        min_conflict_value = min(domain, key=lambda value:
                                 count_conflicts(var, value,
                                                 current_assignment,
                                                 restrictions))
        current_assignment[var] = min_conflict_value

    return None  # No solution found within the given steps


df = create_csp_data_from_csv('CSPData.csv')
restrictions_dict = create_restrictions_dict(df)
variables = set(var for pair in restrictions_dict for var in pair)
colors = {'Red', 'Green', 'Blue', 'Orange'}

# Find a valid coloring
for i in range(5):
    start_time = time.time()
    valid_coloring = min_conflicts(variables, colors, restrictions_dict)
    if valid_coloring:
        break
end_time = time.time()


print(f"Function took {end_time - start_time:.6f} seconds and {i+1} iterations"
      " to complete.")
if valid_coloring:
    print("Valid map coloring:")
    for var, color in valid_coloring.items():
        print(f"{var}: {color}")
else:
    print("No valid coloring found.")
