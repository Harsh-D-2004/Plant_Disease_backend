from http.client import HTTPException
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models.disease_predictor import DiseasePredictor
from schemas.disease_predictor_schema import DiseasePredictorCreate
import requests
from models.factors import Factors
from models.farmer import Farmer
import onnxruntime as ort
import numpy as np
from PIL import Image
import io
from PIL import UnidentifiedImageError

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

def update_disease_predictor(db: Session, disease_predictor: DiseasePredictorCreate, predictor_id: int):
    # Fetch the existing DiseasePredictor from the database
    db_disease_predictor = db.query(DiseasePredictor).filter(DiseasePredictor.id == predictor_id).first()

    if db_disease_predictor is None:
        raise HTTPException(status_code=404, detail="DiseasePredictor not found")

    # Update the fields
    db_disease_predictor.symptoms = disease_predictor.symptoms
    db_disease_predictor.symptom_description = disease_predictor.symptom_description
    db_disease_predictor.farmer_id = disease_predictor.farmer_id

    # Fetch farmer factors
    # db_factors = get_factors_by_id(db=db, farmers_id=disease_predictor.farmer_id)
    # if db_factors is None:
    #     raise HTTPException(status_code=404, detail="Farmer factors not found")
    
    #     Location of farmer: {db_factors.city}, {db_factors.state}
    # Temperature: {db_factors.temperature}
    # Weather: {db_factors.weather}
    # Soil type: {db_factors.soil_type}
    # Symptoms: {db_disease_predictor.symptoms}

    # Construct the prompt for the Gemini API
    print(db_disease_predictor.plant_name, db_disease_predictor.disease_name, db_disease_predictor.pests, db_disease_predictor.symptoms)
    prompt = f"""
Plant Name: {db_disease_predictor.plant_name}
Disease Name: {db_disease_predictor.disease_name}

Based on the given plant name and disease name, provide a detailed solution. If any specific information is unavailable, give the best possible general information.

Ensure that every field below is filled with relevant data:
1. Cause of Disease: Clearly explain the cause, including biological, environmental.(2 lines)
2. Precautions to Take: List preventive measures that can help avoid the disease in the future.(5 points)
3. Treatment: Provide the best available treatment options, including organic, chemical, or cultural methods.(4 points)
4. Severity: (very high, high, medium, low, very low)
5. Time to treatment: (Provide an estimated treatment duration (e.g., 5 days, 2 weeks) for visible improvements.)
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyBzRisNmv2lm0nw1fj4Kml_t-2V_KIQtn0"
    # url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=AIzaSyBzRisNmv2lm0nw1fj4Kml_t-2V_KIQtn0"
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

    try:
        # Make the API request
        response = requests.post(url, json=data, **config)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()

        # Parse the response
        response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        lines = response_text.split("\n")

        # print(response_text)

        # Initialize variables
        cause_of_disease = []
        precautions_to_take = []
        treatment = []
        severity = None
        state = None
        time_to_treatment = None

        current_section = None

        for line in lines:
            line = line.strip().lstrip("0123456789.*-• ")
            if not line:
                continue  # Skip empty lines

            # Check for section headers
            if line.lower().startswith("cause of disease:"):
                current_section = "cause_of_disease"
                cause_of_disease.append(line.split(":", 1)[-1].strip())
            elif line.lower().startswith("precautions to take:"):
                current_section = "precautions_to_take"
                precautions_to_take.append(line.split(":", 1)[-1].strip())
            elif line.lower().startswith("treatment:"):
                current_section = "treatment"
                treatment.append(line.split(":", 1)[-1].strip())
            elif line.lower().startswith("severity:"):
                severity = line.split(":", 1)[-1].strip()
            elif line.lower().startswith("time to treatment:"):
                time_to_treatment = line.split(":", 1)[-1].strip()
            else:
                # Append content to the current section
                if current_section == "cause_of_disease":
                    cause_of_disease.append(line)
                elif current_section == "precautions_to_take":
                    precautions_to_take.append(line)
                elif current_section == "treatment":
                    treatment.append(line)

        # Join list items into strings
        cause_of_disease = " ".join(cause_of_disease) if cause_of_disease else None
        precautions_to_take = " ".join(precautions_to_take) if precautions_to_take else None
        treatment = " ".join(treatment) if treatment else None

        print("Cause of Disease:", cause_of_disease)
        print("Precautions:", precautions_to_take)
        print("Treatment:", treatment)
        print("Severity:", severity)
        print("State:", state)
        print("Time to Treatment:", time_to_treatment)

        db_disease_predictor.Cause_of_disease = cause_of_disease
        db_disease_predictor.Precautions_to_take = precautions_to_take
        db_disease_predictor.Treatment = treatment
        db_disease_predictor.severity = severity
        db_disease_predictor.time_to_treatment = time_to_treatment

        # Save changes to the database
        db.add(db_disease_predictor)
        db.commit()
        db.refresh(db_disease_predictor)

        # Return the updated object
        return db_disease_predictor

    except requests.exceptions.RequestException as e:
        # Handle API request errors
        print(f"API request failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch treatment details from external service")
    except KeyError as e:
        # Handle parsing errors
        print(f"Failed to parse API response: {e}")
        raise HTTPException(status_code=500, detail="Invalid response from external service")
    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

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

CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

# Define the confidence threshold
CONFIDENCE_THRESHOLD = 0.6

def preprocess_image(image_bytes, image_size):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(image_size)
    image_array = np.array(image).astype(np.float32)

    image_array /= 255.0 

    image_array = np.expand_dims(image_array, axis=0)

    return image_array

async def upload_image(image: UploadFile , db: Session):
    MODEL_PATH = r"D:\Plant_Disease_backend\Model\models\tl_inceptionv3_raw_i224_b32_e50_ft2.onnx"
    session = ort.InferenceSession(MODEL_PATH)

    input_shape = session.get_inputs()[0].shape
    image_size = (input_shape[2], input_shape[1])

    IMAGE_DIR = Path("images")
    IMAGE_DIR.mkdir(exist_ok=True)
    
    file_path = IMAGE_DIR / image.filename

    file_content = await image.read()

    with open(file_path, "wb") as buffer:
        buffer.write(file_content)

    print(f"Saved file: {file_path}")

    image.file.seek(0)
    image_bytes = await image.read()

    try:
        image_array = preprocess_image(image_bytes, image_size)
    except UnidentifiedImageError:
        return {"error": "Uploaded file is not a valid image"}

    inputs = {session.get_inputs()[0].name: image_array}
    outputs = session.run(None, inputs)

    class_probabilities = outputs[0][0]

    result_index = np.argmax(class_probabilities)
    max_probability = class_probabilities[result_index]

    if max_probability >= CONFIDENCE_THRESHOLD:
        predicted_class = CLASS_NAMES[result_index]

        split_result = predicted_class.split("___")

        category = split_result[0]
        disease = split_result[1]

        db_disease_predictor = DiseasePredictor(
            plant_name=category,
            disease_name=disease,
            infected_plant_image=str(file_path),
            pests = "",
        )

        db.add(db_disease_predictor)
        db.commit()
        db.refresh(db_disease_predictor)

        return db_disease_predictor
    else:
        return None

    
