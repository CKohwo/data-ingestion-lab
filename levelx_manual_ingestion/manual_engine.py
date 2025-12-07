# level6_manual_ingest/local_loader.py
import pandas as pd
from pathlib import Path
from scripts.schemas import ADIP_SCHEMA

def ingest_csv(file_path: Path) -> pd.DataFrame:
    """
    Lean MVP Ingestion: Reads file, checks structure, cleaning timestamps.
    """ 
    df = pd.read_csv(file_path, on_bad_lines='skip')  

    missing = [col for col in ADIP_SCHEMA if col not in df.columns]
    if missing:
        raise ValueError(f"❌ Schema Mismatch. Missing columns: {missing}")
     
    df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'], errors='coerce')
     
    clean_df = df.dropna(subset=['timestamp_utc'])
    
    print(f"✅ Ingested {len(clean_df)} valid rows from {file_path}")
    return clean_df

if __name__ == "__main__":
    # Test run
    ingest_csv(Path("data/manual_ingest.csv"))