from fastapi import APIRouter
from app.models.symptom import SymptomEntry
import pandas as pd
from app.core.symptoms import compute_matrix, treatment_impact
from typing import List, Dict

router = APIRouter()

@router.post("/symptom/matrix", response_model=pd.DataFrame)
def get_symptom_matrix(entries: List[SymptomEntry]):
    """
    Get the symptom matrix for the given entries.
    returns a pandas dataframe with the symptom matrix
    """
    df = pd.DataFrame([e.model_dump() for e in entries])
    return compute_matrix(df)

@router.post("/symptom/impact", response_model=Dict[int, float])
def get_symptom_impact(entries: List[SymptomEntry], medication: str):
    """
    Get the impact of a symptom on the severity of the condition.
    returns a dictionary with the lag day as key and the impact as value
    """
    df = pd.DataFrame([e.model_dump() for e in entries])
    return treatment_impact(df, medication)

