from pydantic import BaseModel
from typing import List
from schemas.disease_predictor_schema import DiseasePredictorResponse
from schemas.factors_schema import FactorsResponse

class FarmerBase(BaseModel):
    name: str
    phone: str
    crops: List[str]

class FarmerCreate(FarmerBase):
    pass

class FarmerResponse(FarmerBase):
    id: int
    diseased_crops: List[DiseasePredictorResponse] = []
    factors: List[FactorsResponse] = []

    class Config:
        from_attributes = True