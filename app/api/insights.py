from fastapi import APIRouter
from typing import List
from app.models.symptom import SymptomEntry
import pandas as pd
from app.analysis.flares import detect_flare_clusters, FlareCluster

router = APIRouter()

@router.post("/insights/symptoms")
def get_symptom_insights(entries: List[SymptomEntry]):
    """
    Analyse symptom entries to give insights into the user's condition
    """

    df = pd.DataFrame([e.model_dump() for e in entries])
    # TODO: Implement the logic to analyse symptom entries
    return {"message": "Symptom insights generated successfully"}
    
@router.post("/insights/flare-clusters", response_model=List[FlareCluster])
def get_flare_clusters(entries: List[SymptomEntry]):
    df = pd.DataFrame([e.model_dump() for e in entries])
    flares = detect_flare_clusters(df, 3, 3)
    return flares
