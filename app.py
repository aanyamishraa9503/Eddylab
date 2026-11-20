
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from physics import (
    simulate_braking,
    braking_coefficient_from_field
)

from eddylab_component import eddylab_3d


# ==================================================
# 1. PAGE CONFIGURATION AND SESSION STATE
# ==================================================

st.set_page_config(
    page_title="EddyLab | Virtual Physics Laboratory",
    page_icon="⚙️",
    layout="wide"
)

defaults = {
    "run_simulation": False,
    "experiment_trials": [],
    "magnet_air_gap": 0.24,
    "simulation_run_id": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# 2. APPLICATION HEADER
# ==================================================

st.title("⚙️ EDDYLAB")
st.subheader("Virtual Physics Laboratory")
st.caption("Interactive Simulation of Eddy Current Braking")

st.divider()


# ==================================================
# 3. EXPERIMENT OVERVIEW
# ==================================================

with st.expander("Experiment Overview", expanded=True):

    st.subheader("Aim")

    st.write(
        "To investigate how magnetic field strength affects "
        "the braking behaviour of a rotating conducting disc."
    )

    st.subheader("Hypothesis")

    st.write(
        "According to the simplified model, increasing magnetic "
        "field strength increases the effective braking coefficient "
        "and causes angular velocity to decrease more rapidly."
    )

    st.subheader("Experimental Variables")

    st.markdown("""
    - **Independent variable:** Magnetic field strength (T)
    - **Dependent variables:** Angular velocity, braking torque
      and rotational kinetic energy
    - **Controlled variables:** Initial angular velocity,
      moment of inertia and effective system constant
    """)

    st.subheader("Experiment Procedure")

    st.markdown("""
    1. Set the initial angular velocity of the disc.
    2. Set the moment of inertia.
    3. Choose a magnetic field strength.
    4. Keep the other parameters constant.
    5. Run the simulation.
    6. Observe the angular velocity and braking torque graphs.
    7. Repeat with different magnetic field strengths.
    8. Compare the results and draw a conclusion.
    """)

st.markdown("""
Explore how electromagnetic braking affects the rotational
motion of a conducting disc using a simplified mathematical model.
""")


# ==================================================
# 4. SIDEBAR - SIMULATION PARAMETERS
# ==================================================

st.sidebar.header("Simulation Controls")
st.sidebar.subheader("Experimental Parameters")

initial_velocity = st.sidebar.slider(
    "Initial Angular Velocity (rad/s)",
    min_value=10.0,
    max_value=200.0,
    value=100.0,
    step=5.0
)

moment_of_inertia = st.sidebar.slider(
    "Moment of Inertia (kg·m²)",
    min_value=0.01,
    max_value=0.10,
    value=0.02,
    step=0.005,
    format="%.3f"
)

magnetic_field = st.sidebar.slider(
    "Magnetic Field Strength (T)",
    min_value=0.1,
    max_value=1.0,
    value=0.5,
    step=0.05
)

system_constant = st.sidebar.slider(
    "Effective System Constant",
    min_value=0.001,
    max_value=0.1,
    value=0.05,
    step=0.001
)

simulation_time = st.sidebar.slider(
    "Reference Simulation Duration (seconds)",
    min_value=1,
    max_value=30,
    value=10
)


# ==================================================
# 5. SIMULATION BUTTONS
# ==================================================

st.sidebar.divider()

run_col, reset_col = st.sidebar.columns(2)

with run_col:

    if st.button(
        "Run Simulation",
        use_container_width=True
    ):

        st.session_state["run_simulation"] = True

        # A new ID starts a genuinely new simulation.
        st.session_state["simulation_run_id"] += 1


with reset_col:

    if st.button(
        "Reset",
        use_container_width=True
    ):

        st.session_state["run_simulation"] = False

        st.session_state["experiment_trials"] = []

        st.session_state["simulation_run_id"] = 0

        st.rerun()


# ==================================================
# 6. INTERACTIVE 3D APPARATUS
# ==================================================

st.divider()
st.header("Interactive 3D Eddy Current Brake")

st.caption(
    "Drag the magnetic assemblies along the shaft axis. "
    "The magnets move symmetrically around the copper disc. "
    "During an active simulation, magnet movement changes "
    "the braking effect continuously."
)

magnet_data = eddylab_3d(
    initial_angular_velocity=initial_velocity,
    moment_of_inertia=moment_of_inertia,
    magnetic_field=magnetic_field,
    system_constant=system_constant,
    simulation_time=simulation_time,
    air_gap=st.session_state["magnet_air_gap"],
    run_simulation=st.session_state["run_simulation"],
    run_id=st.session_state["simulation_run_id"],
    key="eddylab_3d"
)


# Receive magnet movement from the 3D component.

if isinstance(magnet_data, dict):

    if "air_gap" in magnet_data:

        new_gap = float(magnet_data["air_gap"])

        if np.isfinite(new_gap):

            st.session_state["magnet_air_gap"] = max(
                0.0,
                new_gap
            )

air_gap = st.session_state["magnet_air_gap"]

st.metric(
    "Magnet-to-Disc Air Gap",
    f"{air_gap:.3f} model units"
)


# ==================================================
# 7. PYTHON REFERENCE SIMULATION
# ==================================================

if st.session_state["run_simulation"]:

    reference_gap = 0.24

    # Calculate effective magnetic field using
    # the magnet gap at the time of calculation.

    effective_magnetic_field = np.clip(
        magnetic_field
        * (reference_gap / max(air_gap, 0.04)) ** 2,
        0.1,
        1.0
    )

    # Calculate effective braking coefficient.

    effective_k = braking_coefficient_from_field(
        effective_magnetic_field,
        system_constant
    )

    # Generate analytical reference results.

    time, omega, torque = simulate_braking(
        initial_velocity,
        effective_k,
        moment_of_inertia,
        simulation_time
    )

    kinetic_energy = (
        0.5 * moment_of_inertia * omega**2
    )

    angular_displacement = np.trapezoid(
        omega,
        time
    )

    st.success(
        "Reference calculations generated successfully. "
        "The 3D apparatus runs its own continuous simulation."
    )


    # ==================================================
    # 8. EFFECTIVE PARAMETERS
    # ==================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Effective Magnetic Field",
            f"{effective_magnetic_field:.3f} T"
        )

    with col2:

        st.metric(
            "Effective Braking Coefficient",
            f"{effective_k:.5f}"
        )

    with col3:

        st.metric(
            "Magnet-to-Disc Air Gap",
            f"{air_gap:.3f} model units"
        )


    # ==================================================
    # 9. MAIN SIMULATION RESULTS
    # ==================================================

    st.header("Simulation Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Initial Angular Velocity",
        f"{omega[0]:.2f} rad/s"
    )

    col2.metric(
        "Final Angular Velocity",
        f"{omega[-1]:.4f} rad/s"
    )

    col3.metric(
        "Initial Braking Torque",
        f"{torque[0]:.3f} N·m"
    )

    col4.metric(
        "Effective Braking Coefficient",
        f"{effective_k:.5f}"
    )

    st.caption(
        f"Magnetic field: {magnetic_field:.2f} T | "
        f"System constant: {system_constant:.3f}"
    )

    st.caption(
        "The reference braking coefficient is calculated using "
        "the simplified assumption k = C × B²."
    )


    # ==================================================
    # 10. EXPERIMENT TRIAL RECORDING
    # ==================================================

    st.divider()
    st.subheader("Experiment Trial Recording")

    if st.button("Record Current Trial"):

        trial_number = (
            len(st.session_state["experiment_trials"]) + 1
        )

        trial_data = {
            "Trial": trial_number,
            "Magnetic Field (T)": effective_magnetic_field,
            "Magnet Air Gap (model units)": air_gap,
            "Initial Angular Velocity (rad/s)": initial_velocity,
            "Moment of Inertia (kg·m²)": moment_of_inertia,
            "Effective k": effective_k,
            "Final Angular Velocity (rad/s)": omega[-1],
            "Final Braking Torque (N·m)": torque[-1],
            "Final Kinetic Energy (J)": kinetic_energy[-1]
        }

        st.session_state["experiment_trials"].append(
            trial_data
        )

        st.success(
            f"Trial {trial_number} recorded successfully!"
        )

    if st.session_state["experiment_trials"]:

        trial_df = pd.DataFrame(
            st.session_state["experiment_trials"]
        )

        st.dataframe(
            trial_df.round(5),
            use_container_width=True
        )

        st.download_button(
            "Download Experiment Trials (CSV)",
            trial_df.to_csv(index=False),
            file_name="eddylab_experiment_trials.csv",
            mime="text/csv"
        )

        if st.button("Clear All Trials"):

            st.session_state["experiment_trials"] = []

            st.rerun()

    else:

        st.info(
            "No trials recorded yet. Run a simulation and "
            "record your first trial."
        )


    # ==================================================
    # 11. REFERENCE EDDY CURRENT BRAKE ANIMATION
    # ==================================================

    st.divider()
    st.subheader("Reference Eddy Current Brake Animation")

    st.caption(
        "This separate 2D animation illustrates the calculated "
        "reference angular displacement. The interactive 3D "
        "apparatus above uses continuous magnet-responsive physics."
    )

    angular_position = np.zeros(len(time))

    angular_position[1:] = np.cumsum(
        0.5 * (omega[:-1] + omega[1:]) * np.diff(time)
    )

    frame_indices = np.linspace(
        0,
        len(time) - 1,
        min(60, len(time)),
        dtype=int
    )

    fig_animation = go.Figure()

    theta = np.linspace(0, 2 * np.pi, 100)

    # Conducting disc

    fig_animation.add_trace(
        go.Scatter(
            x=0.95 * np.cos(theta),
            y=0.95 * np.sin(theta),
            mode="lines",
            fill="toself",
            fillcolor="rgba(52, 152, 219, 0.12)",
            line=dict(color="#3498db", width=3),
            name="Conducting Disc"
        )
    )

    # Rotating radial marker

    fig_animation.add_trace(
        go.Scatter(
            x=[0, 0.85],
            y=[0, 0],
            mode="lines",
            line=dict(color="#f39c12", width=5),
            name="Rotating Marker"
        )
    )

    # Central hub

    fig_animation.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker=dict(size=14, color="#2c3e50"),
            name="Disc Centre"
        )
    )

    # Magnetic poles

    fig_animation.add_shape(
        type="rect",
        x0=-1.5,
        y0=0.3,
        x1=-1.05,
        y1=0.7,
        fillcolor="#e74c3c",
        line=dict(color="#e74c3c")
    )

    fig_animation.add_shape(
        type="rect",
        x0=1.05,
        y0=0.3,
        x1=1.5,
        y1=0.7,
        fillcolor="#3498db",
        line=dict(color="#3498db")
    )

    fig_animation.add_annotation(
        x=-1.275,
        y=0.5,
        text="N",
        showarrow=False,
        font=dict(color="white", size=18)
    )

    fig_animation.add_annotation(
        x=1.275,
        y=0.5,
        text="S",
        showarrow=False,
        font=dict(color="white", size=18)
    )

    # Conceptual eddy current loops

    for x_position in [-0.35, 0.35]:

        fig_animation.add_shape(
            type="circle",
            x0=x_position - 0.12,
            y0=-0.12,
            x1=x_position + 0.12,
            y1=0.12,
            line=dict(color="#e67e22", width=2)
        )

    # Animation frames

    animation_frames = []

    for frame_number, index in enumerate(frame_indices):

        angle = angular_position[index]

        animation_frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=[
                            0,
                            0.85 * np.cos(angle)
                        ],
                        y=[
                            0,
                            0.85 * np.sin(angle)
                        ]
                    )
                ],
                traces=[1],
                name=str(frame_number)
            )
        )

    fig_animation.frames = animation_frames

    fig_animation.update_layout(
        height=500,
        template="plotly_white",
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=50),

        xaxis=dict(
            range=[-1.8, 1.8],
            visible=False,
            scaleanchor="y"
        ),

        yaxis=dict(
            range=[-1.3, 1.3],
            visible=False
        ),

        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.5,
                y=-0.12,
                xanchor="center",

                buttons=[
                    dict(
                        label="▶ Play",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {
                                    "duration": 80,
                                    "redraw": True
                                },
                                "fromcurrent": True,
                                "transition": {
                                    "duration": 0
                                }
                            }
                        ]
                    ),

                    dict(
                        label="⏸ Pause",
                        method="animate",
                        args=[
                            [None],
                            {
                                "frame": {
                                    "duration": 0,
                                    "redraw": False
                                },
                                "mode": "immediate",
                                "transition": {
                                    "duration": 0
                                }
                            }
                        ]
                    )
                ]
            )
        ]
    )

    animation_col, readings_col = st.columns([2, 1])

    with animation_col:

        st.plotly_chart(
            fig_animation,
            use_container_width=True
        )

    with readings_col:

        st.subheader("Reference Simulation Readings")

        st.metric(
            "Initial Angular Velocity",
            f"{omega[0]:.2f} rad/s"
        )

        st.metric(
            "Final Angular Velocity",
            f"{omega[-1]:.4f} rad/s"
        )

        st.metric(
            "Initial Braking Torque",
            f"{torque[0]:.4f} N·m"
        )

        st.metric(
            "Final Braking Torque",
            f"{torque[-1]:.6f} N·m"
        )

        st.metric(
            "Reference Simulation Time",
            f"{time[-1]:.1f} s"
        )

    st.info(
        "The 2D animation uses calculated angular displacement "
        "from the simplified reference model. The magnetic poles "
        "and current loops are illustrative."
    )


    # ==================================================
    # 12. BRAKING STRENGTH INDICATOR
    # ==================================================

    st.divider()
    st.subheader("Braking Strength Indicator")

    braking_level = (
        effective_magnetic_field / 1.0
    ) ** 2 * 100

    indicator_col1, indicator_col2 = st.columns(2)

    indicator_col1.metric(
        "Relative Braking Level",
        f"{braking_level:.1f}%"
    )

    indicator_col2.metric(
        "Effective Braking Coefficient",
        f"{effective_k:.5f}"
    )

    st.progress(
        min(int(braking_level), 100)
    )

    st.caption(
        "The indicator represents the normalized B² relationship "
        "for the effective magnetic field. It is not experimentally "
        "measured efficiency."
    )


    # ==================================================
    # 13. AUTOMATIC PHYSICS OBSERVATION
    # ==================================================

    st.subheader("Physics Insights")

    st.write(
        f"At an effective magnetic field strength of "
        f"{effective_magnetic_field:.2f} T, "
        f"the reference braking coefficient is {effective_k:.5f}."
    )

    if effective_magnetic_field < 0.35:

        st.info(
            "Lower magnetic field: The model predicts a relatively "
            "weaker braking effect and a slower reduction in "
            "angular velocity."
        )

    elif effective_magnetic_field < 0.65:

        st.info(
            "Moderate magnetic field: The model predicts a "
            "moderate braking effect on the rotating disc."
        )

    else:

        st.info(
            "Higher magnetic field: The model predicts stronger "
            "braking and a faster reduction in angular velocity."
        )


    # ==================================================
    # 14. ANGULAR VELOCITY GRAPH
    # ==================================================

    st.divider()
    st.subheader("1. Angular Velocity vs Time")

    fig_velocity = go.Figure()

    fig_velocity.add_trace(
        go.Scatter(
            x=time,
            y=omega,
            mode="lines",
            name="Angular Velocity"
        )
    )

    fig_velocity.update_layout(
        xaxis_title="Time (seconds)",
        yaxis_title="Angular Velocity (rad/s)",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig_velocity,
        use_container_width=True
    )


    # ==================================================
    # 15. BRAKING TORQUE GRAPH
    # ==================================================

    st.subheader("2. Braking Torque vs Time")

    fig_torque = go.Figure()

    fig_torque.add_trace(
        go.Scatter(
            x=time,
            y=torque,
            mode="lines",
            name="Braking Torque"
        )
    )

    fig_torque.update_layout(
        xaxis_title="Time (seconds)",
        yaxis_title="Braking Torque (N·m)",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig_torque,
        use_container_width=True
    )


    # ==================================================
    # 16. MAGNETIC FIELD COMPARISON TABLE
    # ==================================================

    st.divider()
    st.subheader("3. Magnetic Field Comparison Data")

    comparison_fields = [0.2, 0.5, 0.8]

    comparison_results = []

    for field in comparison_fields:

        comparison_k = braking_coefficient_from_field(
            field,
            system_constant
        )

        comp_time, comp_omega, comp_torque = simulate_braking(
            initial_velocity,
            comparison_k,
            moment_of_inertia,
            simulation_time
        )

        comp_energy = (
            0.5 * moment_of_inertia * comp_omega**2
        )

        comparison_results.append({
            "Magnetic Field (T)": field,
            "Effective k": comparison_k,
            "Final Angular Velocity (rad/s)": comp_omega[-1],
            "Final Braking Torque (N·m)": comp_torque[-1],
            "Final Kinetic Energy (J)": comp_energy[-1]
        })

    comparison_df = pd.DataFrame(comparison_results)

    st.dataframe(
        comparison_df.round(6),
        use_container_width=True
    )

    st.download_button(
        "Download Magnetic Field Comparison (CSV)",
        comparison_df.to_csv(index=False),
        file_name="eddylab_field_comparison.csv",
        mime="text/csv"
    )

    st.caption(
        "Comparison assumes the same initial angular velocity, "
        "moment of inertia and system constant for all three cases."
    )


    # ==================================================
    # 17. KINETIC ENERGY GRAPH
    # ==================================================

    st.subheader("4. Rotational Kinetic Energy vs Time")

    fig_energy = go.Figure()

    fig_energy.add_trace(
        go.Scatter(
            x=time,
            y=kinetic_energy,
            mode="lines",
            name="Kinetic Energy"
        )
    )

    fig_energy.update_layout(
        xaxis_title="Time (seconds)",
        yaxis_title="Kinetic Energy (J)",
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig_energy,
        use_container_width=True
    )


    # ==================================================
    # 18. MAGNETIC FIELD COMPARISON GRAPH
    # ==================================================

    st.subheader("5. Magnetic Field Comparison")

    fig_comparison = go.Figure()

    for field in comparison_fields:

        comparison_k = braking_coefficient_from_field(
            field,
            system_constant
        )

        comparison_time, comparison_omega, _ = simulate_braking(
            initial_velocity,
            comparison_k,
            moment_of_inertia,
            simulation_time
        )

        fig_comparison.add_trace(
            go.Scatter(
                x=comparison_time,
                y=comparison_omega,
                mode="lines",
                name=f"{field:.1f} T"
            )
        )

    fig_comparison.update_layout(
        title="Effect of Magnetic Field on Angular Velocity",
        xaxis_title="Time (seconds)",
        yaxis_title="Angular Velocity (rad/s)",
        template="plotly_white",
        height=450,
        legend_title="Magnetic Field"
    )

    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )


    # ==================================================
    # 19. ADDITIONAL SIMULATION RESULTS
    # ==================================================

    st.divider()
    st.subheader("6. Additional Simulation Data")

    result_col1, result_col2 = st.columns(2)

    result_col1.metric(
        "Final Kinetic Energy",
        f"{kinetic_energy[-1]:.6f} J"
    )

    result_col2.metric(
        "Angular Displacement",
        f"{angular_displacement:.3f} rad"
    )


    # ==================================================
    # 20. OBSERVATION TABLE
    # ==================================================

    st.subheader("7. Virtual Experiment Observation Table")

    observations = pd.DataFrame({
        "Time (s)": time,
        "Angular Velocity (rad/s)": omega,
        "Braking Torque (N·m)": torque,
        "Kinetic Energy (J)": kinetic_energy
    })

    st.dataframe(
        observations.iloc[::25].round(5),
        use_container_width=True
    )

    st.download_button(
        "Download Simulation Data (CSV)",
        observations.to_csv(index=False),
        file_name="eddylab_observations.csv",
        mime="text/csv"
    )


