"""CSP Algorithms."""
import time
from helper_functions import create_csp_data_from_csv, create_restrictions_dict


def is_valid_assignment(variable, domain_element, assignment, restrictions):
    """Check if assigning 'color' to 'variable' satisfies all constraints."""
    for neighbor in assignment:
        if (neighbor, variable) in restrictions:
            if assignment[neighbor] == domain_element:
                return False
    return True


def backtrack_coloring(variables_set, domain, assignment, restrictions):
    """Depth first search algorithm to find valid map coloring."""
    if len(assignment) == len(variables_set):
        # All variables are assigned; valid coloring found
        return assignment

    # unassigned_var = next(var for var in variables if var not in assignment)
    # Select the unassigned variable with the minimum remaining values (MRV)
    unassigned_var = min(
        (var for var in variables_set if var not in assignment),
        key=lambda var: len([color for color in domain if is_valid_assignment(
            var, color, assignment, restrictions)])
    )
    for item in domain:
        if is_valid_assignment(unassigned_var, item, assignment,
                               restrictions):
            assignment[unassigned_var] = item
            result = backtrack_coloring(variables_set, domain, assignment,
                                        restrictions)
            if result:
                return result
            assignment.pop(unassigned_var)

    return None  # Backtrack


df = create_csp_data_from_csv('CSPData.csv')
restrictions_dict = create_restrictions_dict(df)
variables = set(var for pair in restrictions_dict for var in pair)
colors = {'Red', 'Green', 'Blue', 'Orange'}

# Find a valid coloring
start_time = time.time()
valid_coloring = backtrack_coloring(variables, colors, {}, restrictions_dict)
end_time = time.time()
print(f"Function took {end_time - start_time:.6f} seconds to complete")
if valid_coloring:
    print("Valid map coloring:")
    for var, color in valid_coloring.items():
        print(f"{var}: {color}")
else:
    print("No valid coloring found.")
