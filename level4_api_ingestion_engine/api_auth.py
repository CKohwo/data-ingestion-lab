import os
import pandas as pd
import json
import requests
from dotenv import load_dotenv
from pathlib import Path


# Load environment variables from the (.env) file
load_dotenv()
 
#This variable stores the Weather Api key
API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError("⚠️ WEATHER_API_KEY not found in environment variables.")

#This variable stores the list of city names for which weather data is to be fetched
CITY_NAME = ["Nigeria, Lagos", "Ghana, Accra", "Kenya, Nairobi", "South Africa, Johannesburg"
             ,"Egypt, Cairo", "Morocco, Casablanca", "Ethiopia, Addis Ababa", "Tanzania, Dar es Salaam"
             ,"Uganda, Kampala", "Algeria, Algiers"]

# Base URL for the Weather API & DATA PATH for saving the dataset
BASE_URL = "http://api.weatherapi.com/v1/current.json" 
DATA_PATH = Path(__file__).resolve().parents[1] / "data" /"api_auth.csv" 
 

# Function to fetch weather data for a given city
def fetch_weather_data(city: str) -> dict | None:
    # Parameters for the API request
    params = {"key":API_KEY, "q": city, "aqi":"yes" }
   
    # Nested the API request in a try-except block to handle potential errors
    try: 
            
        response = requests.get(BASE_URL, params = params, timeout=10)
        response.raise_for_status() 
            
        print("Data fetched successfully!")
        data = response.json()

        # --- Data Parsing: This is the core logic ---
        
        # 1. Location Data
        location_data = data['location']
        
        # 2. Weather Data
        current_weather = data['current']
        
        # 3. Air Quality Data (Nested under current)
        air_quality = current_weather['air_quality']
        
        # A clean row dictionary with the required fields
        return {
            'City': location_data['name'],
            'Country': location_data['country'],
            'Latitude': location_data['lat'],
            'Longitude': location_data['lon'],
            'Timestamp_UTC': current_weather['last_updated_epoch'],
            'Temperature_C': current_weather['temp_c'],
            'Wind_KPH': current_weather['wind_kph'],
            'Condition': current_weather['condition']['text'],
            
            # --- Air Quality Metrics ---
            'AQI_US': air_quality.get('us-epa-index'), # US EPA Index (1-6)
            'CO': air_quality.get('co'),
            'NO2': air_quality.get('no2'),
            'O3': air_quality.get('o3'),
            'PM2.5': air_quality.get('pm2_5'),
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP Error for {city}: {http_err.response.status_code}. Key or City may be invalid.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error for {city}: {e}")
        return None
    except Exception as e:
        print(f"❌ Data Parsing Error for {city}: {e}")
        return None

def run_ingestion(CITY_NAME : str) -> pd.DataFrame| None:

    """Main execution function to fetch all data and save to CSV."""
    all_data = []
    print(f"--- 🌎 Starting Hybrid Ingestion for {len(CITY_NAME)} African Cities ---")

    for city in CITY_NAME:
        row = fetch_weather_data(city)
        if row:
            all_data.append(row)
            print(f"✅ Fetched data for {row['City']}, {row['Country']}")

    if not all_data:
        print("🛑 No data was successfully retrieved. Exiting.")
        return

    # Convert the list of dictionaries into a DataFrame
    new_df = pd.DataFrame(all_data)
    return new_df
 

def save_data(new_df, DATA_PATH=DATA_PATH):    
    # --- Data Persistence (Append Logic) ---
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Use the robust data saving logic we discussed
        if DATA_PATH.exists():
                try:
                    existing_df = pd.read_csv(DATA_PATH)
                    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                    print(f"Loaded existing data ({len(existing_df)} rows) and appended new data.")
                except pd.errors.EmptyDataError:
                    # Handle case where file exists but is empty
                    combined_df = new_df
                    print("Existing CSV was empty. Starting new dataset.")
                
        else:
            combined_df = new_df
            combined_df.to_csv(DATA_PATH, index=False)
            print(f"💾 New CSV created at {DATA_PATH}")

        
        # Remove duplicates, keeping the latest timestamp for each city
        # This is critical for time-series data
        combined_df = combined_df.sort_values('Timestamp_UTC', ascending=False).sort_index()

        combined_df.to_csv(DATA_PATH, index=False)
        print(f"\n--- 💾 Success: Data saved to {DATA_PATH} ---")
        print(f"Total rows in dataset: {len(combined_df)}")


# == api_auth_ingestor.py == #
def run_weather_ingestion():
    new_df = run_ingestion(CITY_NAME=CITY_NAME)
    if new_df is not None:
        save_data(new_df, DATA_PATH)


# Main execution function     
if __name__ == "__main__":
    run_weather_ingestion()