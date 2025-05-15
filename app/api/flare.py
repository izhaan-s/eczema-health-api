from fastapi import APIRouter
from typing import List, Tuple, Dict
from app.models.symptom import SymptomEntry
import pandas as pd
from app.core.flares import detect_flare_clusters, FlareCluster, calculate_flare_gaps, get_preflare_symptom_counts

router = APIRouter()

@router.post("/insights/symptoms")
def get_symptom_insights(entries: List[SymptomEntry]):
    """
    Analyse symptom entries to give insights into the user's condition
    """

    df = pd.DataFrame([e.model_dump() for e in entries])
    # TODO: Implement the logic to analyse symptom entries
    return {"message": "Symptom insights generated successfully"}
    
@router.post("/flare/clusters", response_model=List[FlareCluster])
def get_flare_clusters(entries: List[SymptomEntry]):
    """
    Detect flare clusters in the given dataframe with a severity threshold and minimum duration.
    returns a list of flare clusters
    """
    df = pd.DataFrame([e.model_dump() for e in entries])
    flares = detect_flare_clusters(df, 3, 3)
    return flares

@router.post("/flare/gaps", response_model=Tuple[List[int], List[str], float, float])
def get_flare_gaps(entries: List[SymptomEntry]):
    """
    Calculate the gaps between flare clusters and the average gap.
    returns a tuple of gaps, labels, avg_gap, recent_trend
    """
    df = pd.DataFrame([e.model_dump() for e in entries])
    gaps, labels, avg_gap, recent_trend = calculate_flare_gaps(df)
    return (gaps, labels, avg_gap, recent_trend)

@router.post("/flare/preflare-symptoms", response_model=Dict[str, int])
def get_preflare_symptoms(entries: List[SymptomEntry]):
    """
    Get the top k symptoms before a flare going to be used to suggest treatment shortly before flares.
    returns a dictionary of symptom counts
    """
    df = pd.DataFrame([e.model_dump() for e in entries])
    return get_preflare_symptom_counts(df)
