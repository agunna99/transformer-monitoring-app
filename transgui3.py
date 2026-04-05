import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import time
from joblib import dump, load
import plotly.graph_objects as go

# --- CONFIG ---
ARTIFACTS_DIR = "artifacts"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
np.random.seed(42)

st.set_page_config(page_title="Transformer Failure Predictor", page_icon="⚡", layout="wide")
st.title("⚡ Transformer Failure Predictor with Live Monitoring + Failure Diagnostics (3-State Markov Chain)")

# =====================================================
# 🚀 TRAINING PANEL (3-State Markov Chain)
# =====================================================
st.header("🤖 Train the Markov Chain Model")

n_samples = 2000
timestamps = pd.date_range("2024-01-01", periods=n_samples, freq="h")

# Generate synthetic dataset with 3 states
df = pd.DataFrame({
    "timestamp": timestamps,
    "voltage": np.random.normal(11000, 300, n_samples),
    "current": np.random.normal(200, 50, n_samples),
    "oil_density": np.random.normal(890, 5, n_samples),
    "ambient_temperature": np.random.normal(30, 7, n_samples),
    "failure_label": np.random.choice([0, 1, 2], size=n_samples, p=[0.8, 0.15, 0.05])
})

if st.button("🚀 Train Markov Chain"):
    states = df["failure_label"].values
    n_states = 3
    trans_matrix = np.zeros((n_states, n_states))

    for i in range(len(states) - 1):
        trans_matrix[states[i], states[i + 1]] += 1

    # Normalize rows to probabilities
    trans_matrix = trans_matrix / trans_matrix.sum(axis=1, keepdims=True)

    st.success("✅ 3-State Markov Chain trained successfully!")
    st.write("Transition Probability Matrix:")
    st.write(pd.DataFrame(
        trans_matrix,
        index=["Healthy (0)", "Warning (1)", "Failure (2)"],
        columns=["Next Healthy (0)", "Next Warning (1)", "Next Failure (2)"]
    ))

    # Save model
    dump(trans_matrix, os.path.join(ARTIFACTS_DIR, "markov_model.joblib"))
    with open(os.path.join(ARTIFACTS_DIR, "markov_matrix.json"), "w") as f:
        json.dump(trans_matrix.tolist(), f, indent=2)
    st.info(f"Artifacts saved under `{ARTIFACTS_DIR}` ✅")

# =====================================================
# 📡 LIVE SIGNAL SIMULATOR WITH PREDICTIONS
# =====================================================
st.header("📡 Live Transformer Signals & Predictions (3-State Markov Chain)")

# Load Markov Chain if available
model_path = os.path.join(ARTIFACTS_DIR, "markov_model.joblib")
trans_matrix = load(model_path) if os.path.exists(model_path) else None

# Session state for live data
if "live_df" not in st.session_state:
    st.session_state.live_df = pd.DataFrame(columns=[
        "timestamp", "voltage", "current", "oil_density",
        "ambient_temperature", "failure_label", "pred_state", "pred_failure_proba"
    ])
if "running" not in st.session_state:
    st.session_state.running = False
if "current_state" not in st.session_state:
    st.session_state.current_state = 0  # start Healthy

col1, col2 = st.columns(2)
if col1.button("▶️ Start Live Simulation"):
    st.session_state.running = True
if col2.button("⏹ Stop Simulation"):
    st.session_state.running = False

signal_placeholder = st.empty()
failure_placeholder = st.empty()
prediction_placeholder = st.empty()
reasoning_placeholder = st.empty()
summary_placeholder = st.empty()  # natural language summary

# Color map for states
state_colors = {0: "green", 1: "yellow", 2: "red"}

