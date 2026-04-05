# ⚡ Transformer Failure Predictor

A real-time transformer failure prediction and monitoring dashboard built with Streamlit and a 3-State Markov Chain model.

## Features
- 🤖 Train a 3-State Markov Chain model on synthetic transformer data
- 📡 Live simulation of transformer signals (voltage, current, oil density, temperature)
- 📊 Real-time charts for signal trends and state predictions
- 🔍 Automatic failure diagnostics with root cause analysis
- 📢 Natural language status reports for each timestep

## States
| State | Meaning |
|-------|---------|
| 0 | Healthy |
| 1 | Warning |
| 2 | Failure |

## Installation
pip install streamlit pandas numpy plotly joblib

## Usage
streamlit run transgui3.py

1. Click Train Markov Chain to train the model
2. Click Start Live Simulation to begin monitoring
3. Click Stop Simulation to pause

## Tech Stack
- Python, Streamlit, Plotly, NumPy, Pandas, Joblib