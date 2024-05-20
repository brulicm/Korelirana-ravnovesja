from scipy.optimize import linprog

# Coefficients of the objective function
c = [1, 0, 0, -1]  

# Coefficients of inequality constraints
A = [[-2, 1, 0, 0], [0, 0, -2, -1], [-1, 0, 2, 0], [0,1, 0, -2]]

# Right-hand side of inequality constraints
b = [0, 0, 0, 0]

# Coefficients of equality constraint
A_eq = [[1, 1, 1, 1]]

# Right-hand side of equality constraint
b_eq = [1]

# Bounds for decision variables
x_bounds = (0, None)  # x_i >= 0 for all i

# Solve the linear program
result = linprog(c=c, A_ub=A, b_ub=b, A_eq=A_eq, b_eq=b_eq, bounds=[x_bounds] * 4)

num_optimal_solutions = 0

# Output the result
if result.success:
    print("Optimal solution found:")
    print("Objective value:", -result.fun)  # Convert back to maximize
    print("Decision variables:", result.x)
    
    # Increment the counter if an optimal solution is found
    num_optimal_solutions += 1
    
    # Store the solution
    found_solutions = [result.x]
else:
    print("Optimization failed:", result.message)

# Print the number of optimal solutions found
print("Number of optimal solutions found:", num_optimal_solutions)

