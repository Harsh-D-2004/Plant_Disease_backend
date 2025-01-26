from database import engine , Base
from fastapi import FastAPI
from routers import farmer_routes
from routers import disease_predictor_routes
from routers import factors_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(farmer_routes.router)
app.include_router(disease_predictor_routes.router)
app.include_router(factors_routes.router)
    