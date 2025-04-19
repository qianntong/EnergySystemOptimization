import numpy as np
from scipy.optimize import minimize, Bounds, NonlinearConstraint
import matplotlib.pyplot as plt

cost_history = []

def callback(xk, state):
    cost = objective(xk)
    cost_history.append(cost)


# 参数
d_i = 325        
eta = 3.0         
b = 83.3          
t_charge_i = 2.4  
T_avail = 12     
soc_min = 0.2
gamma = 50        

c_carbon = 50     
c_e = 0.13        
c_s = 20000       
c_t = 1000        
c_v = 40 + d_i * 0.6         

E_max = 5
E_saev = 0.1
E_gas = 3

D = 17233
A = 86


# Emission factor as function of x
def f_x(x):
    return 0.5 * (1 - x)

def objective(vars):
    N, y, p, x = vars
    C_emission = c_carbon * (d_i / eta) * N * f_x(x)
    C_charging = c_e * (d_i / eta) * N * x
    C_station = c_s * p * y
    C_fleet = c_v * N
    return C_fleet + C_charging + C_station + C_emission

def constraint_funcs(vars):
    N, y, p, x = vars

    total_energy_demand = (d_i / eta) * N * x
    total_charging_capacity = gamma * p * y * T_avail
    max_vehicles_per_station = T_avail / t_charge_i

    return np.array([
        # 1. Carbon constraint (upper and lower)
        E_saev * x + E_gas * (1 - x) - E_max,  # <= 0
        -(E_saev * x + E_gas * (1 - x)),       # >= 0

        # 2. Charging capacity: demand ≤ supply
        total_energy_demand - total_charging_capacity,  # <= 0

        # 3. Charging time availability: each EV must get enough charging time
        t_charge_i * N * x - p * y * T_avail,  # <= 0

        # 4. Fleet size constraint
        (D / A) - N,  # N >= D/A

        N * x - y * p * max_vehicles_per_station,

        # 5. Penetration bounds (redundant if using Bounds, but reinforce here)
        -x,        # x >= 0
        x - 1,     # x <= 1
        0.1 - x,    # x >= 0.1

        p-3, # p >=3
        20-p, # p <=20
    ])

bounds = Bounds([D/A, 1, 3, 0.1], [np.inf, np.inf, 20, 1])

nonlinear_constraint = NonlinearConstraint(constraint_funcs, -np.inf, 0)

x0 = [D/A + 1, 2, 5, 0.2] #8203;:contentReference[oaicite:13]{index=13}

result = minimize(
    objective,
    x0,
    method='trust-constr',
    bounds=bounds,
    constraints=[nonlinear_constraint],
    callback=callback,
    options={"verbose": 1}
)


if result.success:
    N_opt, y_opt, p_opt, x_opt = result.x
    print("Optimal Fleet Size:", math.ceil(N_opt))
    print("Optimal Charging Stations:", math.ceil(y_opt))
    print("Optimal Penetration Rate:", round(x_opt, 2))
    print("Optimal Charger Numbers:", math.ceil(p_opt))
    print("Total Cost:", result.fun)

    cost_monotonic = []
    current_min = float('inf')
    for cost in cost_history:
        current_min = min(current_min, cost)
        cost_monotonic.append(current_min)

    plt.figure(figsize=(10, 6))
    # plt.plot(range(1, len(cost_history) + 1), cost_history, label='Original Cost History', marker='o')
    plt.plot(range(1, len(cost_monotonic) + 1), cost_monotonic, label='Monotonic Envelope', marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Total Cost')
    plt.title('Total Cost over Iterations')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    print("Optimization failed:", result.message)
