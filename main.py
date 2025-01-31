from database import engine , Base
from fastapi import FastAPI
from routers import farmer_routes
from routers import disease_predictor_routes
from routers import factors_routes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(farmer_routes.router)
app.include_router(disease_predictor_routes.router)
app.include_router(factors_routes.router)
    