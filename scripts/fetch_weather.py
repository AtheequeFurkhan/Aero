import requests
import pandas as pd
import yaml
import os
from datetime import datetime

# Load Config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
CSV_PATH = "data/history.csv"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": config["weather_api"]["units"]
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def update_history():
    data_list = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_only = datetime.now().strftime("%Y-%m-%d")

    for place in config["cities"]:
        city_name = place["name"]
        data = get_weather(city_name)
        
        if data:
            row = {
                "date": date_only,
                "timestamp": timestamp,
                "city": city_name,
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }
            data_list.append(row)
    
    # Save to CSV
    df = pd.DataFrame(data_list)
    
    if os.path.exists(CSV_PATH):
        # Append without writing header
        df.to_csv(CSV_PATH, mode='a', header=False, index=False)
    else:
        # Create new with header
        os.makedirs("data", exist_ok=True)
        df.to_csv(CSV_PATH, mode='w', header=True, index=False)
        
    print(f"Weather data updated for {len(data_list)} cities.")

if __name__ == "__main__":
    update_history()