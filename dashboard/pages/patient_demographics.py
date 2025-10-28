import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Patient Demographics",
    page_icon="👥"
)

# Fetch patient data from API
@st.cache_data(ttl=300)
def get_patients():
    try:
        response = requests.get('http://localhost:3001/patients')
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except:
        return pd.DataFrame()

st.title("👥 Patient Demographics")
st.markdown("---")

patients_df = get_patients()

if not patients_df.empty:
    # Rename columns for display
    patients_df = patients_df.rename(columns={
        'Id': 'ID',
        'FIRST': 'First Name',
        'LAST': 'Last Name',
        'BIRTHDATE': 'Birth Date',
        'RACE': 'Race',
        'GENDER': 'Gender',
        'ADDRESS': 'Address'
    })
    
    # Show interactive dataframe with filters
    st.dataframe(
        patients_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn(format="%d")
        },
        column_order=["ID", "First Name", "Last Name", "Birth Date", "Race", "Gender", "Address"]
    )
else:
    st.warning("No patient data available. Please generate data first.")