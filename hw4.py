import numpy as np

def solve_dc_power_flow(theta1_deg, theta2_deg, G1, D3, X):
    """
    Solves the DC power flow for the 3-bus system.

    Parameters:
        theta1_deg (float): voltage angle at bus 1 (degrees)
        theta2_deg (float): voltage angle at bus 2 (degrees)
        G1 (float): generation at bus 1 (W)
        D3 (float): demand at bus 3 (W)
        X (float): reactance of all lines (Ω)

    Returns:
        dict: containing theta3, D2, G3, and line flows
    """
    # Convert to radians
    theta1 = np.radians(theta1_deg)
    theta2 = np.radians(theta2_deg)
    B = 1 / X  # susceptance

    # Solve for theta3
    # P1 = B*(theta1 - theta2) + B*(theta1 - theta3) = G1
    theta3 = (B * (theta1 - theta2) - G1) / B

    # Solve for D2
    # P2 = -D2 = B*(theta2 - theta1) + B*(theta2 - theta3)
    P2 = B * (theta2 - theta1) + B * (theta2 - theta3)
    D2 = -P2

    # Solve for G3
    # P3 = G3 - D3 = B*(theta3 - theta1) + B*(theta3 - theta2)
    P3 = B * (theta3 - theta1) + B * (theta3 - theta2)
    G3 = P3 + D3

    # Line flows
    P_12 = B * (theta1 - theta2)
    P_13 = B * (theta1 - theta3)
    P_32 = B * (theta3 - theta2)

    return {
        "theta3_rad": theta3,
        "theta3_deg": np.degrees(theta3),
        "D2": D2,
        "G3": G3,
        "P_1_to_2": P_12,
        "P_1_to_3": P_13,
        "P_3_to_2": P_32
    }

theta1_deg = 0
theta2_deg = -9
G1 = 1.0
D3 = 0.8
X = 0.1

results = solve_dc_power_flow(theta1_deg, theta2_deg, G1, D3, X)

print("=== DC Power Flow Results ===")
print(f"Theta3 = {results['theta3_deg']:.2f}° ({results['theta3_rad']:.4f} rad)")
print(f"D2 = {results['D2']:.4f} W")
print(f"G3 = {results['G3']:.4f} W")
print()
print("Line flows:")
print(f"P_1->2 = {results['P_1_to_2']:.4f} W")
print(f"P_1->3 = {results['P_1_to_3']:.4f} W")
print(f"P_3->2 = {results['P_3_to_2']:.4f} W")
