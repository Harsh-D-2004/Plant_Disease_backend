from pydantic import BaseModel
from typing import List

class DiseasePredictorBase(BaseModel):
    plant_name: str
    disease_name: str
    infected_plant_image: str
    pests: str
    symptoms: List[str]
    symptom_description: str
    farmer_id: int
    Preventive_measures: str
    treatment: str
    treatment_description: str
    severity: str
    state: str
    time_to_treatment: str

class DiseasePredictorCreate(BaseModel):
    plant_name: str
    disease_name: str
    infected_plant_image: str
    pests: str
    symptoms: List[str]
    symptom_description: str
    farmer_id: int

class DiseasePredictorResponse(BaseModel):
    id: int

    class Config:     
        from_attributes = True
