from sqlalchemy.orm import Session
from models.disease_predictor import DiseasePredictor
from schemas.disease_predictor_schema import DiseasePredictorCreate
import requests
from models.factors import Factors
from models.farmer import Farmer

def get_factors_by_id(db: Session, farmers_id: int):
    farmer = (
        db.query(Farmer)
        .filter(Farmer.id == farmers_id)
        .first()
    )

    if farmer is None:
        raise Exception("Factors not found")

    db_factors = (
        db.query(Factors)
        .filter(Factors.farmer_id == farmers_id)
        .first()
    )

    if db_factors is None:
        raise Exception("Factors not found")

    return db_factors

def create_disease_predictor(db: Session, disease_predictor: DiseasePredictorCreate):

    # -----------------------------------------------------------------------------
    # Model logic for detecting plant and disease and symptoms comes here//./.
    # ------------------------------------------------------------------------------

    db_disease_predictor = DiseasePredictor(
        plant_name=disease_predictor.plant_name,
        disease_name=disease_predictor.disease_name,
        pests = disease_predictor.pests,
        symptoms=disease_predictor.symptoms,
        symptom_description=disease_predictor.symptom_description,
        farmer_id=disease_predictor.farmer_id,
    )

    db_factors = get_factors_by_id(db=db, farmers_id=disease_predictor.farmer_id)

    prompt = f"""
Plant Name: {db_disease_predictor.plant_name}
Disease Name: {db_disease_predictor.disease_name}
Pests : {db_disease_predictor.pests}
Symptoms: {db_disease_predictor.symptoms}
location of farmer: {db_factors.city} , {db_factors.state}
temperature: {db_factors.temperature}
weather: {db_factors.weather}
soil type: {db_factors.soil_type}


Provide a concise solution to treat plant for each of the following factors based on above information:
1. Preventive Measures: (1-2 lines)
2. Treatment: (Provide the **exact names** of pesticides, fungicides, or fertilizers available in the market that are effective for this condition.)
3. Treatment Description: (Describe a practical treatment plan in 3-4 steps, ensuring ease of implementation for farmers.)
4. Severity: (very high, high, medium, low, very low)
5. State: (healthy, sick, dead)
6. Time to treatment: (Provide an estimated treatment duration (e.g., 5 days, 2 weeks) for visible improvements.)
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyAJsAiNg0ANu12AqWraZWKGCUa8uZ3_njA"

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}],
            },
        ],
    }

    config = {
        "headers": {
            "Content-Type": "application/json",
        },
    }

    response = requests.post(url, json=data, **config)

    if response.status_code == 200:
        response_data = response.json()
        # print(response_data)
        response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]

        lines = response_text.split("\n")
        preventive_measures = None
        treatment_description = None
        severity = None
        state = None
        time_to_treatment = None

        print(response_text)

        for line in lines:
            line = line.strip().lstrip("0123456789.*- ") 
            
            if line.lower().startswith("preventive measures:"):
                preventive_measures = line.split(":", 1)[1].strip()
            elif line.lower().startswith("treatment:"):
                treatment = line.split(":", 1)[1].strip()
            elif line.lower().startswith("treatment description:"):
                treatment_description = line.split(":", 1)[1].strip()
            elif line.lower().startswith("severity:"):
                severity = line.split(":", 1)[1].strip()
            elif line.lower().startswith("state:"):
                state = line.split(":", 1)[1].strip()
            elif line.lower().startswith("time to treatment:"):
                time_to_treatment = line.split(":", 1)[1].strip()

        db_disease_predictor.Preventive_measures = preventive_measures
        db_disease_predictor.treatment = treatment  
        db_disease_predictor.treatment_description = treatment_description
        db_disease_predictor.severity = severity
        db_disease_predictor.state = state
        db_disease_predictor.time_to_treatment = time_to_treatment

        db.add(db_disease_predictor)
        db.commit()
        db.refresh(db_disease_predictor)

        return db_disease_predictor

def get_disease_predictor_by_id(db: Session, disease_predictor_id: int):
    db_disease_predictor = (
        db.query(DiseasePredictor)
        .filter(DiseasePredictor.id == disease_predictor_id)
        .first()
    )

    if db_disease_predictor is None:
        raise Exception("Disease Predictor not found")

    if disease_predictor_id is None:
        raise Exception("Disease Predictor ID is required")

    return db_disease_predictor
