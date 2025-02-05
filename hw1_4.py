def newton_raphson(f, df, x0, iterations):
    x = x0
    for i in range(iterations):
        fx = f(x)
        dfx = df(x)
        delta_x = -fx / dfx
        x += delta_x
        print(f"Iteration {i+1}:")
        print(f"Current value: {fx}")
        print(f"Jacobian (f'(x)): {dfx}")
        print(f"Delta x: {delta_x}")
        print(f"Updated x: {x}")
        print("--------------")


def nr_method(f, df, x0, tol=1e-6, max_iterations=100):
    x = x0
    for i in range(max_iterations):
        fx = f(x)
        dfx = df(x)
        delta_x = -fx / dfx
        x += delta_x
        print(f"Iteration {i+1}:")
        print(f"Jacobian (f'(x)): {dfx}")
        print(f"Delta x: {delta_x}")
        print(f"Updated x: {x}")
        print()

        if abs(delta_x) < tol:
            print(f"Converged after {i + 1} iterations.")
            return x
    print("Maximum iterations reached without convergence.")
    return x


f = lambda x: x**3 - 0.5*x - 1
df = lambda x: 3*x**2 - 0.5

x0 = 1
iterations = 2
newton_raphson(f, df, x0, iterations)   # repeat iterations
# nr_method(f, df, x0)  # until converge