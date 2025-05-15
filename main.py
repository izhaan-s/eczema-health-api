from fastapi import FastAPI
from app.api.insights import router as insights_router
api = FastAPI()

@api.get("/")
def read_root():
    return {"message": "Hello World"}

api.include_router(insights_router)
