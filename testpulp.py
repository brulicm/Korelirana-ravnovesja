import pulp

# Coefficients of the objective function
c = [-1, -1, -1, -1]  # To maximize, multiply coefficients by -1

# Coefficients of inequality constraints
A = [[1, -1, 0, 0], [0, 0, -1, 1], [1, 0, -1, 0], [0, -1, 0, 1]]

# Right-hand side of inequality constraints
b = [0, 0, 0, 0]

# Coefficients of equality constraint
A_eq = [[1, 1, 1, 1]]

# Right-hand side of equality constraint
b_eq = [1]

# Bounds for decision variables
x_bounds = (0, None)  # x_i >= 0 for all i

solutions = []

while len(solutions) < 3:  # Find three solutions
    # Create a LP maximization problem
    problem = pulp.LpProblem("Linear_Program", pulp.LpMaximize)

    # Define decision variables
    x = [pulp.LpVariable(f"x{i}", lowBound=x_bounds[0], upBound=x_bounds[1]) for i in range(len(c))]

    # Add objective function
    problem += sum(c[i] * x[i] for i in range(len(c)))

    # Add inequality constraints
    for i in range(len(b)):
        problem += sum(A[i][j] * x[j] for j in range(len(c))) <= b[i]

    # Add equality constraint
    problem += sum(A_eq[0][j] * x[j] for j in range(len(c))) == b_eq[0]

    # Add a constraint to exclude previous solutions
    if solutions:
        for sol in solutions:
            problem += sum(sol[i] * x[i] for i in range(len(sol))) != sum(sol)

    # Solve the problem
    problem.solve()

    if problem.status == pulp.LpStatusOptimal:
        # Store the solution
        solutions.append([pulp.value(var) for var in x])
    else:
        print("No more solutions found.")
        break

# Print the results
print("Multiple Solutions Found:")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}:")
    for j, val in enumerate(sol):
        print(f"x{j+1} =", val)
    print()
