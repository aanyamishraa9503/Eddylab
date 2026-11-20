
import numpy as np


# ==================================================
# 1. EDDY CURRENT BRAKING SIMULATION
# ==================================================

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

    Mathematical model:

        Braking torque magnitude = k * omega

        I * d(omega)/dt = -k * omega

        omega(t) = omega_0 * exp(-k*t/I)

    Returns:
        time
        angular_velocity
        braking_torque_magnitude

    Note:
        Returned braking torque is a positive magnitude.
        Its physical direction opposes the rotation.
    """

    values = [
        initial_angular_velocity,
        braking_coefficient,
        moment_of_inertia,
        simulation_time
    ]

    if not all(np.isfinite(value) for value in values):
        raise ValueError("All simulation inputs must be finite.")

    if moment_of_inertia <= 0:
        raise ValueError("Moment of inertia must be positive.")

    if braking_coefficient < 0:
        raise ValueError("Braking coefficient cannot be negative.")

    if initial_angular_velocity < 0:
        raise ValueError(
            "Initial angular velocity cannot be negative."
        )

    if simulation_time <= 0:
        raise ValueError("Simulation duration must be positive.")

    if (
        isinstance(time_steps, bool)
        or not isinstance(time_steps, (int, np.integer))
        or time_steps < 2
    ):
        raise ValueError(
            "Time steps must be an integer greater than or equal to 2."
        )

    # Generate time values.

    time = np.linspace(
        0,
        simulation_time,
        time_steps
    )

    # Analytical angular velocity solution.

    angular_velocity = (
        initial_angular_velocity
        * np.exp(
            -(braking_coefficient / moment_of_inertia) * time
        )
    )

    # Positive magnitude of braking torque.

    braking_torque = (
        braking_coefficient * angular_velocity
    )

    return (
        time,
        angular_velocity,
        braking_torque
    )


# ==================================================
# 2. BRAKING COEFFICIENT FROM MAGNETIC FIELD
# ==================================================

def braking_coefficient_from_field(
    magnetic_flux_density,
    system_constant
):
    """
    Estimates the effective braking coefficient.

    Model assumption:

        k_eff = C * B^2

    B: Magnetic flux density (tesla)
    C: Effective system constant

    This is a simplified educational relationship,
    not a universal experimentally established law.
    """

    if not np.isfinite(magnetic_flux_density):
        raise ValueError(
            "Magnetic flux density must be finite."
        )

    if not np.isfinite(system_constant):
        raise ValueError(
            "System constant must be finite."
        )

    if magnetic_flux_density < 0:
        raise ValueError(
            "Magnetic flux density cannot be negative."
        )

    if system_constant < 0:
        raise ValueError(
            "System constant cannot be negative."
        )

    return (
        system_constant * magnetic_flux_density**2
    )
