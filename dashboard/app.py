# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
from dotenv import load_dotenv
import os


# ----- Load data (replace with API fetch later) -----
load_dotenv()

API_URL = os.getenv("API_URL")
@st.cache_data
def load_data():
    patients = pd.read_csv("patients.csv", parse_dates=['birth_date', 'death_date'])
    procedures = pd.read_csv("procedures.csv", parse_dates=['performed_from', 'performed_till'])
    conditions = pd.read_csv("conditions.csv", parse_dates=['event_start', 'event_end'])
    return patients, procedures, conditions

patients, procedures, conditions = load_data()

# ----- Sidebar Navigation -----
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Patients", "Procedures", "Conditions"])

# ----- Home Page -----
if page == "Home":
    st.title("🏥 Hospital Dashboard")
    st.markdown("Welcome to the hospital dashboard! Use the sidebar to navigate.")

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients", len(patients))
    col2.metric("Total Procedures", procedures['uuid'].nunique())
    col3.metric("Total Conditions", conditions['uuid'].nunique())

    # Example chart: Patients by Gender
    gender_counts = patients['gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    fig = px.pie(gender_counts, names='Gender', values='Count', title="Patients by Gender", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# ----- Patients Page -----
elif page == "Patients":
    st.title("👤 Patients Overview")
    
    # Filters
    gender_filter = st.sidebar.multiselect("Gender", options=patients['gender'].unique(), default=patients['gender'].unique())
    filtered_patients = patients[patients['gender'].isin(gender_filter)]

    # Table
    AgGrid(filtered_patients)

    # Example chart: Age distribution
    patients['age'] = (pd.Timestamp.now() - patients['birth_date']).dt.days // 365
    fig = px.histogram(filtered_patients, x='age', nbins=20, title="Patient Age Distribution")
    st.plotly_chart(fig, use_container_width=True)

# ----- Procedures Page -----
elif page == "Procedures":
    st.title("🩺 Procedures Overview")
    
    # Top Procedures
    top_proc = procedures['procedure_description'].value_counts().reset_index().head(10)
    top_proc.columns = ['Procedure', 'Count']
    fig = px.bar(top_proc, x='Procedure', y='Count', title="Top 10 Procedures")
    st.plotly_chart(fig, use_container_width=True)

    # Table
    AgGrid(procedures)

# ----- Conditions Page -----
elif page == "Conditions":
    st.title("⚕️ Conditions / Events Overview")
    
    # Top Conditions
    top_cond = conditions['event_description'].value_counts().reset_index().head(10)
    top_cond.columns = ['Condition', 'Count']
    fig = px.bar(top_cond, x='Condition', y='Count', color='Count', title="Top 10 Conditions")
    st.plotly_chart(fig, use_container_width=True)

    # Table
    AgGrid(conditions)
