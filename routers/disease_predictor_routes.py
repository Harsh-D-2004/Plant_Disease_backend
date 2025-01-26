from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services import disease_predictor_service
from schemas import disease_predictor_schema
from dependency import get_db

router = APIRouter(prefix="/disease_predictor", tags=["disease_predictor"])

@router.post("/", response_model=disease_predictor_schema.DiseasePredictorResponse)
def create_disease_predictor(disease_predictor: disease_predictor_schema.DiseasePredictorCreate, db: Session = Depends(get_db)):
    db_disease_predictor = disease_predictor_service.create_disease_predictor(db=db, disease_predictor=disease_predictor)

    if disease_predictor.plant_name is None:
        raise HTTPException(status_code=400, detail="Plant name is required")
    if disease_predictor.disease_name is None:
        raise HTTPException(status_code=400, detail="Disease name is required")
    if disease_predictor.symptoms is None:
        raise HTTPException(status_code=400, detail="Symptoms is required")
    
    return db_disease_predictor

@router.get("/{disease_predictor_id}", response_model=disease_predictor_schema.DiseasePredictorBase)
def get_disease_predictor_by_id(disease_predictor_id: int, db: Session = Depends(get_db)):
    db_disease_predictor = disease_predictor_service.get_disease_predictor_by_id(db=db, disease_predictor_id=disease_predictor_id)
    if db_disease_predictor is None:
        raise HTTPException(status_code=404, detail="Disease Predictor not found")
    
    return db_disease_predictor