# procedures_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Procedures Dashboard", layout="wide")

# ---------------- SIDEBAR NAVIGATION ----------------
with st.sidebar:
    st.markdown("## Navigation")
    st.page_link("app.py", label="📊 Strategic & Quick Dashboard")
    st.page_link("pages/data_generation.py", label="⚙️ Data Generation")
    st.page_link("pages/conditions_dashboard.py", label="🩺 Conditions Dashboard")
    st.page_link("pages/procedures_dashboard.py", label="📋 Procedures Dashboard")

# -------------------- PLACEHOLDER DATA --------------------
# (Later you’ll replace this with API call)
np.random.seed(42)
dates = pd.date_range("2015-01-01", periods=200, freq="W")
sample_data = {
    "performed_from": np.random.choice(dates, 200),
    "performed_till": np.random.choice(dates, 200),
    "procedure_description": np.random.choice([
        "Medication reconciliation", "Patient referral", "Depression screening",
        "Assessment of substance use", "Dental consultation", "Removal of subgingival calculus",
        "Examination of gingiva"
    ], 200),
    "procedure_cost": np.random.uniform(100, 1000, 200),
    "procedure_type": np.random.choice(["procedure", "therapy", "screening"], 200),
}

df = pd.DataFrame(sample_data)
df["performed_from"] = pd.to_datetime(df["performed_from"])
df["month_year"] = df["performed_from"].dt.to_period("M").astype(str)

# -------------------- HEADER --------------------
st.title("🩺 Procedures Dashboard")
st.markdown("### Insights into performed medical procedures, costs, and trends")

# -------------------- 1️⃣ TOP PROCEDURES BAR CHART --------------------
st.subheader("1️⃣ Most Frequently Performed Procedures")

top_procedures = (
    df["procedure_description"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "procedure_description", "procedure_description": "count"})
)
top_procedures.columns = ["Procedure", "Count"]  # ✅ Fix column names

fig1 = px.bar(
    top_procedures.head(10),
    x="Procedure",
    y="Count",
    color="Count",
    text="Count",
    title="Top 10 Procedures by Frequency",
)
fig1.update_traces(textposition="outside")
fig1.update_layout(template="plotly_dark", xaxis_title="", yaxis_title="Count")
st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

# -------------------- 2️⃣ COST DISTRIBUTION PIE CHART --------------------
st.subheader("2️⃣ Average Cost Distribution by Procedure Type")

avg_cost = df.groupby("procedure_type")["procedure_cost"].mean().reset_index()

fig2 = px.pie(
    avg_cost,
    names="procedure_type",
    values="procedure_cost",
    title="Average Cost by Procedure Type",
    hole=0.4,
)
fig2.update_traces(textinfo="percent+label")
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# -------------------- 3️⃣ COST TREND OVER TIME --------------------
st.subheader("3️⃣ Procedure Cost Trend Over Time")

trend = (
    df.groupby("month_year")["procedure_cost"]
    .mean()
    .reset_index()
    .sort_values("month_year")
)

fig3 = px.line(
    trend,
    x="month_year",
    y="procedure_cost",
    title="Average Procedure Cost Over Time",
    markers=True,
)
fig3.update_layout(
    template="plotly_dark",
    xaxis_title="Month-Year",
    yaxis_title="Average Cost",
)
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# -------------------- 4️⃣ DURATION VS COST CORRELATION --------------------
st.subheader("4️⃣ Procedure Duration vs Cost Analysis")

df["duration_minutes"] = (
    (pd.to_datetime(df["performed_till"]) - pd.to_datetime(df["performed_from"]))
    .dt.total_seconds()
    / 60
)
df = df[df["duration_minutes"] > 0]  # remove invalids

fig4 = px.scatter(
    df,
    x="duration_minutes",
    y="procedure_cost",
    color="procedure_type",
    trendline="ols",
    title="Duration vs Cost (Correlation Analysis)",
)
fig4.update_layout(
    template="plotly_dark",
    xaxis_title="Duration (minutes)",
    yaxis_title="Procedure Cost",
)
st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
