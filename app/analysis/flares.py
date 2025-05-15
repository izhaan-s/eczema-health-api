from pydantic import BaseModel
from typing import List
import pandas as pd

class FlareCluster(BaseModel):
    start: pd.Timestamp
    end: pd.Timestamp
    duration: int

def detect_flare_clusters(df: pd.DataFrame, threshold: int = 4, min_duration: int = 2) -> List[FlareCluster]:
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df['severity'] = pd.to_numeric(df['severity'], errors='coerce')
    df = df.sort_values("date")

    df["is_flare"] = df["severity"] > threshold

    flare_clusters = []
    current_cluster = None

    for _, row in df.iterrows():
        if row["is_flare"]:
            if current_cluster is None:
                current_cluster = FlareCluster(
                    start=row["date"],
                    end=row["date"],
                    duration=1
                )
            else:
                current_cluster.end = row["date"]
                current_cluster.duration += 1
        else:
            if current_cluster is not None:
                if current_cluster.duration >= min_duration:
                    flare_clusters.append(current_cluster)
                current_cluster = None  # reset after end

    # catch cluster at end of data
    if current_cluster is not None and current_cluster.duration >= min_duration:
        flare_clusters.append(current_cluster)

    return flare_clusters
