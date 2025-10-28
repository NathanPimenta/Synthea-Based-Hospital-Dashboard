import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="⚙️ Data Generation",
    layout="wide",
    page_icon="⚙️"
)

# --- UTILITIES ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def handle_generation(num_patients):
    """Simulates the API call and shows progress."""
    st.session_state['status_message'] = f"Generating {num_patients:,} patient records..."
    st.session_state['show_progress'] = True
    st.session_state['patients_to_generate'] = num_patients

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0b0c10 0%, #101820 100%);
    color: #e0e0e0;
}

/* Sidebar Styling */
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

/* Sidebar Navigation Buttons */
a.sidebar-button {
    display: block;
    text-decoration: none;
    color: #E0E0E0;
    background: none;
    font-size: 1.05em;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.3rem;
    transition: 0.25s ease;
}
a.sidebar-button:hover {
    background-color: #1b1f22;
    color: #4DB6AC;
    transform: translateX(3px);
}

/* Header Styling */
.title-header {
    text-align: center; 
    color: #4DB6AC; 
    font-size: 2.5em;
    margin-bottom: 0px;
    font-weight: 600;
}
.subtitle-header {
    text-align: center; 
    color: #BDBDBD; 
    font-size: 1.1em;
    margin-top: 0px;
}

/* Button Styling */
.stButton>button {
    background-color: #1a1a1a;
    color: #4DB6AC;
    border: 2px solid #00C4A7;
    font-weight: 700;
    border-radius: 8px;
    padding: 10px 5px;
    margin: 5px 0;
    width: 100%;
    transition: background-color 0.3s;
}
.stButton>button:hover {
    background-color: #333333;
    border-color: #4DB6AC;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 2.2em; 
    color: #BBDEFB;
}
[data-testid="stMetricLabel"] {
    font-size: 0.9em; 
    color: #AAAAAA;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.markdown("## Navigation")

st.sidebar.page_link("app.py", label="📊 Strategic & Quick Dashboard")
st.sidebar.page_link("pages/patient_demographics.py", label="👥 Patient Demographics Info")
st.sidebar.page_link("pages/data_generation.py", label="⚙️ Data Generation")

# ---------------- MAIN PAGE CONTENT ----------------
def run_data_generation_page():
    lottie_data = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_jcikwtux.json")

    # --- HEADER & ANIMATION ---
    header_col, lottie_col = st.columns([4, 1])
    with header_col:
        st.markdown("<h1 class='title-header'>Hospital Data Generation</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle-header'>Generate synthetic patient records and monitor metrics</p>", unsafe_allow_html=True)
    with lottie_col:
        if lottie_data:
            st_lottie(lottie_data, height=100, key="data_gen_anim")

    # --- MAIN SECTION ---
    interactive_col, metrics_container = st.columns([1, 1])

    # --- LEFT: Data Generation Controls ---
    with interactive_col:
        st.markdown("### 🧬 Data Generation Controls")
        patients_list = [1000, 2000, 5000, 10000, 15000]
        button_cols = st.columns(3)
        for i, num in enumerate(patients_list):
            col_index = i % 3
            if button_cols[col_index].button(f"{num:,} Patients", key=f"btn_{num}"):
                handle_generation(num)

        if 'show_progress' in st.session_state and st.session_state['show_progress']:
            st.info(st.session_state['status_message'])
            progress_bar = st.progress(0)
            for j in range(101):
                progress_bar.progress(j)
                time.sleep(0.01)
            st.success(f"✅ Finished generating {st.session_state['patients_to_generate']:,} records.")
            st.session_state['show_progress'] = False

    # --- RIGHT: Metrics Display ---
    with metrics_container:
        st.markdown("### 📈 Current Data Metrics")
        m_col1, m_col2 = st.columns(2)
        m_col3, m_col4 = st.columns(2)
        with m_col1:
            st.metric("Total Patients", "12,500", "▲ 2%")
        with m_col2:
            st.metric("Procedures Completed", "38,240", "▲ 5%")
        with m_col3:
            st.metric("Allergies Recorded", "1,542", "-3%", delta_color="inverse")
        with m_col4:
            st.metric("Unique Conditions", "1,010", "▲ 1%")

    st.markdown("---")
    st.caption("💡 Use the left navigation menu to explore other analytics modules.")


if __name__ == "__main__":
    run_data_generation_page()
