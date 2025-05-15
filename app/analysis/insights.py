import pandas as pd
import matplotlib.pyplot as plt

def get_flare_clusters(df: pd.DataFrame, severity_threshold: int = 4, min_duration: int = 2) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["is_flare"] = df["severity"] >= severity_threshold
    df["flare_group"] = (df["is_flare"] != df["is_flare"].shift()).cumsum()

    flare_clusters = (
        df[df["is_flare"]]
        .groupby("flare_group")["date"]
        .agg(["min", "max", "count"])
        .rename(columns={"min": "start", "max": "end", "count": "duration"})
    )
    return flare_clusters[flare_clusters["duration"] >= min_duration]


def plot_severity_with_flares(df: pd.DataFrame, flare_clusters: pd.DataFrame):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    plt.figure(figsize=(12, 4))
    plt.plot(df["date"], df["severity"], marker='o', label="Severity", color="black")

    for _, row in flare_clusters.iterrows():
        plt.axvspan(row["start"], row["end"], color="red", alpha=0.3,
                    label="Flare Period" if _ == flare_clusters.index[0] else "")
    
    plt.title("Severity Over Time with Flare Periods")
    plt.xlabel("Date")
    plt.ylabel("Severity")
    plt.ylim(0, 5.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


def get_symptom_frequencies(df: pd.DataFrame) -> pd.Series:
    return df.explode("symptoms")["symptoms"].value_counts()


def get_medication_effectiveness(df: pd.DataFrame) -> pd.Series:
    df_med = df.explode("medications")
    return df_med.groupby("medications")["severity"].mean().sort_values()


def plot_weekly_severity(df: pd.DataFrame):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    weekly_avg = df.set_index("date").resample("W")["severity"].mean()

    plt.figure(figsize=(10, 4))
    weekly_avg.plot(marker="o", title="Average Weekly Severity")
    plt.xlabel("Week")
    plt.ylabel("Severity")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