# ==================================================
# 21. INTRODUCTION SCREEN
# ==================================================

else:

    st.info(
        "Adjust the experimental parameters and click Run Simulation."
    )

    st.subheader("How the Simulation Works")

    st.markdown("""
    1. Set the initial angular velocity of the disc.
    2. Adjust the moment of inertia.
    3. Set the magnetic field strength.
    4. Adjust the effective system constant.
    5. Select the reference simulation duration.
    6. Run the simulation and examine the resulting graphs.

    **Magnetic-field relationship:**
    """)

    st.latex(r"k_{\mathrm{eff}} = CB^2")

    st.markdown("**Braking torque:**")

    st.latex(r"\tau_b = k_{\mathrm{eff}}\omega")

    st.markdown("**Rotational equation of motion:**")

    st.latex(r"I\frac{d\omega}{dt}=-k_{\mathrm{eff}}\omega")

    st.markdown("**Angular velocity solution:**")

    st.latex(
        r"\omega(t)=\omega_0e^{-k_{\mathrm{eff}}t/I}"
    )

    st.caption(
        "Note: This is an idealized mathematical model. "
        "The B² relationship is a simplified assumption, and "
        "the effective system constant requires calibration "
        "against a real physical system."
    )


# ==================================================
# 22. FOOTER
# ==================================================

st.divider()

st.caption(
    "EDDYLAB | Interactive Virtual Physics Laboratory | "
    "Educational Simulation Prototype"
)
