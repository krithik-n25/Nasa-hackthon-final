# modules/data_logic.py
# This file simulates fetching data from NASA's APIs and contains the business
# logic for processing that data into the format the frontend needs.
import requests
import random
import os
from dotenv import load_dotenv
from datetime import date, timedelta
from .simulation import predict_yield # Import our simulation logic


# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
print(f"🔑 API Key loaded: {API_KEY[:10] if API_KEY else 'NONE'}...")
# --- Mock NASA Data Fetching & Processing ---
def _get_mock_climate_info(lat: float, lon: float):
    """Generates random but plausible climate data as a fallback."""
    print(f"Coordinates ({lat}, {lon}) are valid, but falling back to mock climate data.")
    temp = round(random.uniform(28.0, 35.5), 1)
    rainfall = round(random.uniform(0.0, 15.0), 1)
    drought_index = round(1 - (rainfall / 15.0), 2)
    history = []
    today = date.today()
    for i in range(7):
        day = today - timedelta(days=i)
        history.append({
            "day": day.isoformat(),
            "rainfall": round(random.uniform(0.0, 20.0), 1)
        })
    return {
        "temperature": temp,
        "rainfall": rainfall,
        "drought_index": drought_index,
        "history": list(reversed(history))
    }


def get_climate_info(lat: float, lon: float):
    """
    Fetches REAL-TIME climate data from OpenWeatherMap API.
    Falls back to mocked data if the API call fails.
    """
    # OpenWeatherMap current weather endpoint
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"  # Celsius
    }
    
    try:
        # Fetch current weather
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract data from OpenWeatherMap response
        latest_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        
        # OpenWeatherMap doesn't provide direct rainfall in current weather
        # Use cloudiness and humidity to estimate drought conditions
        cloudiness = data["clouds"]["all"]  # 0-100%
        
        # Check if there's rain data (only available during rain)
        if "rain" in data and "1h" in data["rain"]:
            rainfall = data["rain"]["1h"]  # mm in last hour
        else:
            rainfall = 0.0
        
        # Calculate drought index based on humidity and cloudiness
        # Low humidity + low clouds = high drought risk
        drought_factor = (100 - humidity) / 100 * (100 - cloudiness) / 100
        drought_index = round(drought_factor, 2)
        
        # Generate mock history for the last 7 days
        # (OpenWeatherMap free tier doesn't include historical data)
        history = []
        today = date.today()
        for i in range(7):
            day = today - timedelta(days=i)
            # Vary rainfall based on current conditions
            if rainfall > 0:
                daily_rainfall = round(random.uniform(0.5, rainfall * 2), 1)
            else:
                # Dry conditions - low rainfall
                daily_rainfall = round(random.uniform(0.0, 5.0), 1)
            
            history.append({
                "day": day.isoformat(),
                "rainfall": daily_rainfall
            })
        
        return {
            "temperature": round(latest_temp, 1),
            "rainfall": round(rainfall, 1),
            "drought_index": max(0, min(1, drought_index)),  # Clamp between 0-1
            "history": list(reversed(history)),
            "humidity": humidity,  # Extra data you might want
            "cloudiness": cloudiness
        }
    
    except (requests.exceptions.RequestException, KeyError) as e:
        print(f"OpenWeatherMap API call failed: {e}. Falling back to mock data.")
        return _get_mock_climate_info(lat, lon)
# --- Mock NASA Data Fetching & Processing ---

def _get_mock_soil_info(lat: float, lon: float):
    """Generates random but plausible soil data as a fallback."""
    print(f"Coordinates ({lat}, {lon}) are valid, but falling back to mock soil data.")
    moisture = round(random.uniform(15.0, 45.0), 1)
    if moisture < 20:
        status = "critical"
    elif moisture < 30:
        status = "low moisture"
    else:
        status = "good"
    nutrients = {"N": random.randint(30, 70), "P": random.randint(20, 50), "K": random.randint(50, 90)}
    depth = {
        "0-10cm": round(moisture * random.uniform(0.8, 0.95), 1),
        "0-100cm": round(moisture * random.uniform(1.0, 1.15), 1)
    }
    return {"moisture": moisture, "nutrients": nutrients, "depth": depth, "status": status}

