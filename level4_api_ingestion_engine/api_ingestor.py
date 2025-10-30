import pandas as pd
import json 
import requests 
from pathlib import Path 
import time
from datetime import datetime


URL = "https://fakestoreapi.com/products"

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "API_dataset.csv"

  
# Function to safely get data from API with retries 

def safe_get(URL, retries = 4, delay = 4): 
    #retries--The maximum number of attempts the function will make.
    #delay--The number of seconds the script will pause before making the next attempt.
    
    for attempt in range(retries):
        try:
            print(f"🌐 Attemp=t {attempt}: Fetching data from {URL}") 
            response = requests.get(URL, timeout = 10, verify=True)

            if response.status_code == 200:
                print("All is well...data fetched successfully!")
                return response.json()
            
            else:
                print(f"⚠️ Received status code {response.status_code}, retrying...")

        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}. Retrying in {delay}s...")

        # Wait before next retry
        time.sleep(delay)

    print("🚨 All retries failed. Returning None.")
    return None


# Function to normalize raw product data into a clean DataFrame 

def normalize_products(data):
     
    if not data:
        print("⚠️ No data to normalize.")
        return pd.DataFrame()  # Return empty DataFrame
    
    records = []
    for item in data:
        try:
            record = {
                "ProductID": item.get("id"),
                "Title": item.get("title"),
                "Price": item.get("price"),
                "Category": item.get("category"),
                "Rating": item.get("rating"),
                "Description": item.get("description"),
                "ImageURL": item.get("image"),
                "Timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "Source": "FakeStoreAPI"
            }
            records.append(record)
        except Exception as e:
            print(f"❌ Error normalizing record: {e}")
            continue

    df = pd.DataFrame(records)
    print(f"✅ Normalized {len(df)} products into a clean DataFrame.")
    return df


def save_to_csv(df, CSV_PATH):
    try:
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)


        if CSV_PATH.exists():
            existing_df = pd.read_csv(CSV_PATH)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
         # The Procudt id is used for mapping individual iitems, we can 
         # drop duplicates based on ProductID (if it exists)
            if "ProductID" in combined_df.columns:
                combined_df.drop_duplicates(subset="ProductID", inplace=True)
            
            combined_df.to_csv(CSV_PATH, index=False)
            print(f"💾 Data appended & deduplicated successfully to {CSV_PATH}")
        else:
            df.to_csv(CSV_PATH, index=False)
            print(f"💾 New CSV created at {CSV_PATH}")

    except Exception as e:
        print(f"❌ Error saving data to CSV: {e}")
        print(f"💾 Data saved to {CSV_PATH}")
     

if __name__ == "__main__":
    data = safe_get(URL)
    df = normalize_products(data) 
    if not df.empty:
        save_to_csv(df, CSV_PATH)
    
 
