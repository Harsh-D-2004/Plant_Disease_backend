from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import factors_service
from schemas import factors_schema
from dependency import get_db

router = APIRouter(prefix="/factors", tags=["factors"])

@router.post("/", response_model=factors_schema.FactorsResponse)
def create_factors(factors: factors_schema.FactorsCreate, db: Session = Depends(get_db)):
    db_factors = factors_service.create_factors(db=db, factors=factors)

    if factors.farmer_id is None:
        raise HTTPException(status_code=400, detail="Id is required")
    
    return db_factors

@router.get("/{factors_id}", response_model=factors_schema.FactorsBase)
def get_factors(factors_id: int, db: Session = Depends(get_db)):    
    db_factors = factors_service.get_factors_by_id(db=db, factors_id=factors_id)
    if db_factors is None:
        raise HTTPException(status_code=404, detail="Factors not found")
    
    return db_factors