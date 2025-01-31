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
    Cause_of_disease: str
    Precautions_to_take: str
    Treatment: str
    severity: str
    time_to_treatment: str

class DiseasePredictorCreate(BaseModel):
    symptoms: List[str]
    symptom_description: str
    farmer_id: int

class DiseasePredictorResponse(BaseModel):
    id: int

    class Config:     
        from_attributes = True
