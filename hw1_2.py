import sympy as sp

x1, x2, miu1, miu2 = sp.symbols('x1 x2 miu1 miu2')

objective = -x1**2 - x2**2
constraint1 = x1**2 - x2  # x1^2 - x2 <= 0
constraint2 = 2*x1 + x2 - 8  # 2*x1 + x2 <= 8

L = objective + miu1 * constraint1 + miu2 * constraint2

grad_L = [
    sp.diff(L, x1),
    sp.diff(L, x2),
    sp.diff(L, miu1),
    sp.diff(L, miu2)
]

complementary_conditions = [
    miu1 * constraint1,  # miu1 * (x1^2 - x2) = 0
    miu2 * constraint2   # miu2 * (2*x1 + x2 - 8) = 0
]

inequality_conditions = [
    constraint1 <= 0,  # x1^2 - x2 <= 0
    constraint2 <= 0,  # 2*x1 + x2 - 8 <= 0
    miu1 >= 0,         # miu1 >= 0
    miu2 >= 0          # miu2 >= 0
]

conditions = grad_L + complementary_conditions + inequality_conditions

solutions = sp.solve(grad_L + complementary_conditions, (x1, x2, miu1, miu2), dict=True)

valid_solutions = []
for sol in solutions:
    if all(c.subs(sol) for c in inequality_conditions):
        valid_solutions.append(sol)

for sol in valid_solutions:
    print(sol)
    x1_val = sol[x1]
    x2_val = sol[x2]
    miu1_val = sol[miu1]
    miu2_val = sol[miu2]
    objective_val = objective.subs({x1: x1_val, x2: x2_val})
    print(f"x1 = {x1_val}, x2 = {x2_val}, miu1 = {miu1_val}, miu2 = {miu2_val}, Objective = {objective_val}")
    print(f"verification: -2 * x2 + miu1 + miu2 = -2 * {x1_val} + {miu1_val} + {miu2_val} = {-2 * x1_val + miu1_val + miu2_val}")