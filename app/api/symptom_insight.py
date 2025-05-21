from fastapi import APIRouter
from app.models.symptom import SymptomEntry
import pandas as pd
from app.core.symptoms import compute_matrix, treatment_impact
from typing import List, Dict
import logging

router = APIRouter()

@router.post("/symptom/matrix", response_model=List[dict])
def get_symptom_matrix(entries: List[SymptomEntry]):
    """
    Get the symptom matrix for the given entries.
    returns a list of dictionaries with explicitly converted float values
    """
    try:
        df = pd.DataFrame([e.model_dump() for e in entries])
        matrix = compute_matrix(df)
        
        # Convert the matrix to list of dictionaries with explicit float conversion
        result = []
        for symptom in matrix.index:
            row_dict = {}
            for col in matrix.columns:
                # Explicitly convert each value to float
                row_dict[col] = float(matrix.at[symptom, col])
            result.append(row_dict)
        
        return result
    except Exception as e:
        logging.error(f"Error in symptom matrix: {e}")
        return []

@router.post("/symptom/impact", response_model=Dict[int, float])
def get_symptom_impact(entries: List[SymptomEntry], medication: str):
    """
    Get the impact of a symptom on the severity of the condition.
    returns a dictionary with the lag day as key and the impact as value
    """
    try:
        df = pd.DataFrame([e.model_dump() for e in entries])
        return treatment_impact(df, medication)
    except Exception as e:
        logging.error(f"Error in symptom impact: {e}")
        return {}

