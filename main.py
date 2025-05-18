from fastapi import FastAPI
from app.api.flare import router as flare_router
from app.api.symptom_insight import router as symptom_insight_router    

api = FastAPI()

@api.get("/")
def read_root():
    return {"message": "Hello World"}

api.include_router(flare_router)
api.include_router(symptom_insight_router)
