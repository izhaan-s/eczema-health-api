import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Union, Optional
from pydantic import BaseModel
import logging

def compute_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a matrix of symptom matching i.e correlation between itchiness and redness.
    """
    try:
        symptoms_list = df['symptoms'].dropna().apply(lambda x: set(x))
        unique_symptoms = sorted({s for symptoms in symptoms_list for s in symptoms})
        
        if not unique_symptoms:
            return pd.DataFrame()
            
        matrix = pd.DataFrame(0, index=unique_symptoms, columns=unique_symptoms)

        for symptoms in symptoms_list:
            for a in symptoms:
                for b in symptoms:
                    matrix.at[a, b] += 1

        return matrix
    except Exception as e:
        logging.error(f"Error computing symptom matrix: {e}")
        return pd.DataFrame()

def treatment_impact(df: pd.DataFrame, medication: str, max_lag: int = 3, require_consecutive: bool = True) -> Dict[int, float]:
    """
    Return a dict {lag_day: average_severity_drop}.
      • lag = 1 → next-day effect
      • Positive value  = severity went DOWN (good)
      • Negative value  = severity went UP   (bad)
    """
    try:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        # flag medication use
        df["used"] = df["medications"].apply(
            lambda meds: medication in meds if isinstance(meds, list) else False
        )

        # ensure numeric severity
        df["severity"] = pd.to_numeric(df["severity"], errors="coerce")

        impact: Dict[int, float] = {}

        # index positions where the med was used
        use_idx: List[int] = df.index[df["used"]].tolist()

        for lag in range(1, max_lag + 1):          # start at 1 → skip "same-day 0"
            deltas: List[float] = []

            for idx in use_idx:
                after_idx = idx + lag
                if after_idx >= len(df):
                    continue

                # Optional: make sure the calendar gap really is `lag` days
                if require_consecutive:
                    try:
                        day_diff = (df.loc[after_idx, "date"] - df.loc[idx, "date"]).days  # type: ignore
                        if day_diff != lag:
                            continue
                    except:
                        continue

                before_val = df.loc[idx, "severity"]
                after_val = df.loc[after_idx, "severity"]

                try:
                    if pd.notna(before_val) and pd.notna(after_val):
                        deltas.append(float(before_val) - float(after_val))  # type: ignore
                except:
                    continue

            impact[lag] = round(sum(deltas) / len(deltas), 2) if deltas else 0.0

        return impact
    except Exception as e:
        logging.error(f"Error calculating treatment impact: {e}")
        return {i: 0.0 for i in range(1, max_lag + 1)}