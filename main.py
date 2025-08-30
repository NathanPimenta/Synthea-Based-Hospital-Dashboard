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
    
    

@app.get("/dashboard")
async def root():
    return {"Message": "Interactive dashboard for hospital readmission prediction and analysis as well as insights"}