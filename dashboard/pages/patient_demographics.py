import streamlit as st
import requests
import pandas as pd
try:
    import plotly.express as px
except ImportError:
    st.error("Plotly Express is not installed. Please install it using 'pip install plotly'.")
    st.stop()

st.set_page_config(
    page_title="Patient Demographics",
    page_icon="👥"
)

# Fetch patient data from API
@st.cache_data(ttl=300)
def get_patients():
    try:
        response = requests.get('http://localhost:3001/patients')
        response.raise_for_status()  # Raise exception for non-200 status
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"API connection error: {str(e)}")
        st.info("Please ensure the backend API is running on port 3001")
        return pd.DataFrame([{
            'Id': 1001,
            'FIRST': 'John',
            'LAST': 'Doe',
            'BIRTHDATE': '1985-03-15',
            'RACE': 'White',
            'GENDER': 'Male',
            'ADDRESS': '123 Main St, Boston, MA'
        }, {
            'Id': 1002,
            'FIRST': 'Jane',
            'LAST': 'Smith',
            'BIRTHDATE': '1990-07-22',
            'RACE': 'Asian',
            'GENDER': 'Female',
            'ADDRESS': '456 Oak Ave, Cambridge, MA'
        }, {
            'Id': 1003,
            'FIRST': 'Robert',
            'LAST': 'Johnson',
            'BIRTHDATE': '1978-11-05',
            'RACE': 'Black',
            'GENDER': 'Male',
            'ADDRESS': '789 Pine Rd, Somerville, MA'
        }])

st.title("👥 Patient Demographics")
st.markdown("---")

patients_df = get_patients()

if not patients_df.empty:
    # Show data source status
    if patients_df.iloc[0]['Id'] < 1000:
        st.success("✅ Live patient data loaded from API")
    else:
        st.info("ℹ️ Showing sample data - generate real patient data using the Data Generation page")
    
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
    
    st.markdown("---")
    st.markdown("## 📊 Demographic Insights")
    
    # Calculate age from birthdate
    patients_df['Age'] = (pd.to_datetime('today') - pd.to_datetime(patients_df['Birth Date'])).dt.days // 365
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Gender distribution
        gender_counts = patients_df['Gender'].value_counts()
        fig_gender = px.pie(
            gender_counts,
            names=gender_counts.index,
            values=gender_counts.values,
            title='Gender Distribution',
            color_discrete_sequence=px.colors.sequential.Teal
        )
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Race distribution
        race_counts = patients_df['Race'].value_counts()
        fig_race = px.bar(
            race_counts,
            x=race_counts.index,
            y=race_counts.values,
            title='Race Distribution',
            labels={'x': 'Race', 'y': 'Count'},
            color=race_counts.index,
            color_discrete_sequence=px.colors.sequential.Teal_r
        )
        st.plotly_chart(fig_race, use_container_width=True)
    
    with col3:
        # Age distribution
        fig_age = px.histogram(
            patients_df,
            x='Age',
            nbins=20,
            title='Age Distribution',
            color_discrete_sequence=['#4DB6AC']
        )
        fig_age.update_layout(bargap=0.1)
        st.plotly_chart(fig_age, use_container_width=True)
    
    # Top cities from addresses
    st.markdown("### 🌍 Patient Locations")
    patients_df['City'] = patients_df['Address'].str.extract(r', (\w+),')[0]
    city_counts = patients_df['City'].value_counts().head(10)
    fig_city = px.bar(
        city_counts,
        x=city_counts.index,
        y=city_counts.values,
        title='Top Cities',
        labels={'x': 'City', 'y': 'Patients'},
        color=city_counts.values,
        color_continuous_scale='Teal'
    )
    st.plotly_chart(fig_city, use_container_width=True)
    
else:
    st.warning("⚠️ No patient data available - generate data first")