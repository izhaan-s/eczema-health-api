from datetime import datetime
from typing import List, Tuple
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

def calculate_flare_gaps(df: pd.DataFrame, threshold: int = 4, min_duration: int = 2) -> Tuple[List[int], List[str], float, float]:
    clusters = detect_flare_clusters(df, threshold, min_duration)
    if len(clusters) < 2:
        return [], [], 0, 0

    gaps = []
    labels = []
    for i in range(1, len(clusters)):
        gap = (clusters[i].start - clusters[i-1].end).days
        gaps.append(gap)
        label = f"{clusters[i-1].duration}d {clusters[i].duration}d"
        labels.append(label)
    
    avg_gap = sum(gaps) / len(gaps)

    if len(gaps) >= 2:
        recent_trend = (gaps[-1] - gaps[-2]) / gaps[-2] * 100
    else:
        recent_trend = 0
    
    return gaps, labels, avg_gap, recent_trend
