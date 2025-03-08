import pulp as lp

# Define the optimization problem
problem = lp.LpProblem("SAEV_Fleet_Optimization", lp.LpMinimize)

# Define decision variables
N = lp.LpVariable("Fleet_Size", lowBound=1, cat="Integer")
y = lp.LpVariable("Charging_Stations", lowBound=1, cat="Integer")

# Define parameters
d_i = 150  # Daily travel distance per vehicle (miles)
eta = 5  # Vehicle efficiency (miles/kWh)
b = 50  # Battery capacity per vehicle (kWh)
t_charge_i = 1.5  # Charging time per vehicle (hours)
T_avail = 8  # Available charging time per station per day (hours)
E_max = 500  # Maximum allowable carbon emissions (kg CO2)
f_x = 0.2  # Assumed emission factor

# Define objective function: total operational cost
C_fleet = 1000 * N  # Fleet operation cost
C_charging = 0.15 * (d_i / eta) * N  # Charging cost (assuming $0.15 per kWh)
C_emission = 50 * (d_i / eta) * N * f_x  # Carbon emission cost
problem += C_fleet + C_charging + C_emission

# Define constraints
problem += (d_i / eta) * N * f_x <= E_max  # Carbon emissions constraint
problem += t_charge_i * N <= y * T_avail  # Charging infrastructure constraint
problem += N >= 5  # Minimum fleet size requirement

# Solve the problem
problem.solve()

# Output results
print("Optimal Fleet Size:", lp.value(N))
print("Optimal Charging Stations:", lp.value(y))
print("Total Cost:", lp.value(problem.objective))
