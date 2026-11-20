
import numpy as np

from physics import (
    simulate_braking,
    braking_coefficient_from_field
)


# ==================================================
# 1. SIMULATION PARAMETERS
# ==================================================

omega_0 = 100
k = 0.05
I = 0.02
duration = 10


# ==================================================
# 2. RUN BRAKING SIMULATION
# ==================================================

time, omega, torque = simulate_braking(
    omega_0, k, I, duration
)


# ==================================================
# 3. ANALYTICAL VALIDATION
# ==================================================

expected_omega = omega_0 * np.exp(
    -(k / I) * time
)

error = np.max(np.abs(omega - expected_omega))


print("\n===== EDDYLAB MODEL VALIDATION =====")

print("Initial angular velocity:", omega[0])
print("Final angular velocity:", omega[-1])

print("Initial braking torque:", torque[0])
print("Final braking torque:", torque[-1])

print("Maximum analytical error:", error)

print("\nVelocity decreases:", np.all(np.diff(omega) <= 0))
print("Torque decreases:", np.all(np.diff(torque) <= 0))
print("Analytical agreement:", np.allclose(omega, expected_omega))


# ==================================================
# 4. MAGNETIC FIELD RELATIONSHIP TEST
# ==================================================

B1 = 0.2
B2 = 0.4
C = 0.05

k1 = braking_coefficient_from_field(B1, C)
k2 = braking_coefficient_from_field(B2, C)

ratio = k2 / k1

print("\n===== MAGNETIC FIELD TEST =====")

print("Magnetic field 1:", B1, "T")
print("Magnetic field 2:", B2, "T")

print("Braking coefficient at 0.2 T:", k1)
print("Braking coefficient at 0.4 T:", k2)

print("Coefficient ratio:", ratio)
print("Expected ratio:", 4)

print(
    "B-squared relationship verified:",
    np.isclose(ratio, 4)
)

print("================================")