def get_soil_info(lat: float, lon: float):
    """
    Fetches real soil moisture data from the Crop-CASMA WMS API.
    Falls back to mocked data if the API call fails.
    """
    base_url = "https://cloud.csiss.gmu.edu/Crop-CASMA/wms"
    # Data is often a day or two behind, so let's check for yesterday's data.
    query_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")
    layer_name = "crop_casma_sm_pct"
    
    # For a GetFeatureInfo request, we define a small bounding box around our point.
    bbox = f"{lon-0.01},{lat-0.01},{lon+0.01},{lat+0.01}"

    params = {
        'SERVICE': 'WMS', 'VERSION': '1.1.1', 'REQUEST': 'GetFeatureInfo',
        'LAYERS': layer_name, 'QUERY_LAYERS': layer_name, 'BBOX': bbox,
        'WIDTH': 1, 'HEIGHT': 1, 'X': 0, 'Y': 0, 'SRS': 'EPSG:4326',
        'INFO_FORMAT': 'application/json', 'TIME': query_date,
    }

    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # The value is in the 'features' array, under 'properties', with the key 'GRAY_INDEX'.
        soil_moisture_value = data['features'][0]['properties']['GRAY_INDEX']
        moisture = round(float(soil_moisture_value), 1)

        if moisture < 20:
            status = "critical"
        elif moisture < 30:
            status = "low moisture"
        else:
            status = "good"
            
        # Nutrient levels remain mocked as there is no direct NASA API for them.
        # In a full game, this would be part of the player's state.
        nutrients = {"N": random.randint(30, 70), "P": random.randint(20, 50), "K": random.randint(50, 90)}
        
        # Mock moisture at different soil depths based on the real surface value.
        depth = {
            "0-10cm": round(moisture * random.uniform(0.95, 1.0), 1), # Surface
            "0-100cm": round(moisture * random.uniform(1.0, 1.15), 1) # Deeper
        }
        
        return {"moisture": moisture, "nutrients": nutrients, "depth": depth, "status": status}

    except (requests.exceptions.RequestException, KeyError, IndexError, ValueError) as e:
        print(f"Crop-CASMA API call failed: {e}. Falling back to mock data.")
        return _get_mock_soil_info(lat, lon)


def _get_mock_crop_info(lat: float, lon: float, crop: str):
    """Generates random but plausible crop health data as a fallback."""
    print(f"Coordinates ({lat}, {lon}) are valid, but falling back to mock crop data.")
    ndvi_value = random.uniform(0.55, 0.90)
    health_score = int((ndvi_value - 0.2) / 0.7 * 100)
    if health_score < 70:
        status = "stressed"
    elif health_score < 85:
        status = "healthy"
    else:
        status = "thriving"
    predicted_yield = predict_yield(crop, health_score)
    trend = [
        round(predicted_yield * random.uniform(0.92, 0.96), 2),
        round(predicted_yield * random.uniform(0.95, 0.99), 2),
        predicted_yield
    ]
    return {
        "health_score": health_score,
        "status": status,
        "predicted_yield": predicted_yield,
        "trend": trend
    }


def get_crop_info(lat: float, lon: float, crop: str):
    """
    Fetches real crop health (NDVI) data from the Crop-CASMA WMS API.
    Falls back to mocked data if the API call fails.
    """
    base_url = "https://cloud.csiss.gmu.edu/Crop-CASMA/wms"
    # NDVI data is not daily; we check for a recent composite image (e.g., 5 days ago)
    query_date = (date.today() - timedelta(days=5)).strftime("%Y-%m-%d")
    layer_name = "crop_casma_ndvi"
    
    bbox = f"{lon-0.01},{lat-0.01},{lon+0.01},{lat+0.01}"

    params = {
        'SERVICE': 'WMS', 'VERSION': '1.1.1', 'REQUEST': 'GetFeatureInfo',
        'LAYERS': layer_name, 'QUERY_LAYERS': layer_name, 'BBOX': bbox,
        'WIDTH': 1, 'HEIGHT': 1, 'X': 0, 'Y': 0, 'SRS': 'EPSG:4326',
        'INFO_FORMAT': 'application/json', 'TIME': query_date,
    }

    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # The raw NDVI value is returned, often needs scaling.
        raw_ndvi = float(data['features'][0]['properties']['GRAY_INDEX'])
        # MODIS NDVI is often scaled by 10000, so we divide to get the -1 to 1 range.
        ndvi_value = raw_ndvi / 10000.0

        # Convert NDVI to a simple 0-100 health score
        # A simple linear scale from 0.2 (low vegetation) to 0.9 (dense vegetation)
        health_score = int(((ndvi_value - 0.2) / (0.9 - 0.2)) * 100)
        health_score = max(0, min(100, health_score)) # Clamp between 0 and 100

        if health_score < 70:
            status = "stressed"
        elif health_score < 85:
            status = "healthy"
        else:
            status = "thriving"
        
        predicted_yield = predict_yield(crop, health_score)
        trend = [
            round(predicted_yield * random.uniform(0.92, 0.96), 2),
            round(predicted_yield * random.uniform(0.95, 0.99), 2),
            predicted_yield
        ]
        
        return {
            "health_score": health_score,
            "status": status,
            "predicted_yield": predicted_yield,
            "trend": trend
        }

    except (requests.exceptions.RequestException, KeyError, IndexError, ValueError) as e:
        print(f"Crop-CASMA NDVI call failed: {e}. Falling back to mock data.")
        return _get_mock_crop_info(lat, lon, crop)


