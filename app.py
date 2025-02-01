import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- Title of the Dashboard ---
st.title("Dam Water Velocity Dashboard")

# --- User Inputs ---
st.sidebar.header("Input Parameters")

initial_level = st.sidebar.number_input("Initial Water Level (m)", min_value=0.0, step=0.1)
final_level = st.sidebar.number_input("Final Water Level (m)", min_value=0.0, step=0.1)
location = st.sidebar.text_input("Location of Dam", placeholder="Enter location")

# --- Water Flow Rate Simulation ---
rate_of_flow = random.uniform(10, 100)  # Simulating RoF (can be replaced with real data)
st.metric(label="Rate of Flow (cubic meters/sec)", value=f"{rate_of_flow:.2f}")

# --- Gauge Representation ---
st.progress(int(rate_of_flow))  # Simulated Gauge

# --- Historic RoF Trends ---
st.subheader("Historical Rate of Flow Trends")

# Generating random data for past 10 days
dates = pd.date_range(end=pd.Timestamp.today(), periods=10).strftime("%Y-%m-%d")
historical_rof = [random.uniform(10, 100) for _ in range(10)]
df = pd.DataFrame({"Date": dates, "Rate of Flow": historical_rof})

fig = px.bar(df, x="Date", y="Rate of Flow", title="Rate of Flow Over Time")
st.plotly_chart(fig)

# --- User Input for Custom Date ---
selected_date = st.date_input("Select a date to view RoF data")
if str(selected_date) in df["Date"].values:
    selected_rof = df[df["Date"] == str(selected_date)]["Rate of Flow"].values[0]
    st.write(f"Rate of Flow on {selected_date}: {selected_rof:.2f} cubic meters/sec")
else:
    st.write("No data available for the selected date.")

# --- Notification for Water Levels ---
st.sidebar.subheader("Notification Settings")
enable_notifications = st.sidebar.checkbox("Enable Water Level Notifications")

if enable_notifications:
    threshold = st.sidebar.number_input("Set Water Level Threshold (m)", min_value=0.0, step=0.1)
    if final_level > threshold:
        st.warning(f"⚠️ Alert: Water level has exceeded the threshold of {threshold}m!")
