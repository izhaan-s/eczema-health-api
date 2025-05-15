from datetime import datetime
from typing import List
import pandas as pd
from pydantic import BaseModel


class FlareCluster(BaseModel):
    start: datetime
    end: datetime
    duration: int

def detect_flare_clusters(df: pd.DataFrame, threshold: int = 4, min_duration: int = 2) -> List[FlareCluster]:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["severity"] = pd.to_numeric(df["severity"], errors="coerce")
    df = df.sort_values("date")

    df["is_flare"] = df["severity"] > threshold
    flare_days = df[df["is_flare"]].reset_index(drop=True)

    flare_days["gap"] = flare_days["date"].diff().dt.days.fillna(1)
    flare_days["flare_group"] = (flare_days["gap"] > 1).cumsum()

    clusters = []
    for _, group in flare_days.groupby("flare_group"):
        duration = (group["date"].iloc[-1] - group["date"].iloc[0]).days + 1
        if duration >= min_duration:
            clusters.append(FlareCluster(
                start=group["date"].iloc[0],
                end=group["date"].iloc[-1],
                duration=duration
            ))

    return clusters
