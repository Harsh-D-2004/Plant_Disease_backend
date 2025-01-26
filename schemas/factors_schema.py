from pydantic import BaseModel

class FactorsBase(BaseModel):
    city: str
    state: str
    latitude : float
    longitude : float
    temperature : str
    weather : str
    soil_type : str
    farmer_id: int

class FactorsCreate(BaseModel):
    farmer_id: int

class FactorsResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True