"""To handle the backend API Calls and management of data"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter
from typing import List, DefaultDict

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

@app.get("/dashboard")
async def root():
    return {"Message": "Interactive dashboard for hospital readmission prediction and analysis as well as insights"}