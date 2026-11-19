
import streamlit as st
import numpy as np
import plotly.graph_objects as go

from physics import simulate_braking


# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------

st.set_page_config(
    page_title="EddyLab | Virtual Physics Laboratory",
    page_icon="⚙️",
    layout="wide"
)


# ------------------------------------------------
# APPLICATION HEADER
# ------------------------------------------------

st.title("⚙️ EDDYLAB")
st.subheader("Virtual Physics Laboratory")
st.caption("Interactive Simulation of Eddy Current Braking")

st.divider()

st.markdown("""
Explore how electromagnetic braking affects the rotational
motion of a conducting disc using a simplified mathematical model.
""")


# ------------------------------------------------
# SIDEBAR - SIMULATION PARAMETERS
# ------------------------------------------------

st.sidebar.header("Simulation Controls")

st.sidebar.subheader("Experimental Parameters")

initial_velocity = st.sidebar.slider(
    "Initial Angular Velocity (rad/s)",
    min_value=10.0,
    max_value=200.0,
    value=100.0,
    step=5.0
)

braking_coefficient = st.sidebar.slider(
    "Effective Braking Coefficient (N·m·s/rad)",
    min_value=0.001,
    max_value=0.100,
    value=0.050,
    step=0.001,
    format="%.3f"
)

moment_of_inertia = st.sidebar.slider(
    "Moment of Inertia (kg·m²)",
    min_value=0.01,
    max_value=0.10,
    value=0.02,
    step=0.005,
    format="%.3f"
)

simulation_time = st.sidebar.slider(
    "Simulation Duration (seconds)",
    min_value=1,
    max_value=30,
    value=10
)

st.sidebar.divider()

run_simulation = st.sidebar.button(
    "▶ Run Simulation",
    use_container_width=True
)


# ------------------------------------------------
# SIMULATION
# ------------------------------------------------

if run_simulation:

    time, omega, torque = simulate_braking(
        initial_angular_velocity=initial_velocity,
        braking_coefficient=braking_coefficient,
        moment_of_inertia=moment_of_inertia,
        simulation_time=simulation_time
    )

    # Rotational kinetic energy
    kinetic_energy = 0.5 * moment_of_inertia * omega**2

    # Angular displacement
    angular_displacement = np.trapezoid(omega, time)

    st.success("Simulation completed successfully!")

    # ------------------------------------------------
    # RESULTS
    # ------------------------------------------------

    st.header("Simulation Results")

    col1, col2, col3 = st.columns(3)

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

    st.divider()

    # ------------------------------------------------
    # ANGULAR VELOCITY GRAPH
    # ------------------------------------------------

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

    st.plotly_chart(fig_velocity, use_container_width=True)

    # ------------------------------------------------
    # BRAKING TORQUE GRAPH
    # ------------------------------------------------

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

    st.plotly_chart(fig_torque, use_container_width=True)

    # ------------------------------------------------
    # KINETIC ENERGY GRAPH
    # ------------------------------------------------

    st.subheader("3. Rotational Kinetic Energy vs Time")

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

    st.plotly_chart(fig_energy, use_container_width=True)

    # ------------------------------------------------
    # ADDITIONAL RESULTS
    # ------------------------------------------------

    st.divider()

    st.subheader("Additional Simulation Data")

    result_col1, result_col2 = st.columns(2)

    result_col1.metric(
        "Final Kinetic Energy",
        f"{kinetic_energy[-1]:.6f} J"
    )

    result_col2.metric(
        "Angular Displacement",
        f"{angular_displacement:.3f} rad"
    )

    # ------------------------------------------------
    # OBSERVATION TABLE
    # ------------------------------------------------

    st.subheader("Virtual Experiment Observation Table")

    import pandas as pd

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
        "Download Experimental Data (CSV)",
        observations.to_csv(index=False),
        file_name="eddylab_observations.csv",
        mime="text/csv"
    )

else:

    st.info("Adjust the experimental parameters and click Run Simulation.")

    st.subheader("How the Simulation Works")

    st.markdown("""
    1. Set the initial angular velocity of the disc.
    2. Adjust the effective braking coefficient.
    3. Set the moment of inertia.
    4. Select the simulation duration.
    5. Run the simulation and examine the resulting graphs.

    **Mathematical model:**

    The initial simulation assumes a braking torque
    proportional to angular velocity:

    """)

    st.latex(r"\tau_b = k\omega")

    st.latex(r"I\frac{d\omega}{dt}=-k\omega")

    st.latex(r"\omega(t)=\omega_0 e^{-kt/I}")

    st.caption(
        "Note: This is an idealized linear braking model. "
        "The coefficient k is an effective model parameter, "
        "not a directly measured magnetic-field property."
    )


# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.divider()

st.caption(
    "EDDYLAB | Interactive Virtual Physics Laboratory | "
    "Educational Simulation Prototype"
)
