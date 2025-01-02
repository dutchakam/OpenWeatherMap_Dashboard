import requests
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Define the cities and API endpoint
### [Atlanta GA, Oakton VA, Richmond VA, Denver CO, Portsmouth NH, Luanda AO]
coords = [["33.749", "-84.388"], ["38.881", "-77.3008"], ["37.5538", "-77.4603"], ["39.7392", "-104.9847"], ["43.0718", "-70.7626"], ["-8.8368", "13.2343"]]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def extract_weather_data(coords):
    """Extract weather data for a list of cities."""
    weather_data = []
    for coord in coords:
        try:
            response = requests.get(BASE_URL, params={
                "lat": coord[0],
                "lon": coord[1],
                "appid": API_KEY,
                "units": "imperial"
            })
            data = response.json()
            if response.status_code == 200:
                weather_data.append({
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "weather": data["weather"][0]["description"],
                    "timestamp": pd.Timestamp.now()
                })
            else:
                print(f"Failed to fetch data for {coord}: {data.get('message')}")
        except Exception as e:
            print(f"Error fetching data for {coord}: {e}")
    return weather_data

def transform_weather_data(weather_data):
    """Transform the raw weather data into a DataFrame."""
    df = pd.DataFrame(weather_data)
    # Ensure consistent column types
    df["temperature"] = df["temperature"].astype(float)
    df["humidity"] = df["humidity"].astype(int)
    return df

def load_weather_data(df):
    """Load the transformed data into a SQLite database."""
    conn = sqlite3.connect("weather_data.db")
    try:
        df.to_sql("weather", conn, if_exists="append", index=False)
        print("Data successfully loaded into the database!")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        conn.close()

def main():
    """ETL pipeline main function."""
    print("Starting ETL pipeline...")
    
    # Extract
    raw_data = extract_weather_data(coords)
    print("Extraction complete.")
    
    # Transform
    transformed_data = transform_weather_data(raw_data)
    print("Transformation complete.")
    
    # Load
    load_weather_data(transformed_data)
    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
