import os 
import time
import json 
import pandas as pd
import sys
import random
import subprocess 
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
DATA_PATH = "level3_automated_ingestion(Scraper + APIs)/scraper_dataset.csv" 
CATEGORY_FILE = Path("sites/categories.json")

# === GIT COMMIT FUNCTION === #

"""This function stages, commits, and pushes the updated dataset to GitHub."""     

def commit_data_to_git():
    try:
        GT_TOKEN = os.environ.get("GT_TOKEN")
        if not GT_TOKEN:
            print("❌ GT_TOKEN not set; skipping git push.")
            return

        # Build a pushable repo URL containing token (temporary, only used for push)
        repo_remote = f"https://{GT_TOKEN}@github.com/CKohwo/data-ingestion-lab.git"

        # Configure git identity
        subprocess.run(["git", "config", "--global", "user.name", "DataIngestor-bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "bot@adip.io"], check=True)

        # Stage file
        subprocess.run(["git", "add", str(DATA_PATH)], check=True)

        # Check if there is anything to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if str(DATA_PATH.name) not in status.stdout:
            print("✅ No changes to commit.")
            return

        commit_msg = f"DATA: Auto-update scraper dataset {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        # Pull with rebase to avoid simple conflicts, then push
        # Use repo_remote as the temporary remote to authenticate push
        subprocess.run(["git", "pull", repo_remote, "main", "--rebase"], check=True)
        subprocess.run(["git", "push", repo_remote, "HEAD:main"], check=True)

        print("✅ Successfully pushed scraper_dataset.csv to GitHub.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error during git commit: {e}")


# === INGESTION CYCLE FUNCTION === #

    
"""This function runs a full ingestion cycle across all categories in categories.json
Appends timestamp + category columns and merges with scraper dataset if present or creates a new one.""" 
 

def run_ingestion_cycle():
    print("\n🚀 Starting ingestion cycle...\n")

    # Load all categories
    with open(CATEGORY_FILE, "r") as file:
        categories = json.load(file)

    all_data = []

    # Loop through all categories
    for category, url in categories.items():
        try:
            print(f"🔍 Scraping category: {category}") 

            # Call our reusable core engine
            category_data = fetch_all_products(url, headers, selector)

        except Exception as e:
            print(f"❌ Error scraping category {category}: {e}")
            continue

        # Add category + timestamp metadata
        for record in category_data:
            record["Category"] = category
            record["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        all_data.extend(category_data)
        print(f"✅ Completed category: {category} | {len(category_data)} items scraped\n")

        time.sleep(random.uniform(6, 11))  # Random delay between categories to mimic human behavior

    # Convert to DataFrame
    new_data = pd.DataFrame(all_data)
    print(f"📦 New ingestion batch: {len(new_data)} records")

    # If master_dataset exists, append
    try:
        if os.path.exists(DATA_PATH) and os.path.getsize(DATA_PATH) > 0:
            existing_df = pd.read_csv(DATA_PATH)
            combined_df = pd.concat([existing_df, new_data], ignore_index=True)
        else:
            print("🆕 No existing dataset found — creating new scraper dataset...")
            combined_df = new_data

        # Save updated dataset
        combined_df.to_csv(DATA_PATH, index=False)
        print(f"💾 Updated scraper dataset saved → {DATA_PATH}\n")
        print("🕒 Ingestion cycle completed successfully.")

    except Exception as e:
        print(f"❌ Error during ingestion cycle: {e}")



if __name__ == "__main__":
    run_ingestion_cycle() 
    commit_data_to_git()