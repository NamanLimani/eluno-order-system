import pandas as pd
import os

def ingest_data(data_path: str) -> pd.DataFrame:
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cannot find dataset at {data_path}")
    return pd.read_csv(data_path)