import requests
import pandas as pd
import sqlite3 
from datetime import datetime
import json
import os
import time  

API_KEY = "d5977def6093a5d3df0671e94e2d9860"

def get_city_coordinates(city_name, country_code=None):
    """Get latitude and longitude for a city"""
    
    cities = {
        'hong kong': {'lat': 22.3193, 'lon': 114.1694, 'country': 'HK'},
        'new york': {'lat': 40.7128, 'lon': -74.0060, 'country': 'US'},
        'london': {'lat': 51.5074, 'lon': -0.1278, 'country': 'GB'},
        'tokyo': {'lat': 35.6762, 'lon': 139.6503, 'country': 'JP'},
        'paris': {'lat': 48.8566, 'lon': 2.3522, 'country': 'FR'},
        'sydney': {'lat': -33.8688, 'lon': 151.2093, 'country': 'AU'},
        'mumbai': {'lat': 19.0760, 'lon': 72.8777, 'country': 'IN'},
        'singapore': {'lat': 1.3521, 'lon': 103.8198, 'country': 'SG'},
        'dubai': {'lat': 25.2048, 'lon': 55.2708, 'country': 'AE'},
        'toronto': {'lat': 43.6532, 'lon': -79.3832, 'country': 'CA'},
        'berlin': {'lat': 52.5200, 'lon': 13.4050, 'country': 'DE'}
    }
    
    city_key = city_name.lower()
    if city_key in cities:
        return cities[city_key]
    else: 
        return cities['hong kong']

def fetch_weather_data():
    """Fetch weather data from OpenWeatherMap API for multiple cities"""
    
    print("Fetching weather data from OpenWeatherMap...")
    
    if API_KEY  == "":  
        print("ERROR: You need to add your OpenWeatherMap API key!")
        print("Get it from: https://home.openweathermap.org/api_keys")
        print("Replace 'YOUR_API_KEY_HERE' in data_fetcher.py with your actual key")
        return None
    
    cities = [
        'hong kong', 'new york', 'london', 'tokyo', 'paris', 
        'sydney', 'mumbai', 'singapore', 'dubai', 'toronto', 
        'berlin'
    ]
    
    all_weather_data = []
    
    for city in cities:
        try:
            # Get city coordinates 
            coords = get_city_coordinates(city)
            url = "https://api.openweathermap.org/data/2.5/weather"
            
            # Parameters 
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': API_KEY,
                'units': 'metric'
            }
            
            # Make API request
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Get weather data
            data = response.json()
            
            # Extract data
            weather_info = {
                'city': city.title(),
                'country': coords['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'weather': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'cloudiness': data['clouds']['all'],
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'timezone': data['timezone']
            }
            
            all_weather_data.append(weather_info)
            print(f"Fetched data for {city.title()}")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")
            continue
    
    if all_weather_data:
        # Convert to pandas DataFrame
        df = pd.DataFrame(all_weather_data)
        
        # Add timestamp
        df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save to CSV
        df.to_csv('weather_data.csv', index=False)
        print(f"Data saved for {len(all_weather_data)} cities to weather_data.csv")
        
        # Save to SQLite database
        save_to_database(df)
        
        return df
    else:
        print("No data was fetched")
        return None

def save_to_database(df):
    """Save data to SQLite database"""
    try:
        conn = sqlite3.connect('weather_database.db')
        df.to_sql('weather_data', conn, if_exists='append', index=False)
        conn.close()
        print("Data saved to database")
    except Exception as e:
        print(f"Database error: {e}")

def save_api_key():
    """Helper function to save API key"""
    if not os.path.exists('config.json'):
        config = {'api_key': API_KEY}
        with open('config.json', 'w') as f:
            json.dump(config, f)
        print("Config file created")

if __name__ == "__main__":
    # Save API key to config file
    save_api_key()
    
    # Run the data fetcher
    df = fetch_weather_data()
    
    if df is not None:
        print("\nWeather Data Sample:")
        print(df[['city', 'temperature', 'weather', 'humidity', 'wind_speed']].head())