"""To handle the backend API Calls and management of data"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter
from typing import List, DefaultDict
from .models import Input

app = FastAPI()

app.add_middleware(

    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Message": "Welcome to hospital readmission prediction and analysis"}

@app.post("/add_data", status_code=status.HTTP_200_OK)
async def add_data(input: Input):
    input_obj = Input(

        patientid=input.patientid,
        gender=input.gender,
        department=input.department,
        diagnosis=input.diagnosis,
        admissiondate=input.admissiondate,
        dischargedate=input.dischargedate,
        doctorname=input.doctorname,
        readmitted=input.readmitted,
        city=input.city,
        severity=input.severity,
        insuranceprovider=input.insuranceprovider,
        treatmenttype=input.treatmenttype,
        bedtype=input.bedtype,
        paymentmethod=input.paymentmethod,
        age_group=input.age_group
    )

@app.get("/dashboard")
async def root():
    return {"Message": "Interactive dashboard for hospital readmission prediction and analysis as well as insights"}