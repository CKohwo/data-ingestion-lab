import pandas as pd
from pathlib import Path
import sys

# --- Configuration ---
# 1. The Gatekeeper: Strict Schema Definition
ADIP_STANDARD_SCHEMA = {
    "timestamp_utc": "datetime", # Must be convertible to datetime
    "entity_id": "object",       # String (City, Product Name)
    "metric_type": "object",     # String (Price, Temp, AQI)
    "metric_value": "float",     # Number (The actual data)
    "source": "object"           # String (Provenance)
}

DEFAULT_PATH = Path(__file__).resolve().parents[1] / "data" / "manual_ingest.csv"

def validate_schema(df: pd.DataFrame) -> bool:
    """
    Enforces Data Governance.
    Checks if the dataframe matches the ADIP Standard Schema.
    """
    missing_cols = [col for col in ADIP_STANDARD_SCHEMA.keys() if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"❌ Data Governance Error: Missing critical columns: {missing_cols}")
    
    # Ensure 'metric_value' is actually numeric
    if not pd.api.types.is_numeric_dtype(df['metric_value']):
        raise TypeError("❌ Data Quality Error: 'metric_value' column must be numeric.")
        
    return True

def run_local_ingestion(file_path: str = str(DEFAULT_PATH)):
    """
    Ingests a local CSV, validates it against ADIP standards, and standardizes it.
    """
    print(f"📂 [Manual] Starting Local Ingestion Sequence...")
    print(f"    Target File: {file_path}")

    try:
        path = Path(file_path)
        if not path.exists():
            # Create a template file if it doesn't exist (User Experience)
            print("⚠️ File not found. Generating template...")
            path.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(columns=ADIP_STANDARD_SCHEMA.keys()).to_csv(path, index=False)
            raise FileNotFoundError(f"Template created at {path}. Please populate data and re-run.")

        # 1. Load
        df = pd.read_csv(path)
        
        # 2. Validate (The Quality Gate)
        validate_schema(df)
        
        # 3. Standardize Dates
        df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
        
        print(f"✅ [Manual] Schema Validation Passed.")
        print(f"✅ [Manual] Successfully ingested {len(df)} rows.")
        
        # In a real scenario, we would append this to the Master Lake here
        # df.to_csv("data/master_lake.csv", mode='a', header=False)
        
        return df

    except Exception as e:
        print(f"❌ [Manual] Ingestion Failed: {e}")
        # We re-raise to ensure the Orchestrator knows it failed
        raise e

if __name__ == "__main__":
    run_local_ingestion()