import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --------------------------------------------------
# STREAMLIT CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="QualSteam Dashboard",
    layout="wide"
)

# --------------------------------------------------
# DATA FILES
# --------------------------------------------------
DATA_FOLDER = "data"

csv_files = sorted(
    [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("Trial Date Selection")
selected_file = st.sidebar.selectbox(
    "Select Trial Data",
    csv_files
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv(os.path.join(DATA_FOLDER, selected_file))
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.sort_values("Timestamp")

min_date = df["Timestamp"].min().strftime("%Y-%m-%d %H:%M")
max_date = df["Timestamp"].max().strftime("%Y-%m-%d %H:%M")

# --------------------------------------------------
# MAIN TITLE (WHITE TEXT FOR STREAMLIT DARK BG)
# --------------------------------------------------
st.markdown(
    f"""
    <h2 style="text-align:center; color:white;">
        Zydus LifeSciences, Ahmedabad. ({min_date} to {max_date})<br>
        <span style="font-size:16px;">Customer Trial Data</span>
    </h2>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# CREATE FIGURE
# --------------------------------------------------
fig = make_subplots(
    rows=4,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.25, 0.25, 0.25, 0.25]
)

# =========================
# ROW 1: TEMPERATURE
# =========================
fig.add_trace(
    go.Scatter(
        x=df["Timestamp"],
        y=df["Process Temp SP"],
        name="Process Temp SP",
        line=dict(color="black", dash="dot", width=2)
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=df["Timestamp"],
        y=df["Process Temp"],
        name="Process Temp",
        line=dict(color="#D32F2F", width=2)
    ),
    row=1, col=1
)

fig.update_yaxes(
    title_text="Temp (°C)",
    title_font=dict(color="black"),
    tickfont=dict(color="black"),
    row=1, col=1
)

# =========================
# ROW 2: PRESSURE
# =========================
fig.add_trace(
    go.Scatter(
        x=df["Timestamp"],
        y=df["Pressure SP"],
        name="Pressure SP",
        line=dict(color="#1A237E", dash="dot", width=2)
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=df["Timestamp"],
        y=df["Inlet Steam Pressure"],
        name="Inlet P1",
        line=dict(color="#004D40", width=2)
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=df["Timestamp"],
        y=df["Outlet Steam Pressure"],
        name="Outlet P2",
        line=dict(color="#00008B", width=2),
        fill="tozeroy",
        fillcolor="rgba(0, 0, 139, 0.1)"
    ),
    row=2, col=1
)

fig.update_yaxes(
    title_text="Bar",
    title_font=dict(color="black"),
    tickfont=dict(color="black"),
    row=2, col=1
)

# =========================
# ROW 3: FLOW RATE
# =========================
fig.add_trace(
    go.Scatter(
        x=df["Timestamp"],
        y=df["Steam Flow Rate"],
        name="Flow Rate",
        line=dict(color="#7B1FA2", width=2),
        fill="tozeroy",
        fillcolor="rgba(123, 31, 162, 0.1)"
    ),
    row=3, col=1
)

fig.update_yaxes(
    title_text="kg/hr",
    title_font=dict(color="black"),
    tickfont=dict(color="black"),
    row=3, col=1
)

# =========================
# ROW 4: VALVE OPENING
# =========================
fig.add_trace(
    go.Scatter(
        x=df["Timestamp"],
        y=df["QualSteam Valve Opening"],
        name="Valve %",
        line=dict(color="#B8860B", width=2),
        fill="tozeroy",
        fillcolor="rgba(184, 134, 11, 0.1)"
    ),
    row=4, col=1
)

fig.update_yaxes(
    title_text="%",
    range=[0, 105],
    title_font=dict(color="black"),
    tickfont=dict(color="black"),
    row=4, col=1
)

fig.update_xaxes(
    title_text="Timestamp",
    title_font=dict(color="black"),
    tickfont=dict(color="black")
)

# --------------------------------------------------
# GLOBAL LAYOUT (FORCE VISIBILITY)
# --------------------------------------------------
fig.update_layout(
    height=900,
    hovermode="x unified",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="black"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color="black")
    )
)

fig.update_xaxes(showgrid=True, gridcolor="#f0f0f0")
fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0")

# --------------------------------------------------
# RENDER
# --------------------------------------------------
st.plotly_chart(fig, use_container_width=True)

