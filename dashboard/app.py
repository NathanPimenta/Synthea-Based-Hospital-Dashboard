import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import requests

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="Main Dashboard",
    layout="wide",
    page_icon="🏥"
)

API_URL = "http://localhost:3001/quick_dashboard"

# ---------------- FETCH DATA FROM API ----------------
@st.cache_data(ttl=600)
def load_data():
    """Fetch Spark patient data via Flask API."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            json_data = response.json()
            if json_data.get("api-status") == "successs":
                data = json_data.get("data", [])
                if data:
                    df = pd.DataFrame(data)

                    # ✅ Fix negative or invalid family income values
                    if "family_income" in df.columns:
                        df["family_income"] = pd.to_numeric(df["family_income"], errors="coerce").abs().fillna(0)

                    return df
        st.warning("⚠️ No data returned from API or data format invalid.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error fetching data from API: {e}")
        return pd.DataFrame()

df = load_data()

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
    content: "🏥  Synthea Dashboard";
    display: block;
    font-size: 1.3em;
    font-weight: 700;
    color: #4DB6AC;
    text-align: center;
    margin-bottom: 1rem;
}
a[class^="st-emotion-cache"] {
    color: #E0E0E0 !important;
    font-size: 1.05em !important;
    padding: 0.5rem 1rem !important;
    border-radius: 8px !important;
    transition: all 0.25s ease !important;
}
a[class^="st-emotion-cache"]:hover {
    background-color: #1b1f22 !important;
    color: #4DB6AC !important;
    transform: translateX(3px);
}
.main-title {
    font-size: 2.8em;
    color: #4DB6AC;
    font-weight: 700;
    margin-bottom: 0.2em;
}
.main-subtitle {
    color: #BDBDBD;
    font-size: 1.05em;
    margin-bottom: 1em;
}
[data-testid="stMetric"] {
    background-color: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 15px;
    transition: 0.3s ease-in-out;
}
[data-testid="stMetric"]:hover {
    border-color: #4DB6AC;
    transform: scale(1.02);
}
[data-testid="stMetricValue"] {
    font-size: 2em;
    color: #BBDEFB;
}
[data-testid="stMetricLabel"] {
    font-size: 0.9em;
    color: #AAAAAA;
}
h3 {
    color: #BBDEFB;
    border-bottom: 1px solid #333;
    padding-bottom: 5px;
}
footer {
    text-align: center;
    color: #777;
    padding-top: 1rem;
    font-size: 0.9em;
}
@media (max-width: 768px) {
    .main-title { text-align: center; font-size: 2.2em; }
    .main-subtitle { text-align: center; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR NAVIGATION ----------------
with st.sidebar:
    st.markdown("## Navigation")
    st.page_link("app.py", label="📊 Strategic & Quick Dashboard")
    st.page_link("pages/data_generation.py", label="⚙️ Data Generation")
    st.page_link("pages/patient_demographics.py", label="👥 Patient Demographics")
    st.page_link("pages/conditions_dashboard.py", label="🩺 Conditions Dashboard")
    st.page_link("pages/procedures_dashboard.py", label="⚕️ Procedures Dashboard")

# ---------------- MAIN CONTENT ----------------
st.markdown("<p class='main-title'>Strategic & Quick Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Real-time analytics for patient engagement and hospital performance.</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- KPI SECTION ----------------
if not df.empty:
    total_patients = len(df)
    avg_income = df["family_income"].mean() if "family_income" in df.columns else 0
    unique_cities = df["city"].nunique() if "city" in df.columns else 0
    unique_genders = df["gender"].nunique() if "gender" in df.columns else 0
else:
    total_patients = avg_income = unique_cities = unique_genders = 0

st.markdown("### 📈 Core Performance Indicators")
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric(label="Total Patients", value=f"{total_patients:,}")
with k2:
    st.metric(label="Average Family Income", value=f"${avg_income:,.2f}")
with k3:
    st.metric(label="Unique Cities", value=f"{unique_cities}")
with k4:
    st.metric(label="Unique Genders", value=f"{unique_genders}")

# ---------------- DEMOGRAPHIC OVERVIEW ----------------
st.markdown("### 📊 Demographic Insights")
c1, c2 = st.columns(2)

# --- Gender Distribution ---
if not df.empty and "gender" in df.columns:
    gender_counts = df["gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    fig_g = px.pie(
        gender_counts,
        names="Gender",
        values="Count",
        title="Gender Distribution",
        color_discrete_sequence=px.colors.sequential.Tealgrn
    )
    fig_g.update_traces(textinfo='percent+label')
    fig_g.update_layout(template="plotly_dark", height=320, title_x=0.5)
    with c1:
        st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})
else:
    st.warning("⚠️ Gender data not available.")

# --- Top Cities ---
if not df.empty and "city" in df.columns:
    city_counts = df["city"].value_counts().nlargest(10).reset_index()
    city_counts.columns = ["City", "Patients"]
    fig_c = px.bar(
        city_counts,
        x="City",
        y="Patients",
        title="Top 10 Cities by Patient Count",
        color="City",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_c.update_layout(template="plotly_dark", height=320, title_x=0.5)
    with c2:
        st.plotly_chart(fig_c, use_container_width=True, config={"displayModeBar": False})

# --- Ethnicity / Ancestry ---
if not df.empty and "ancestry" in df.columns:
    ancestry_counts = df["ancestry"].value_counts().nlargest(10).reset_index()
    ancestry_counts.columns = ["Ancestry", "Count"]
    fig_eth = px.bar(
        ancestry_counts,
        x="Ancestry",
        y="Count",
        title="Ancestry Distribution",
        color="Ancestry",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_eth.update_layout(template="plotly_dark", height=320, title_x=0.5)
    st.plotly_chart(fig_eth, use_container_width=True, config={"displayModeBar": False})

# ---------------- NEW DECISIVE GRAPHS ----------------
st.markdown("### 📉 Advanced Insights")

if not df.empty:
    a1, a2 = st.columns(2)

    # --- Family Income Distribution ---
    with a1:
        if "family_income" in df.columns:
            fig_income = px.histogram(
                df,
                x="family_income",
                nbins=30,
                title="Family Income Distribution",
                color_discrete_sequence=["#4DB6AC"]
            )
            fig_income.update_layout(template="plotly_dark", height=320, title_x=0.5)
            st.plotly_chart(fig_income, use_container_width=True, config={"displayModeBar": False})

    # --- Age vs Income Correlation ---
    with a2:
        if "age" in df.columns and "family_income" in df.columns:
            fig_age_income = px.scatter(
                df,
                x="age",
                y="family_income",
                title="Age vs Family Income Correlation",
                color="gender" if "gender" in df.columns else None,
                color_discrete_sequence=px.colors.qualitative.Safe,
                opacity=0.7
            )
            fig_age_income.update_layout(template="plotly_dark", height=320, title_x=0.5)
            st.plotly_chart(fig_age_income, use_container_width=True, config={"displayModeBar": False})

    b1, b2 = st.columns(2)

    # --- Gender-wise Average Income ---
    with b1:
        if "gender" in df.columns and "family_income" in df.columns:
            avg_by_gender = df.groupby("gender")["family_income"].mean().reset_index()
            fig_gi = px.bar(
                avg_by_gender,
                x="gender",
                y="family_income",
                title="Average Family Income by Gender",
                color="gender",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_gi.update_layout(template="plotly_dark", height=320, title_x=0.5)
            st.plotly_chart(fig_gi, use_container_width=True, config={"displayModeBar": False})

    # --- City-wise Average Income (Treemap) ---
    with b2:
        if "city" in df.columns and "family_income" in df.columns:
            city_avg = df.groupby("city")["family_income"].mean().nlargest(20).reset_index()
            fig_t = px.treemap(
                city_avg,
                path=["city"],
                values="family_income",
                title="City-wise Average Income (Top 20)",
                color="family_income",
                color_continuous_scale="Tealgrn"
            )
            fig_t.update_layout(template="plotly_dark", height=320, title_x=0.5)
            st.plotly_chart(fig_t, use_container_width=True, config={"displayModeBar": False})

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("💡 Use the sidebar to navigate between analytical modules.")
st.markdown(
    "<footer>© 2025 Synthea-Based Hospital Dashboard | Designed for Performance & Clarity</footer>",
    unsafe_allow_html=True
)