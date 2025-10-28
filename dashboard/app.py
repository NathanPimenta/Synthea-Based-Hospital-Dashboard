import streamlit as st
import plotly.express as px
import pandas as pd

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="🏥 Strategic and Quick Dashboard",
    layout="wide",
    page_icon="🏥"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Global Theme */
body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0b0c10 0%, #101820 100%);
    color: #e0e0e0;
}

/* Sidebar */
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

/* Sidebar Links */
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

/* Main Titles */
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

/* Metrics */
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

/* Charts */
h3 {
    color: #BBDEFB;
    border-bottom: 1px solid #333;
    padding-bottom: 5px;
}

/* Footer */
footer {
    text-align: center;
    color: #777;
    padding-top: 1rem;
    font-size: 0.9em;
}

/* Responsive */
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
    # st.page_link("pages/patient_demographics.py", label="👥 Patient Demographics Info")
    st.page_link("pages/data_generation.py", label="⚙️ Data Generation")

# ---------------- MAIN CONTENT ----------------
st.markdown("<p class='main-title'>Strategic & Quick Dashboard</p>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Real-time analytics for patient engagement and hospital performance.</p>", unsafe_allow_html=True)
st.markdown("---")

# ---- KPIs ----
st.markdown("### 📈 Core Performance Indicators")
k1, k2, k3, k4 = st.columns(4)
with k1: st.metric(label="Encounters This Week", value="2,145", delta="▲ 12%")
with k2: st.metric(label="Avg. Procedure Cost", value="$455.50", delta="▼ 1.5%", delta_color="inverse")
with k3: st.metric(label="Active Patients (30 days)", value="12,500", delta="▲ 2%")
with k4: st.metric(label="Unresolved Claims", value="154", delta="▼ 25%", delta_color="inverse")

# ---- Charts Section ----
st.markdown("### 📊 Utilization & Demographic Overview")
c1, c2 = st.columns(2)

# --- Patient Volume Trend ---
with c1:
    df = pd.DataFrame({
        "Week": ["W1", "W2", "W3", "W4", "W5"],
        "Encounters": [1450, 1600, 1750, 1950, 2145]
    })
    fig = px.line(df, x="Week", y="Encounters", title="Weekly Patient Volume Trend", markers=True)
    fig.update_layout(
        template="plotly_dark",
        height=280,
        margin=dict(l=30, r=30, t=50, b=20),
        plot_bgcolor="#0f0f0f",
        paper_bgcolor="#0f0f0f",
        font=dict(color="#E0E0E0")
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Condition Trend ---
with c2:
    df2 = pd.DataFrame({
        "Condition": ["Allergy", "Injury", "Chronic", "Other"],
        "Count": [320, 210, 150, 80]
    })
    fig2 = px.bar(df2, x="Condition", y="Count", title="Top Reported Conditions")
    fig2.update_layout(
        template="plotly_dark",
        height=280,
        margin=dict(l=30, r=30, t=50, b=20),
        plot_bgcolor="#0f0f0f",
        paper_bgcolor="#0f0f0f",
        font=dict(color="#E0E0E0")
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("💡 Use the sidebar to navigate between analytical modules.")

# ---------------- FOOTER ----------------
st.markdown(
    "<footer>© 2025 Synthea-Based Hospital Dashboard | Designed for Performance & Clarity</footer>",
    unsafe_allow_html=True
)