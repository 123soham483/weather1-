"""
WeatherNow - Backend API Server (Vercel Serverless Function)
Created by: Soham
Copyright © 2025 Soham. All rights reserved.
"""

from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import httpx


ROOT_DIR = Path(__file__).parent
# In Vercel, env vars are handled by the platform, but we keep this for local dev
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
# Use get() to avoid KeyError if env vars are missing during build/initialization
mongo_url = os.environ.get('MONGO_URL')
db_name = os.environ.get('DB_NAME')

client = None
db = None

if mongo_url and db_name:
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class AirQuality(BaseModel):
    aqi: int
    category: str
    pm2_5: float
    pm10: float
    health_recommendation: str

class WeatherResponse(BaseModel):
    city: str
    country: Optional[str] = None
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    pressure: float
    weather_description: str
    icon: str
    visibility: Optional[int] = None
    timestamp: str
    air_quality: Optional[AirQuality] = None

class ForecastDay(BaseModel):
    date: str
    day_of_week: str
    temperature_max: float
    temperature_min: float
    weather_description: str
    icon: str
    precipitation_probability: int
    wind_speed: float
    humidity: int

class ForecastResponse(BaseModel):
    city: str
    country: Optional[str] = None
    current_datetime: str
    forecast_days: List[ForecastDay]

