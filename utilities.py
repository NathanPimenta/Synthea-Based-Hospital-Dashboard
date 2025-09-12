import pandas as pd
import numpy as np
import scipy as sp
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

data = pd.read_csv('Datasets/HCP.csv')
le = LabelEncoder()

months = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

graphConfig = {'displayModeBar': False}

def get_months() -> list:
    month_options = list(months.values())
    return month_options

def get_month_number(month_name) -> int:

    for number, name in months.items():

        if month_name == name:
            return number
    
    return None

def get_doctor_names() -> list:
    return list(data['doctorname'].unique())

def get_data():
    data['readmitted'] = le.fit_transform(data['readmitted'])
    data['Month'] = data['dischargedate'].apply(
    lambda dt: ((((datetime.strptime(dt, '%Y-%m-%d')).month)% 12)) + 1
)
    return data

if __name__ == "__main__":
    get_doctor_names()