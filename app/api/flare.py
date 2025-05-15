from fastapi import APIRouter
from typing import List, Tuple
from app.models.symptom import SymptomEntry
import pandas as pd
from app.core.flares import detect_flare_clusters, FlareCluster, calculate_flare_gaps

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

@router.post("/insights/flare-gaps", response_model=Tuple[List[int], List[str], float, float])
def get_flare_gaps(entries: List[SymptomEntry]):
    df = pd.DataFrame([e.model_dump() for e in entries])
    gaps, labels, avg_gap, recent_trend = calculate_flare_gaps(df)
    return {"gaps": gaps, "labels": labels, "avg_gap": avg_gap, "recent_trend": recent_trend}

