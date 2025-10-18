import os 
import time
import json 
import pandas as pd
import sys
from datetime import datetime
from pathlib import Path 
 
# === SETUP PATHS === #
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# === IMPORTS === #
from core.scraper_engine import fetch_all_products  
from sites.jumia_config import headers, selector 

# === CONFIGURATIONS === #
DATA_PATH = Path("data/master_dataset.csv")
CATEGORY_FILE = Path("sites/categories.json")
CATEGORY_WAIT = 10  # polite delay between categories (seconds)

"""    
This function runs a full ingestion cycle across all categories in categories.json
Appends timestamp + category columns and merges with master dataset if present or creates a new one.
"""

def run_ingestion_cycle():
    print("\n🚀 Starting ingestion cycle...\n")

    # Load all categories
    with open(CATEGORY_FILE, "r") as file:
        categories = json.load(file)

    all_data = []

    # Loop through all categories
    for category, url in categories.items():
        print(f"🔍 Scraping category: {category}")
        print(f"Found {total_pages} pages for {category}")

          
        # Call our reusable core engine
        category_data = fetch_all_products(url, headers, selector)

        # Add category + timestamp metadata
        for record in category_data:
            record["Category"] = category
            record["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        all_data.extend(category_data)
        print(f"✅ Completed category: {category} | {len(category_data)} items scraped\n")

        time.sleep(CATEGORY_WAIT)

    # Convert to DataFrame
    new_df = pd.DataFrame(all_data)
    print(f"📦 New ingestion batch: {len(new_df)} records")

    # If master_dataset exists, append
    try:
        if DATA_PATH.exists() and os.path.getsize(DATA_PATH) > 0:
            print("🔄 Existing dataset detected — appending new records...")
            old_df = pd.read_csv(DATA_PATH)
            combined_df = pd.concat([old_df, new_df], ignore_index=True)
        
        else:
            print("🆕 No existing dataset found — creating new master dataset...")
            combined_df = new_df

        # Save updated dataset
        combined_df.to_csv(DATA_PATH, index=False)
        print(f"💾 Updated master dataset saved → {DATA_PATH}\n")
        print("🕒 Ingestion cycle completed successfully.")

    except Exception as e:
        print(f"❌ Error during ingestion cycle: {e}")

if __name__ == "__main__":
    run_ingestion_cycle()

