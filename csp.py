import pandas as pd
import time

def create_csp_data_from_csv(csv_file_path):
    # Read the CSV file into a DataFrame
    return pd.read_csv(csv_file_path, index_col=0)

def create_restrictions_dict(csp_data):
    elements = csp_data.columns
    restrictions_dict = {}
    
    for col in elements:
        for row in elements:
            if row == col:
                continue
            value = csp_data.at[col, row]
            if pd.isna(value):
                value = csp_data.at[row, col]
            
            # Populate the restrictions_dict
            if value == 1.0:
                restrictions_dict[(col, row)] = value
    
    return restrictions_dict

def is_valid_assignment(variable, color, assignment, restrictions_dict):
    """
    Check if assigning 'color' to 'variable' satisfies all constraints.
    """
    for neighbor in assignment:
        if (neighbor, variable) in restrictions_dict:
            if assignment[neighbor] == color:
                return False
    return True

def backtrack_coloring(variables, domain, assignment, restrictions_dict):
    if len(assignment) == len(variables):
        # All variables are assigned; valid coloring found
        return assignment
    
    #unassigned_var = next(var for var in variables if var not in assignment)
    # Select the unassigned variable with the minimum remaining values (MRV)
    unassigned_var = min(
        (var for var in variables if var not in assignment),
        key=lambda var: len([color for color in domain if is_valid_assignment(var, color, assignment, restrictions_dict)])
    )
    for color in domain:
        if is_valid_assignment(unassigned_var, color, assignment, restrictions_dict):
            assignment[unassigned_var] = color
            result = backtrack_coloring(variables, domain, assignment, restrictions_dict)
            if result:
                return result
            assignment.pop(unassigned_var)
    
    return None  # Backtrack

df = create_csp_data_from_csv('CSPData.csv')
restrictions_dict = create_restrictions_dict(df)
variables = set(var for pair in restrictions_dict for var in pair)
domain = {'Red', 'Green', 'Blue', 'Yellow'}  # Set of available colors

# Find a valid coloring
start_time = time.time()
valid_coloring = backtrack_coloring(variables, domain, {}, restrictions_dict)
end_time = time.time()
print(f"Function took {end_time - start_time:.6f} seconds to complete")
if valid_coloring:
    print("Valid map coloring:")
    for var, color in valid_coloring.items():
        print(f"{var}: {color}")
else:
    print("No valid coloring found.")






