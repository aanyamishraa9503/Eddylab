
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
