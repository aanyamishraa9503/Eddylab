from pathlib import Path

import streamlit.components.v1 as components


# ==================================================
# COMPONENT BUILD DIRECTORY
# ==================================================

BUILD_DIR = (
    Path(__file__).resolve().parent.parent
    / "frontend"
    / "dist"
)


# ==================================================
# REGISTER THREE.JS COMPONENT
# ==================================================

_eddylab_component = components.declare_component(
    "eddylab_3d",
    path=str(BUILD_DIR)
)


# ==================================================
# COMPONENT FUNCTION
# ==================================================

def eddylab_3d(
    initial_angular_velocity=100.0,
    moment_of_inertia=0.02,
    magnetic_field=0.5,
    system_constant=0.05,
    simulation_time=10,
    air_gap=0.24,
    run_simulation=False,
    run_id=0,
    key=None
):
    """
    Displays the interactive EddyLab 3D apparatus.

    The Three.js frontend handles continuous disc rotation
    and dynamically calculates braking from the current
    magnet-to-disc air gap.

    Python supplies the experimental parameters and
    simulation control state.
    """

    return _eddylab_component(

        initial_angular_velocity=initial_angular_velocity,

        moment_of_inertia=moment_of_inertia,

        magnetic_field=magnetic_field,

        system_constant=system_constant,

        simulation_time=simulation_time,

        air_gap=air_gap,

        run_simulation=run_simulation,

        run_id=run_id,

        key=key,

        default=None
    )