# =====================================================
# 🔄 SIMULATION LOOP
# =====================================================
if st.session_state.running:
    for i in range(200):  # simulate 200 timesteps
        new_row = {
            "timestamp": pd.Timestamp.now(),
            "voltage": np.random.normal(11000, 300),
            "current": np.random.normal(200, 50),
            "oil_density": np.random.normal(890, 5),
            "ambient_temperature": np.random.normal(30, 7),
            "failure_label": np.random.choice([0, 1, 2], p=[0.85, 0.1, 0.05])
        }

        # Predict next state with Markov Chain
        if trans_matrix is not None:
            st.session_state.current_state = np.random.choice(
                [0, 1, 2],
                p=trans_matrix[st.session_state.current_state]
            )
            predicted_state = st.session_state.current_state
            failure_proba = trans_matrix[predicted_state, 2]
        else:
            predicted_state = np.nan
            failure_proba = np.nan

        new_row["pred_state"] = predicted_state
        new_row["pred_failure_proba"] = failure_proba
        st.session_state.live_df = pd.concat(
            [st.session_state.live_df, pd.DataFrame([new_row])],
            ignore_index=True
        )
        if len(st.session_state.live_df) > 200:
            st.session_state.live_df = st.session_state.live_df.iloc[-200:]

        # --- Plot signals ---
        fig = go.Figure()
        colors = {"voltage": "red", "current": "blue", "oil_density": "green", "ambient_temperature": "orange"}
        for col in ["voltage", "current", "oil_density", "ambient_temperature"]:
            fig.add_trace(go.Scatter(
                x=st.session_state.live_df["timestamp"],
                y=st.session_state.live_df[col],
                mode="lines",
                name=col,
                line=dict(color=colors[col], width=2)
            ))
        fig.update_layout(title="Live Transformer Signals", template="plotly_dark", height=400)
        signal_placeholder.plotly_chart(fig, use_container_width=True)

        # --- Plot actual states ---
        failure_fig = go.Figure()
        for state_val, color in state_colors.items():
            subset = st.session_state.live_df[st.session_state.live_df["failure_label"] == state_val]
            failure_fig.add_trace(go.Scatter(
                x=subset["timestamp"],
                y=subset["failure_label"],
                mode="markers+lines",
                name=f"State {state_val}",
                marker=dict(color=color, size=8),
                line=dict(color=color, width=2)
            ))
        failure_fig.update_layout(
            title="Live Transformer States (0=Healthy 🟢, 1=Warning 🟡, 2=Failure 🔴)",
            template="plotly_dark",
            height=250,
            yaxis=dict(range=[-0.2, 2.2])
        )
        failure_placeholder.plotly_chart(failure_fig, use_container_width=True)

        # --- Plot Markov predictions ---
        if trans_matrix is not None:
            pred_fig = go.Figure()
            for state_val, color in state_colors.items():
                subset = st.session_state.live_df[st.session_state.live_df["pred_state"] == state_val]
                pred_fig.add_trace(go.Scatter(
                    x=subset["timestamp"],
                    y=subset["pred_state"],
                    mode="markers+lines",
                    name=f"Predicted {state_val}",
                    marker=dict(color=color, size=8),
                    line=dict(color=color, width=2)
                ))
            pred_fig.add_trace(go.Scatter(
                x=st.session_state.live_df["timestamp"],
                y=st.session_state.live_df["pred_failure_proba"],
                mode="lines",
                name="Failure Probability",
                line=dict(color="yellow", width=2, dash="dot")
            ))
            pred_fig.update_layout(
                title="Live Markov Predictions (Colored States + Failure Probability)",
                template="plotly_dark",
                height=250,
                yaxis=dict(range=[-0.2, 2.2])
            )
            prediction_placeholder.plotly_chart(pred_fig, use_container_width=True)

            # --- Natural Language Summary with Trends ---
            latest = st.session_state.live_df.iloc[-1]
            volt, curr, oil, temp = (
                latest["voltage"],
                latest["current"],
                latest["oil_density"],
                latest["ambient_temperature"]
            )

            if len(st.session_state.live_df) > 1:
                prev = st.session_state.live_df.iloc[-2]

                def trend(curr_val, prev_val, name, tol=0.05):
                    if abs(curr_val - prev_val) < tol * abs(prev_val):
                        return f"{name} is stable ({curr_val:.1f})"
                    elif curr_val > prev_val:
                        return f"{name} is rising ({curr_val:.1f} ↑ from {prev_val:.1f})"
                    else:
                        return f"{name} is falling ({curr_val:.1f} ↓ from {prev_val:.1f})"

                volt_trend = trend(volt, prev["voltage"], "Voltage")
                curr_trend = trend(curr, prev["current"], "Current")
                oil_trend = trend(oil, prev["oil_density"], "Oil density")
                temp_trend = trend(temp, prev["ambient_temperature"], "Temperature")
            else:
                volt_trend = f"Voltage: {volt:.1f}"
                curr_trend = f"Current: {curr:.1f}"
                oil_trend = f"Oil density: {oil:.1f}"
                temp_trend = f"Temperature: {temp:.1f}"

            if predicted_state == 0:
                summary_text = (
                    "🟢 The transformer is currently in a **Healthy** state. "
                    f"{volt_trend}, {curr_trend}, {oil_trend}, {temp_trend}. "
                    "All signals are within safe operating ranges. No immediate action is required."
                )
            elif predicted_state == 1:
                summary_text = (
                    "🟡 The transformer is in a **Warning** state. "
                    f"{volt_trend}, {curr_trend}, {oil_trend}, {temp_trend}. "
                    "Some signals show early instability — preventive maintenance is recommended."
                )
            elif predicted_state == 2:
                summary_text = (
                    "🔴 The transformer is in a **Failure** state. "
                    f"{volt_trend}, {curr_trend}, {oil_trend}, {temp_trend}. "
                    "Critical conditions detected — immediate inspection and shutdown are required."
                )
            else:
                summary_text = (
                    "⚠️ Transformer state unknown. "
                    "Please train the Markov Chain model before starting the simulation."
                )

            summary_placeholder.markdown(f"### 📢 Current Status Report\n\n{summary_text}")

            # --- Failure Diagnostic Panel ---
            pred_state = latest["pred_state"]
            prob = latest["pred_failure_proba"]

            if pred_state == 2 or prob > 0.6 or temp > 90 or oil > 900 or curr > 300:
                reasoning_placeholder.subheader("🔍 Failure Diagnostic Panel")

                causes = []
                if pred_state == 2:
                    causes.append("❌ Transformer is in FAILURE state.")
                elif pred_state == 1:
                    causes.append("⚠️ Transformer is in WARNING state — unstable condition detected.")
                if prob > 0.6:
                    causes.append("⚠️ High probability of transitioning into Failure soon.")
                if temp > 90:
                    causes.append("🔥 Overheating detected: ambient temperature above safe limits.")
                if oil > 900:
                    causes.append("🛢 Oil density is abnormally high → possible insulation breakdown.")
                if curr > 300:
                    causes.append("⚡ Current spike detected → potential overload or short circuit.")

                reasoning_placeholder.write("**Possible Causes of Risk/Failure:**")
                for c in causes:
                    reasoning_placeholder.markdown(f"- {c}")

                if pred_state == 2 or prob > 0.6 or temp > 90 or oil > 900 or curr > 300:
                    recommendation = "🚨 Immediate inspection required. Reduce load and check cooling/insulation."
                elif pred_state == 1:
                    recommendation = "⚠️ Monitor closely. Schedule preventive maintenance soon."
                else:
                    recommendation = "✅ Continue normal operation."

                reasoning_placeholder.markdown(f"**Recommended Action:** {recommendation}")
            else:
                reasoning_placeholder.empty()
        else:
            prediction_placeholder.info("⚠️ Train the Markov Chain first to see live predictions.")

        time.sleep(1)  # update every second
