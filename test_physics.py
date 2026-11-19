
import numpy as np
from physics import simulate_braking

# Simulation parameters
omega_0 = 100
k = 0.05
I = 0.02
duration = 10

# Run simulation
time, omega, torque = simulate_braking(
    omega_0, k, I, duration
)

# Analytical solution
expected_omega = omega_0 * np.exp(-(k / I) * time)

# Validation
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

print("====================================")
