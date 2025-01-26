from pydantic import BaseModel
from typing import List
# from schemas.farmer_schema import FarmerResponse

class DiseasePredictorBase(BaseModel):
    plant_name: str
    disease_name: str
    symptoms: List[str]
    symptom_description: str
    farmer_id: int
    Preventive_measures: str
    treatment: str
    treatment_description: str
    severity: str
    state: str
    time_to_treatment: str

class DiseasePredictorCreate(DiseasePredictorBase):
    pass

class DiseasePredictorResponse(BaseModel):
    id: int

    class Config:     
        from_attributes = True
