from pydantic import BaseModel, field_validator, model_validator, Field
from typing import List, Optional, DefaultDict

class Input(BaseModel):

    patientid: str
    gender: str
    department: str
    diagnosis: str
    admissiondate: str
    dischargedate: str
    doctorname: str
    readmitted: str
    city: str
    severity: str
    insuranceprovider: str
    treatmenttype: str
    bedtype: str
    paymentmethod: str
    age_group: str

    model_config = DefaultDict

