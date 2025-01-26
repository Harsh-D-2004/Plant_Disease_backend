import requests
from schemas import factors_schema
from models.factors import Factors
from sqlalchemy.orm import Session

def locationCoordinates():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        latitude, longitude = float(loc[0]), float(loc[1])
        city = data.get('city', 'Unknown')
        state = data.get('region', 'Unknown')
        return latitude, longitude, city, state
    
    except requests.RequestException:
        return None , None , None , None
    
def get_data(city , state):
    try:

        prompt = f"""
        Provide exact temperature in celcius and a line about how weather is and type of soil in single word based on {city} , {state}
        Give in below format
        Temperature: data
        Weather: data
        Soil Type: data
        """
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=AIzaSyBzRisNmv2lm0nw1fj4Kml_t-2V_KIQtn0"

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
            print(response.json())
            response_data = response.json()
            response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            lines = response_text.split("\n")

            temperature = None
            weather = None
            soil_type = None
            
            for line in lines:
                line = line.strip().lstrip("0123456789.*- ") 
                
                if line.lower().startswith("temperature:"):
                    temperature = line.split(":", 1)[1].strip()
                elif line.lower().startswith("weather:"):
                    weather = line.split(":", 1)[1].strip()
                elif line.lower().startswith("soil type:"):
                    soil_type = line.split(":", 1)[1].strip()
            
            return temperature, weather, soil_type
    
    except Exception as e:
        return {"error": str(e)}

def create_factors(db: Session, factors: factors_schema.FactorsCreate):
    latitude, longitude, city, state = locationCoordinates()
    
    if latitude is None or longitude is None or city is None or state is None:
        raise Exception("Failed to get location coordinates")
    
    db_factors = Factors(
        farmer_id=factors.farmer_id,
    )
    db_factors.latitude = latitude
    db_factors.longitude = longitude
    db_factors.city = city
    db_factors.state = state

    temperature, weather, soil_type = get_data(city, state)

    db_factors.temperature = temperature
    db_factors.weather = weather
    db_factors.soil_type = soil_type

    db.add(db_factors)
    db.commit()
    db.refresh(db_factors)
    return db_factors

def get_factors_by_id(db: Session, factors_id: int):
    db_factors = (
        db.query(Factors)
        .filter(Factors.id == factors_id)
        .first()
    )

    if db_factors is None:
        raise Exception("Factors not found")

    if factors_id is None:
        raise Exception("Factors ID is required")

    return db_factors