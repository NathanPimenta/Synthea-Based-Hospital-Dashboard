import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import numpy as np
import time
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns 

# --- PAGE CONFIG ---
st.set_page_config(page_title="Synthea Hospital Data Generator", layout="wide", page_icon="🏥")

# --- CUSTOM CSS (Compacting Vertical Space) ---
st.markdown("""
<style>
/* 1. Header Styling */
.title-header {
    text-align: center; 
    color: #0077B6;
    font-size: 2.5em;
    margin-bottom: 0px;
}
.subtitle-header {
    text-align: center; 
    color: #888888;
    font-size: 1.1em;
    margin-top: 0px;
}
/* 2. COMPACTING VERTICAL MARGINS */
.stMarkdown h3 {
    margin-top: 10px;    
    margin-bottom: 5px;  
}
.block-container {
    padding-top: 1rem;   
    padding-bottom: 0rem;
}
/* 3. Button Styling (Actionable Green) */
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 5px;
    margin: 5px 0;
    width: 100%; /* Ensure buttons fill their column width */
}
/* 4. Metric Styling */
[data-testid="stMetricValue"] {
    font-size: 1.8em; 
}
[data-testid="stMetricLabel"] {
    font-size: 0.8em; 
}
</style>
""", unsafe_allow_html=True)

# --- UTILITIES ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_data = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_jcikwtux.json")

def handle_generation(num_patients):
    """Simulates the API call and shows progress."""
    st.session_state['status_message'] = f"Generating {num_patients:,} patient records..."
    st.session_state['show_progress'] = True
    st.session_state['patients_to_generate'] = num_patients

# --- MAIN LAYOUT ---

# ---------------- HEADER & ANIMATION ----------------
header_col, lottie_col = st.columns([4, 1])

with header_col:
    st.markdown("<h1 class='title-header'>Hospital Data Generation</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle-header'>Generate synthetic patient records and monitor metrics</p>", unsafe_allow_html=True)
    st.markdown("---")

with lottie_col:
    if lottie_data:
        st_lottie(lottie_data, height=100, key="data_gen_anim")


# ---------------- MAIN INTERACTIVE ROW (Buttons vs Metrics) ----------------
# Use a 1:1 ratio for the interactive column and the metrics column
interactive_col, metrics_container = st.columns([1, 1])

# --- LEFT SIDE: DATA GENERATION (Buttons & Progress) ---
with interactive_col:
    st.markdown("### 🧬 Data Generation Controls")
    patients_list = [1000, 2000, 5000, 10000, 15000]

    # Group buttons into a compact 3-column layout inside the left column
    button_cols = st.columns(3)
    
    # Place buttons sequentially across the three columns
    for i, num in enumerate(patients_list):
        if i < 3:
            col_index = i
        else:
            col_index = i - 3
        
        # Using a simple row-wise layout due to 5 buttons
        if button_cols[col_index % 3].button(f"{num:,} Patients", key=f"btn_{num}"):
            handle_generation(num)

    # --- Progress Bar Simulation ---
    if 'show_progress' in st.session_state and st.session_state['show_progress']:
        # Placing progress bar directly below the buttons
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        for j in range(101):
            progress_bar.progress(j)
            progress_text.text(f"{st.session_state['status_message']} Progress: {j}%")
            time.sleep(0.01) 

        progress_text.empty()
        progress_bar.empty()
        st.success(f"✅ Finished generating {st.session_state['patients_to_generate']:,} records.")
        st.session_state['show_progress'] = False


# --- RIGHT SIDE: CURRENT DATA METRICS ---
with metrics_container:
    st.markdown("### 📈 Current Data Metrics")
    
    # Use st.columns for a compact 2x2 grid layout inside the metrics column
    m_col1, m_col2 = st.columns(2)
    m_col3, m_col4 = st.columns(2) 

    # Data fetched from the Master ETL Singleton (Simulated values)
    m_col1.metric("Total Patients", "12,500", "▲ 2%")
    m_col2.metric("Procedures Completed", "38,240", "▲ 5%")
    m_col3.metric("Allergies Recorded", "1,542", "-3%")
    m_col4.metric("Unique Conditions", "1,010", "▲ 1%")


# ---------------- GRAPHS (Interactive Plotly Row) ----------------
st.markdown("---")
st.markdown("### 📊 Quick Visual Insights")

# Example Data (Simulated)
data = pd.DataFrame({
    'State': ['MA', 'CA', 'TX', 'NY', 'FL', 'OH'],
    'Patients': [1200, 3100, 2700, 2200, 1800, 1300]
})
procedures = pd.DataFrame({
    'Procedure': ['Surgery', 'Checkup', 'Dental', 'Therapy'],
    'Count': [1200, 5500, 2200, 3200]
})


with st.expander("Expand to view Analytical Charts"):
    
    graph_col1, graph_col2 = st.columns(2)

    # Plotly Bar Chart
    with graph_col1:
        st.subheader("Patients per State (Utilization)")
        fig_bar = px.bar(
            data, 
            x='State', 
            y='Patients', 
            title='Patient Volume by State',
            color='State'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Plotly Pie Chart
    with graph_col2:
        st.subheader("Procedures Breakdown")
        fig_pie = px.pie(
            procedures, 
            values='Count', 
            names='Procedure', 
            title='Distribution of Services Rendered'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

if __name__ == "__main__":
    pass