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

# API URL Templates
CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?id={}&appid={}&units=metric"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?id={}&appid={}&units=metric"

# Combined CSV File Name
COMBINED_WEATHER_CSV = "combined_weather.csv"

def fetch_weather():
    combined_weather_data = []

    for city, city_id in CITIES.items():
        # Fetch Current Weather Data
        current_url = CURRENT_WEATHER_URL.format(city_id, API_KEY)
        current_response = requests.get(current_url)
        current_data = current_response.json()

        if current_response.status_code == 200:
            current_weather = {
                "Timestamp": pd.Timestamp.now(),
                "City": city,
                "Weather Type": "Current",
                "Latitude": current_data["coord"]["lat"],
                "Longitude": current_data["coord"]["lon"],
                "Temperature (°C)": current_data["main"]["temp"],
                "Feels Like (°C)": current_data["main"]["feels_like"],
                "Min Temp (°C)": current_data["main"]["temp_min"],
                "Max Temp (°C)": current_data["main"]["temp_max"],
                "Humidity (%)": current_data["main"]["humidity"],
                "Pressure (hPa)": current_data["main"]["pressure"],
                "Wind Speed (m/s)": current_data["wind"]["speed"],
                "Wind Direction (°)": current_data["wind"]["deg"],
                "Cloudiness (%)": current_data["clouds"]["all"],
                "Weather Condition": current_data["weather"][0]["description"],
                "Rain (Last 1h) (mm)": current_data.get("rain", {}).get("1h", 0),
                "Snow (Last 1h) (mm)": current_data.get("snow", {}).get("1h", 0),
                "Sunrise": pd.to_datetime(current_data["sys"]["sunrise"], unit="s"),
                "Sunset": pd.to_datetime(current_data["sys"]["sunset"], unit="s"),
            }
            combined_weather_data.append(current_weather)
        else:
            print(f"Error fetching current weather data for {city}: {current_data.get('message', 'Unknown error')}")

        # Fetch Forecast Data
        forecast_url = FORECAST_URL.format(city_id, API_KEY)
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        if forecast_response.status_code == 200:
            for entry in forecast_data["list"]:
                forecast_weather = {
                    "Timestamp": pd.to_datetime(entry["dt"], unit="s"),
                    "City": city,
                    "Weather Type": "Forecast",
                    "Latitude": forecast_data["city"]["coord"]["lat"],
                    "Longitude": forecast_data["city"]["coord"]["lon"],
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
                    "Snow (3h) (mm)": entry.get("snow", {}).get("3h", 0),
                    "Sunrise": pd.to_datetime(forecast_data["city"]["sunrise"], unit="s"),
                    "Sunset": pd.to_datetime(forecast_data["city"]["sunset"], unit="s"),
                }
                combined_weather_data.append(forecast_weather)
        else:
            print(f"Error fetching forecast data for {city}: {forecast_data.get('message', 'Unknown error')}")

    # Convert to DataFrame
    combined_df = pd.DataFrame(combined_weather_data)

    # Save to CSV file
    combined_df.to_csv(COMBINED_WEATHER_CSV, index=False)

    print(f"✅ Combined Weather Data Saved to {COMBINED_WEATHER_CSV}:\n", combined_df)

# Run the function
fetch_weather()
