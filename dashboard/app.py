import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="🏥 Main Dashboard",
    layout="wide",
    page_icon="🏥"
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

# ---------------- MAIN CONTENT ----------------
st.markdown("<p class='main-title'>Strategic & Quick Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Real-time analytics for patient engagement and hospital performance.</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- KPIs ----------------
st.markdown("### 📈 Core Performance Indicators")
k1, k2, k3, k4 = st.columns(4)
with k1: st.metric(label="Encounters This Week", value="2,145", delta="▲ 12%")
with k2: st.metric(label="Avg. Procedure Cost", value="$455.50", delta="▼ 1.5%", delta_color="inverse")
with k3: st.metric(label="Active Patients (30 days)", value="12,500", delta="▲ 2%")
with k4: 
    st.metric(label="Top Condition", value="Allergy", delta="▲ 1.5%")

# ---------------- CHARTS: UTILIZATION ----------------
st.markdown("### 📊 Utilization & Demographic Overview")
c1, c2 = st.columns(2)

# --- Patient Volume Trend ---
with c1:
    df = pd.DataFrame({
        "Week": ["W1", "W2", "W3", "W4", "W5"],
        "Encounters": [1450, 1600, 1750, 1950, 2145]
    })
    fig = px.line(df, x="Week", y="Encounters", title="Weekly Patient Volume Trend", markers=True)
    fig.update_traces(line=dict(color="#4DB6AC", width=3), marker=dict(size=8, color="#81D4FA"))
    fig.update_layout(
        template="plotly_dark",
        height=280,
        margin=dict(l=30, r=30, t=50, b=20),
        plot_bgcolor="#0f0f0f",
        paper_bgcolor="#0f0f0f",
        font=dict(color="#E0E0E0"),
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# --- Condition Trend ---
with c2:
    df2 = pd.DataFrame({
        "Condition": ["Allergy", "Injury", "Chronic", "Other"],
        "Count": [320, 210, 150, 80]
    })
    fig2 = px.bar(df2, x="Condition", y="Count", title="Top Reported Conditions",
                  color="Condition", color_discrete_sequence=px.colors.sequential.Teal)
    fig2.update_traces(marker_line_width=0.5, marker_line_color="#222")
    fig2.update_layout(
        template="plotly_dark",
        height=280,
        margin=dict(l=30, r=30, t=50, b=20),
        plot_bgcolor="#0f0f0f",
        paper_bgcolor="#0f0f0f",
        font=dict(color="#E0E0E0"),
        title_x=0.5
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ---------------- DEMOGRAPHIC INSIGHTS ----------------
st.markdown("### 🌍 Interactive Demographic Insights")

# ---- ROW 1: Gender & Age Distribution ----
col1, col2 = st.columns(2)

with col1:
    gender_data = pd.DataFrame({
        "Gender": ["Male", "Female", "Other"],
        "Count": [5200, 4800, 150]
    })
    fig_g = px.pie(gender_data, names="Gender", values="Count", title="Gender Distribution",
                   color_discrete_sequence=px.colors.sequential.Tealgrn)
    fig_g.update_traces(textinfo='percent+label', pull=[0.05, 0, 0])
    fig_g.update_layout(template="plotly_dark", height=320, title_x=0.5)
    st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})

with col2:
    ages = np.random.normal(40, 15, 1000)
    fig_age = px.histogram(pd.DataFrame({"Age": ages}), x="Age", nbins=20,
                           title="Age Distribution", color_discrete_sequence=["#4DB6AC"])
    fig_age.update_traces(marker_line_width=0.2)
    fig_age.update_layout(template="plotly_dark", height=320, title_x=0.5,
                          plot_bgcolor="#0f0f0f", paper_bgcolor="#0f0f0f")
    st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False})

# ---- ROW 2: City & Income ----
col3, col4 = st.columns(2)

with col3:
    cities = ["Boston", "Lowell", "Worcester", "Cambridge", "Springfield"]
    city_counts = [3500, 1800, 1500, 1200, 900]
    df_city = pd.DataFrame({"City": cities, "Patients": city_counts})
    fig_city = px.bar(df_city, x="City", y="Patients", title="Patients by City",
                      color="City", color_discrete_sequence=px.colors.qualitative.Prism)
    fig_city.update_traces(marker_line_width=0.5, marker_line_color="#111")
    fig_city.update_layout(template="plotly_dark", height=320, title_x=0.5)
    st.plotly_chart(fig_city, use_container_width=True, config={"displayModeBar": False})

with col4:
    df_income = pd.DataFrame({
        "Income Range": ["<25k", "25k-50k", "50k-75k", "75k-100k", "100k+"],
        "Patients": [1200, 2400, 3100, 1800, 650]
    })
    fig_income = px.area(df_income, x="Income Range", y="Patients", title="Patients by Family Income",
                         color_discrete_sequence=["#64B5F6"])
    fig_income.update_traces(line=dict(width=3))
    fig_income.update_layout(template="plotly_dark", height=320, title_x=0.5,
                             plot_bgcolor="#0f0f0f", paper_bgcolor="#0f0f0f")
    st.plotly_chart(fig_income, use_container_width=True, config={"displayModeBar": False})

# ---- ROW 3: Race & Geo Distribution ----
col5, col6 = st.columns(2)

with col5:
    df_ethnicity = pd.DataFrame({
        "Ethnicity": ["White", "Black", "Hispanic", "Asian", "Other"],
        "Count": [4500, 2200, 1800, 900, 300]
    })
    fig_eth = px.bar(df_ethnicity, x="Ethnicity", y="Count", title="Ethnicity Breakdown",
                     color="Ethnicity", color_discrete_sequence=px.colors.qualitative.Vivid)
    fig_eth.update_layout(template="plotly_dark", height=320, title_x=0.5)
    st.plotly_chart(fig_eth, use_container_width=True, config={"displayModeBar": False})

with col6:
    pass

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("💡 Use the sidebar to navigate between analytical modules.")
st.markdown(
    "<footer>© 2025 Synthea-Based Hospital Dashboard | Designed for Performance & Clarity</footer>",
    unsafe_allow_html=True
)