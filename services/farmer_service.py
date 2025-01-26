from sqlalchemy.orm import Session
from schemas import farmer_schema
from models.farmer import Farmer


def create_farmer(db : Session, farmer : farmer_schema.FarmerCreate):
    db_farmer = Farmer(name=farmer.name , phone=farmer.phone , crops=farmer.crops)
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)    
    return db_farmer

def get_farmer_by_id(db : Session, farmer_id : int):
    db_farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()

    if(db_farmer is None):
        return None
    
    if(farmer_id is None):
        raise Exception("Farmer ID is required")

    return db_farmer

def update_by_id(db : Session, farmer_id : int, farmer : farmer_schema.FarmerCreate):
    db_farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if(db_farmer is None):
        raise Exception("Farmer not found")
    
    db_farmer.name = farmer.name
    db_farmer.phone = farmer.phone
    db_farmer.crops = farmer.crops
    db.commit()
    db.refresh(db_farmer)    
    return db_farmer