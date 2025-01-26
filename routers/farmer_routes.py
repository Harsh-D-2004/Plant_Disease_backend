
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import farmer_service
from schemas import farmer_schema
from dependency import get_db

router = APIRouter(prefix="/farmer", tags=["farmer"])


@router.post("/", response_model=farmer_schema.FarmerResponse)
def create_farmer(farmer: farmer_schema.FarmerCreate, db: Session = Depends(get_db)):
    db_farmer = farmer_service.create_farmer(db=db, farmer=farmer)

    if farmer.name is None:
        raise HTTPException(status_code=400, detail="Name is required")
    
    return db_farmer

@router.get("/{farmer_id}", response_model=farmer_schema.FarmerResponse)
def get_farmer_by_id(farmer_id: int, db: Session = Depends(get_db)):
    db_farmer = farmer_service.get_farmer_by_id(db=db, farmer_id=farmer_id)
    if db_farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return db_farmer    

@router.put("/{farmer_id}", response_model=farmer_schema.FarmerResponse)
def update_farmer_by_id(farmer_id: int, farmer: farmer_schema.FarmerCreate, db: Session = Depends(get_db)):
    db_farmer = farmer_service.update_by_id(db=db, farmer_id=farmer_id, farmer=farmer)
    if db_farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return db_farmer