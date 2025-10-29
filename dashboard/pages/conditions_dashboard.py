import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="Conditions Dashboard",
    layout="wide",
    page_icon="🩺"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0b0c10 0%, #101820 100%);
    color: #e0e0e0;
}
section[data-testid="stSidebar"] {
    background-color: #121212 !important;
    border-right: 1px solid #1f1f1f !important;
    padding-top: 1.2rem;
}
section[data-testid="stSidebar"]::before {
    content: "🩺 Conditions Dashboard";
    display: block;
    font-size: 1.3em;
    font-weight: 700;
    color: #4DB6AC;
    text-align: center;
    margin-bottom: 1rem;
}
h2, h3 {
    color: #4DB6AC;
}
[data-testid="stMetric"] {
    background-color: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 15px;
}
footer {
    text-align: center;
    color: #777;
    padding-top: 1rem;
    font-size: 0.9em;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## Navigation")
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/data_generation.py", label="⚙️ Data Generation")
    st.page_link("pages/conditions_dashboard.py", label="🩺 Conditions Dashboard")

# ---------------- MAIN HEADER ----------------
st.markdown("<h1 style='color:#4DB6AC;'>Conditions Overview</h1>", unsafe_allow_html=True)
st.markdown("Gain insights into common, chronic, and acute conditions across patients — powered by synthetic health data.")
st.markdown("---")

# ---------------- PLACEHOLDER DATA ----------------
np.random.seed(42)
conditions = ["Gingivitis", "Chronic Pain", "Stress", "Laceration", "Viral Sinusitis",
              "Fibromyalgia", "Infection of tooth", "Primary Dental Caries", "Medication Review", "Chronic Low Back Pain"]
event_types = ["disorder", "finding", "situation"]

data = []
for i in range(500):
    start = datetime(2015, 1, 1) + timedelta(days=np.random.randint(0, 3000))
    end = start + timedelta(days=np.random.randint(5, 300)) if np.random.rand() > 0.3 else None
    data.append({
        "event_start": start,
        "event_end": end,
        "event_description": np.random.choice(conditions),
        "event_type": np.random.choice(event_types),
    })
df = pd.DataFrame(data)
df["year"] = df["event_start"].dt.year
df["duration_days"] = (df["event_end"] - df["event_start"]).dt.days.fillna(0)

# ---------------- 1️⃣ Top 10 Most Common Conditions ----------------
st.subheader("1️⃣ Top 10 Most Common Conditions")
cond_counts = df["event_description"].value_counts().reset_index()
cond_counts.columns = ["Condition", "Count"]
fig1 = px.bar(
    cond_counts.head(10),
    x="Count",
    y="Condition",
    orientation="h",
    title="Most Frequent Conditions",
)
fig1.update_layout(
    template="plotly_dark",
    height=350,
    margin=dict(l=20, r=20, t=50, b=20),
    showlegend=False,
    plot_bgcolor="#0f0f0f",
    paper_bgcolor="#0f0f0f",
)
st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

# ---------------- 2️⃣ Condition Trends Over Time ----------------
st.subheader("2️⃣ Condition Trends Over Time")
top_conditions = cond_counts["Condition"].head(5).tolist()
selected = st.multiselect(
    "Select conditions to analyze trends:", options=conditions, default=top_conditions
)
trend_df = (
    df[df["event_description"].isin(selected)]
    .groupby(["year", "event_description"])
    .size()
    .reset_index(name="Count")
)
fig2 = px.line(
    trend_df,
    x="year",
    y="Count",
    color="event_description",
    markers=True,
    title="Yearly Condition Trends",
)
fig2.update_layout(
    template="plotly_dark",
    height=350,
    margin=dict(l=20, r=20, t=50, b=20),
    plot_bgcolor="#0f0f0f",
    paper_bgcolor="#0f0f0f",
)
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ---------------- 3️⃣ Average Condition Duration ----------------
st.subheader("3️⃣ Average Condition Duration by Type")
fig3 = px.violin(
    df,
    x="event_type",
    y="duration_days",
    box=True,
    points="all",
    color="event_type",
    title="Duration Distribution by Condition Type (days)",
)
fig3.update_layout(
    template="plotly_dark",
    height=350,
    margin=dict(l=20, r=20, t=50, b=20),
    plot_bgcolor="#0f0f0f",
    paper_bgcolor="#0f0f0f",
    showlegend=False,
)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# ---------------- 4️⃣ Condition Type Distribution ----------------
st.subheader("4️⃣ Condition Type Distribution")
type_counts = df["event_type"].value_counts().reset_index()
type_counts.columns = ["Type", "Count"]
fig4 = px.pie(
    type_counts,
    values="Count",
    names="Type",
    hole=0.4,
    title="Proportion of Condition Types",
)
fig4.update_layout(
    template="plotly_dark",
    height=350,
    margin=dict(l=20, r=20, t=50, b=20),
    plot_bgcolor="#0f0f0f",
    paper_bgcolor="#0f0f0f",
)
st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

st.markdown("<footer>© 2025 Synthea-Based Hospital Dashboard | Condition Analytics Module</footer>", unsafe_allow_html=True)