# Routes
@api_router.get("/")
async def api_root():
    return {"message": "Weather API is running"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    if not db:
        raise HTTPException(status_code=503, detail="Database connection not available")
    
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    if not db:
        raise HTTPException(status_code=503, detail="Database connection not available")
        
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

@api_router.get("/weather", response_model=WeatherResponse)
async def get_weather(city: str):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client_http:
            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            
            geo_response = await client_http.get(geocoding_url, params=geo_params)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if not geo_data.get("results"):
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
            
            location = geo_data["results"][0]
            latitude = location["latitude"]
            longitude = location["longitude"]
            city_name = location["name"]
            country = location.get("country", "")
            
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code",
                "timezone": "auto"
            }
            
            weather_response = await client_http.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            current = weather_data["current"]
            weather_code = current["weather_code"]
            weather_info = get_weather_info(weather_code)
            
            air_quality_obj = None
            try:
                air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
                air_quality_params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "pm2_5,pm10,us_aqi",
                    "timezone": "auto"
                }
                
                air_response = await client_http.get(air_quality_url, params=air_quality_params)
                air_response.raise_for_status()
                air_data = air_response.json()
                if "current" in air_data:
                    us_aqi = air_data["current"].get("us_aqi") or 0
                    pm2_5 = air_data["current"].get("pm2_5") or 0.0
                    pm10 = air_data["current"].get("pm10") or 0.0
                    
                    aqi_info = get_aqi_info(us_aqi)
                    
                    air_quality_obj = AirQuality(
                        aqi=us_aqi,
                        category=aqi_info["category"],
                        pm2_5=round(float(pm2_5), 1),
                        pm10=round(float(pm10), 1),
                        health_recommendation=aqi_info["recommendation"]
                    )
            except Exception as e:
                logger.warning(f"Could not fetch air quality data: {e}")
            
            return WeatherResponse(
                city=city_name,
                country=country,
                temperature=round(current["temperature_2m"], 1),
                feels_like=round(current["apparent_temperature"], 1),
                humidity=current["relative_humidity_2m"],
                wind_speed=round(current["wind_speed_10m"], 1),
                pressure=round(current["pressure_msl"], 1),
                weather_description=weather_info["description"],
                icon=weather_info["icon"],
                visibility=None,
                timestamp=current["time"],
                air_quality=air_quality_obj
            )
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch weather data")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(city: str):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client_http:
            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            
            geo_response = await client_http.get(geocoding_url, params=geo_params)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if not geo_data.get("results"):
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")
            
            location = geo_data["results"][0]
            latitude = location["latitude"]
            longitude = location["longitude"]
            city_name = location["name"]
            country = location.get("country", "")
            
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,relative_humidity_2m_mean",
                "timezone": "auto",
                "forecast_days": 7
            }
            
            weather_response = await client_http.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            daily = weather_data["daily"]
            
            from datetime import datetime as dt
            current_dt = dt.now(timezone.utc).isoformat()
            
            forecast_days = []
            for i in range(1, 7):
                date_str = daily["time"][i]
                date_obj = dt.fromisoformat(date_str)
                day_of_week = date_obj.strftime("%A")
                
                weather_code = daily["weather_code"][i]
                weather_info = get_weather_info(weather_code)
                
                forecast_day = ForecastDay(
                    date=date_str,
                    day_of_week=day_of_week,
                    temperature_max=round(daily["temperature_2m_max"][i], 1),
                    temperature_min=round(daily["temperature_2m_min"][i], 1),
                    weather_description=weather_info["description"],
                    icon=weather_info["icon"],
                    precipitation_probability=daily["precipitation_probability_max"][i] or 0,
                    wind_speed=round(daily["wind_speed_10m_max"][i], 1),
                    humidity=daily["relative_humidity_2m_mean"][i]
                )
                forecast_days.append(forecast_day)
            
            return ForecastResponse(
                city=city_name,
                country=country,
                current_datetime=current_dt,
                forecast_days=forecast_days
            )
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch forecast data")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def get_weather_info(code: int) -> dict:
    weather_codes = {
        0: {"description": "Clear sky", "icon": "☀️"},
        1: {"description": "Mainly clear", "icon": "🌤️"},
        2: {"description": "Partly cloudy", "icon": "⛅"},
        3: {"description": "Overcast", "icon": "☁️"},
        45: {"description": "Foggy", "icon": "🌫️"},
        48: {"description": "Depositing rime fog", "icon": "🌫️"},
        51: {"description": "Light drizzle", "icon": "🌦️"},
        53: {"description": "Moderate drizzle", "icon": "🌦️"},
        55: {"description": "Dense drizzle", "icon": "🌧️"},
        61: {"description": "Slight rain", "icon": "🌧️"},
        63: {"description": "Moderate rain", "icon": "🌧️"},
        65: {"description": "Heavy rain", "icon": "⛈️"},
        71: {"description": "Slight snow", "icon": "🌨️"},
        73: {"description": "Moderate snow", "icon": "🌨️"},
        75: {"description": "Heavy snow", "icon": "❄️"},
        77: {"description": "Snow grains", "icon": "🌨️"},
        80: {"description": "Slight rain showers", "icon": "🌦️"},
        81: {"description": "Moderate rain showers", "icon": "🌧️"},
        82: {"description": "Violent rain showers", "icon": "⛈️"},
        85: {"description": "Slight snow showers", "icon": "🌨️"},
        86: {"description": "Heavy snow showers", "icon": "❄️"},
        95: {"description": "Thunderstorm", "icon": "⛈️"},
        96: {"description": "Thunderstorm with slight hail", "icon": "⛈️"},
        99: {"description": "Thunderstorm with heavy hail", "icon": "⛈️"},
    }
    return weather_codes.get(code, {"description": "Unknown", "icon": "🌡️"})

def get_aqi_info(aqi: int) -> dict:
    if aqi <= 50:
        category = "Good"
        recommendation = "Air quality is satisfactory. Enjoy outdoor activities!"
    elif aqi <= 100:
        category = "Moderate"
        recommendation = "Air quality is acceptable. Sensitive individuals should consider reducing prolonged outdoor activities."
    elif aqi <= 150:
        category = "Unhealthy for Sensitive Groups"
        recommendation = "Sensitive groups should reduce prolonged or heavy outdoor activities."
    elif aqi <= 200:
        category = "Unhealthy"
        recommendation = "Everyone should reduce prolonged or heavy outdoor activities."
    elif aqi <= 300:
        category = "Very Unhealthy"
        recommendation = "Everyone should avoid prolonged outdoor activities."
    else:
        category = "Hazardous"
        recommendation = "Everyone should avoid all outdoor activities."
    
    return {
        "category": category,
        "recommendation": recommendation
    }

# Include the router
app.include_router(api_router)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:5173",
        "https://weather1-sand-nine.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()
