import requests
import pandas as pd

# OpenWeatherMap API Key
API_KEY = "abaa4d0c32318cdd32cea687247af76d"

# List of Major Cities in India (City IDs from OpenWeatherMap)
CITIES = {
    "Bengaluru": 1277333,
    "Mumbai": 1275339,
    "Delhi": 1273294,
    "Chennai": 1264527,
    "Kolkata": 1275004,
    "Hyderabad": 1269843,
    "Ahmedabad": 1279233,
    "Pune": 1259229
}

# API URL Template for Forecast Data
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?id={}&appid={}&units=metric"
AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}"  # Air Quality Index API

# Combined CSV File Name
COMBINED_WEATHER_CSV = "final_forecast.csv"

def fetch_forecast():
    forecast_weather_data = []
    today = pd.Timestamp.now().normalize()
    
    for city, city_id in CITIES.items():
        # Fetch Forecast Data
        forecast_url = FORECAST_URL.format(city_id, API_KEY)
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        if forecast_response.status_code == 200:
            city_lat = forecast_data["city"]["coord"]["lat"]
            city_lon = forecast_data["city"]["coord"]["lon"]
            
            # Fetch AQI Data
            aqi_url = AQI_URL.format(city_lat, city_lon, API_KEY)
            aqi_response = requests.get(aqi_url)
            aqi_data = aqi_response.json()
            
            aqi = aqi_data["list"][0]["main"]["aqi"] if "list" in aqi_data else None
            pm2_5 = aqi_data["list"][0]["components"]["pm2_5"] if "list" in aqi_data else None
            pm10 = aqi_data["list"][0]["components"]["pm10"] if "list" in aqi_data else None

            for entry in forecast_data["list"]:
                forecast_time = pd.to_datetime(entry["dt"], unit="s")
                day_difference = (forecast_time.normalize() - today).days
                
                # Assigning day labels
                if day_difference == 0:
                    day_label = "Today"
                else:
                    day_label = f"Day {day_difference}"
                
                # Check if the forecast falls within the next 7 days from today
                if forecast_time <= today + pd.Timedelta(days=7):
                    forecast_weather = {
                        "Timestamp": forecast_time,
                        "Day": day_label,
                        "City": city,
                        "Weather Type": "Forecast",
                        "Latitude": city_lat,
                        "Longitude": city_lon,
                        "Temperature (°C)": entry["main"]["temp"],
                        "Feels Like (°C)": entry["main"]["feels_like"],
                        "Min Temp (°C)": entry["main"]["temp_min"],
                        "Max Temp (°C)": entry["main"]["temp_max"],
                        "Humidity (%)": entry["main"]["humidity"],
                        "Pressure (hPa)": entry["main"]["pressure"],
                        "Wind Speed (m/s)": entry["wind"]["speed"],
                        "Wind Direction (°)": entry["wind"]["deg"],
                        "Cloudiness (%)": entry["clouds"]["all"],
                        "Weather Condition": entry["weather"][0]["description"],
                        "Rain (3h) (mm)": entry.get("rain", {}).get("3h", 0),
                        "AQI": aqi,
                        "PM2.5 (µg/m³)": pm2_5,
                        "PM10 (µg/m³)": pm10,
                        "Sunrise": (pd.to_datetime(forecast_data["city"]["sunrise"], unit="s") + pd.Timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
                        "Sunset": (pd.to_datetime(forecast_data["city"]["sunset"], unit="s") + pd.Timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    forecast_weather_data.append(forecast_weather)
        else:
            print(f"Error fetching forecast data for {city}: {forecast_data.get('message', 'Unknown error')}")

    # Convert to DataFrame
    forecast_df = pd.DataFrame(forecast_weather_data)
    
    # Save to CSV file
    forecast_df.to_csv(COMBINED_WEATHER_CSV, index=False)
    
    print(f"✅ Forecast Data Saved to {COMBINED_WEATHER_CSV}:", forecast_df)

# Run the function
fetch_forecast()
