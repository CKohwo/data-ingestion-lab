import pandas as pd
import json 
import requests 
from pathlib import Path 
import time
from datetime import datetime


API_URL = "https://api.konga.com/v1/graphql"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64), AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}


CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "ecommerce_api_dataset.csv"

# GraphQL query payload
payload = {
  "query": """
    {
      searchByStore(
        search_term: [["category.category_id:5237"]],
        numericFilters: [],
        sortBy: "",
        paginate: {page: 0, limit: 40},
        store_id: 1
      ) {
        pagination {
          limit
          page
          total
        }
        products {
          name
          brand
          price
          deal_price
          final_price
          description
          image_thumbnail
          sku
          seller {
            name
          }
          stock {
            in_stock
            quantity
          }
          product_rating {
            quality {
              average
              number_of_ratings
            }
          }
        }
      }
    }
  """
}


  
# Function to safely get data from API with retries  
def safe_get(API_URL, retries = 4, delay = 4): 
    #retries--The maximum number of attempts the function will make.
    #delay--The number of seconds the script will pause before making the next attempt.
    
    for attempt in range(retries):
        try:
            print(f"🌐 Attemp=t {attempt}: Fetching data from {API_URL}") 
            response = requests.post(API_URL,headers = headers, json=payload, timeout = 10, verify=True)

            response.raise_for_status()
            print("All is well...data fetched successfully!")
            return response.json() # Return the JSON data as a Python dictionary
            
            

        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}. Retrying in {delay}s...")

        # Wait before next retry
        time.sleep(delay)

    print("🚨 All retries failed. Returning None.")
    return None



# Function to normalize raw product data into a clean DataFrame  
def load(data):
     
    if not data:
        print("⚠️ No data to normalize.")
        return pd.DataFrame()  # Return empty DataFrame

    # Extract products 
    df = json.dumps(data, indent=4)
    products = data["data"]["searchByStore"]["products"]
    dfs = pd.DataFrame(products)
    dfs['fetched_at'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ Normalized {len(dfs)} products into a clean DataFrame.")
    return dfs


# Function to save DataFrame to CSV, appending if file exists
def save_to_csv(dfs, CSV_PATH):
    try:
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)


        if CSV_PATH.exists():
            existing_df = pd.read_csv(CSV_PATH)
            combined_df = pd.concat([existing_df, dfs], ignore_index=True)
         # The Procudt id is used for mapping individual iitems, we can 
         # drop duplicates based on ProductID (if it exists)
             
            combined_df.to_csv(CSV_PATH, index=False)
            print(f"💾 Data appended & saved successfully to {CSV_PATH}")
        else:
            dfs.to_csv(CSV_PATH, index=False)
            print(f"💾 New CSV created at {CSV_PATH}")

    except Exception as e:
        print(f"❌ Error saving data to CSV: {e}")
        print(f"💾 Data saved to {CSV_PATH}")
     

if __name__ == "__main__":
    data = safe_get(API_URL)
    dfs = load(data) 
    if not dfs.empty:
        save_to_csv(dfs, CSV_PATH)
     