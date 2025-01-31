from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from services import disease_predictor_service
from schemas import disease_predictor_schema
from dependency import get_db

router = APIRouter(prefix="/disease_predictor", tags=["disease_predictor"])

@router.put("/{disease_predictor_id}", response_model=disease_predictor_schema.DiseasePredictorResponse)
def update_disease_predictor(disease_predictor: disease_predictor_schema.DiseasePredictorCreate , disease_predictor_id: int , db: Session = Depends(get_db)):
    db_disease_predictor = disease_predictor_service.update_disease_predictor(db=db, disease_predictor=disease_predictor , predictor_id=disease_predictor_id)
    
    return db_disease_predictor

@router.get("/{disease_predictor_id}", response_model=disease_predictor_schema.DiseasePredictorBase)
def get_disease_predictor_by_id(disease_predictor_id: int, db: Session = Depends(get_db)):
    db_disease_predictor = disease_predictor_service.get_disease_predictor_by_id(db=db, disease_predictor_id=disease_predictor_id)
    if db_disease_predictor is None:
        raise HTTPException(status_code=404, detail="Disease Predictor not found")
    
    return db_disease_predictor

@router.post("/image" , response_model=disease_predictor_schema.DiseasePredictorResponse)
async def upload_image(image: UploadFile = File(...) , db: Session = Depends(get_db) , ):
    disease_predictor = await disease_predictor_service.upload_image(image=image , db=db)
    return disease_predictor