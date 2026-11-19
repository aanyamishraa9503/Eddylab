
import numpy as np


def simulate_braking(
    initial_angular_velocity,
    braking_coefficient,
    moment_of_inertia,
    simulation_time=10,
    time_steps=500
):
    """
    Simulates eddy current braking using a simplified
    linear torque-speed model.

    Assumption:
        Braking torque = k * angular velocity

    Returns:
        time, angular_velocity, braking_torque
    """

    if moment_of_inertia <= 0:
        raise ValueError("Moment of inertia must be positive.")

    if braking_coefficient < 0:
        raise ValueError("Braking coefficient cannot be negative.")

    if initial_angular_velocity < 0:
        raise ValueError("Initial angular velocity cannot be negative.")

    if simulation_time <= 0 or time_steps < 2:
        raise ValueError("Invalid simulation duration or time steps.")

    time = np.linspace(0, simulation_time, time_steps)

    angular_velocity = (
        initial_angular_velocity
        * np.exp(
            -(braking_coefficient / moment_of_inertia) * time
        )
    )

    braking_torque = braking_coefficient * angular_velocity

    return time, angular_velocity, braking_torque
def braking_coefficient_from_field(magnetic_flux_density, system_constant):
    """
    Estimates the effective braking coefficient using an assumed
    magnetic-field-squared relationship.

    Model assumption:
        k_eff = C * B^2

    B: Magnetic flux density (tesla)
    C: Effective system constant
    """

    if not np.isfinite(magnetic_flux_density) or not np.isfinite(system_constant):
        raise ValueError("Inputs must be finite numbers.")

    if magnetic_flux_density < 0:
        raise ValueError("Magnetic field strength cannot be negative.")

    if system_constant < 0:
        raise ValueError("System constant cannot be negative.")

    return system_constant * magnetic_flux_density**2

from physics import braking_coefficient_from_field

B1 = 0.2  # Tesla
B2 = 0.4  # Tesla
C = 0.05  # Illustrative system constant

k1 = braking_coefficient_from_field(B1, C)
k2 = braking_coefficient_from_field(B2, C)

print("\n===== MAGNETIC FIELD TEST =====")
print("Braking coefficient at 0.2 T:", k1)
print("Braking coefficient at 0.4 T:", k2)
print("Ratio k2/k1:", k2 / k1)
print("Expected ratio:", 4)
print("B-squared relationship verified:", np.isclose(k2 / k1, 4))
print("================================")
