import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple
from pydantic import BaseModel

def compute_matrix(df: pd.DataFrame) -> pd.DataFrame:
    symptoms_list = df['symptoms'].dropna().apply(lambda x: set(x))
    unique_symptoms = sorted({s for symptoms in symptoms_list for s in symptoms})
    matrix = pd.DataFrame(0, index=unique_symptoms, columns=unique_symptoms)

    for symptoms in symptoms_list:
        for a in symptoms:
            for b in symptoms:
                matrix.at[a, b] += 1

    return matrix
