#!/usr/bin/env python3
"""
Weather Fetcher CLI Tool

A command-line interface for fetching current weather conditions and 6-day forecast for any city.
Usage: python weather_cli.py [CITY_NAME]

Examples:
  python weather_cli.py London
  python weather_cli.py "New York"
  python weather_cli.py Tokyo
"""

import sys
import requests
import os
from typing import Optional
from datetime import datetime

# Backend URL from environment or default
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
WEATHER_API_URL = f"{BACKEND_URL}/api/weather"
FORECAST_API_URL = f"{BACKEND_URL}/api/forecast"

def fetch_weather(city: str) -> Optional[dict]:
    """
    Fetch weather data for a given city from the backend API.
    
    Args:
        city: Name of the city
    
    Returns:
        Weather data dictionary or None if request fails
    """
    try:
        response = requests.get(WEATHER_API_URL, params={'city': city}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching weather data: {e}")
        return None

def fetch_forecast(city: str) -> Optional[dict]:
    """
    Fetch 6-day forecast for a given city from the backend API.
    
    Args:
        city: Name of the city
    
    Returns:
        Forecast data dictionary or None if request fails
    """
    try:
        response = requests.get(FORECAST_API_URL, params={'city': city}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching forecast data: {e}")
        return None

def format_weather_output(weather: dict) -> str:
    """
    Format weather data into a user-friendly terminal output.
    
    Args:
        weather: Weather data dictionary
    
    Returns:
        Formatted weather string
    """
    output = []
    output.append("\n" + "="*70)
    output.append(f"  {weather['icon']}  CURRENT WEATHER - {weather['city']}")
    if weather.get('country'):
        output.append(f"      {weather['country']}")
    output.append("="*70)
    output.append("")
    output.append(f"  🌡️  Temperature:      {weather['temperature']}°C")
    output.append(f"  🤚  Feels Like:       {weather['feels_like']}°C")
    output.append(f"  ☁️  Conditions:       {weather['weather_description']}")
    output.append("")
    output.append("  Additional Details:")
    output.append(f"    💧 Humidity:        {weather['humidity']}%")
    output.append(f"    💨 Wind Speed:      {weather['wind_speed']} km/h")
    output.append(f"    📊 Pressure:        {weather['pressure']} hPa")
    
    # Add AQI information if available
    if weather.get('air_quality'):
        aqi_data = weather['air_quality']
        output.append("")
        output.append("  Air Quality Index (AQI):")
        
        # Color code based on category
        aqi_icon = "🟢"
        if aqi_data['category'] == "Moderate":
            aqi_icon = "🟡"
        elif "Sensitive" in aqi_data['category']:
            aqi_icon = "🟠"
        elif aqi_data['category'] == "Unhealthy":
            aqi_icon = "🔴"
        elif "Very" in aqi_data['category']:
            aqi_icon = "🟣"
        elif aqi_data['category'] == "Hazardous":
            aqi_icon = "🟤"
        
        output.append(f"    {aqi_icon} AQI:              {aqi_data['aqi']} ({aqi_data['category']})")
        output.append(f"    💨 PM2.5:           {aqi_data['pm2_5']} µg/m³")
        output.append(f"    💨 PM10:            {aqi_data['pm10']} µg/m³")
        output.append(f"    💡 Recommendation:  {aqi_data['health_recommendation']}")
    
    output.append("")
    output.append(f"  Last Updated: {weather['timestamp']}")
    output.append("="*70 + "\n")
    
    return "\n".join(output)

def format_forecast_output(forecast: dict) -> str:
    """
    Format forecast data into a user-friendly terminal output.
    
    Args:
        forecast: Forecast data dictionary
    
    Returns:
        Formatted forecast string
    """
    output = []
    
    # Display current date & time
    current_dt = datetime.fromisoformat(forecast['current_datetime'].replace('Z', '+00:00'))
    formatted_dt = current_dt.strftime("%A, %B %d, %Y at %I:%M %p %Z")
    
    output.append("\n" + "="*70)
    output.append("  📅  6-DAY WEATHER FORECAST")
    output.append("="*70)
    output.append(f"\n  Current Date & Time: {formatted_dt}")
    output.append("")
    
    # Display each forecast day
    for day in forecast['forecast_days']:
        date_obj = datetime.fromisoformat(day['date'])
        formatted_date = date_obj.strftime("%B %d, %Y")
        
        output.append("  " + "-"*66)
        output.append(f"  {day['icon']}  {day['day_of_week']}, {formatted_date}")
        output.append("  " + "-"*66)
        output.append(f"    🌡️  Temperature:  High {day['temperature_max']}°C / Low {day['temperature_min']}°C")
        output.append(f"    ☁️  Conditions:   {day['weather_description']}")
        output.append(f"    💧 Humidity:     {day['humidity']}%")
        output.append(f"    💨 Wind Speed:   {day['wind_speed']} km/h")
        output.append(f"    🌧️  Rain Chance:  {day['precipitation_probability']}%")
        
        # Add special predictions
        predictions = []
        if day['precipitation_probability'] > 60:
            predictions.append("⚠️  High chance of rain")
        if day['wind_speed'] > 30:
            predictions.append("💨 Windy conditions expected")
        if 'clear' in day['weather_description'].lower():
            predictions.append("☀️  Sunny day ahead")
        
        if predictions:
            output.append(f"    📌 Alerts:       {', '.join(predictions)}")
        
        output.append("")
    
    output.append("="*70 + "\n")
    
    return "\n".join(output)

def main():
    """
    Main CLI entry point.
    """
    # Check if city argument is provided
    if len(sys.argv) < 2:
        print("\n🌤️  Weather Fetcher CLI")
        print("="*70)
        print("\nUsage: python weather_cli.py [CITY_NAME]")
        print("\nExamples:")
        print("  python weather_cli.py London")
        print('  python weather_cli.py "New York"')
        print("  python weather_cli.py Tokyo")
        print("\n" + "="*70 + "\n")
        sys.exit(1)
    
    # Get city name from arguments (join if multiple words)
    city = ' '.join(sys.argv[1:])
    
    print(f"\n🔍 Fetching weather data and forecast for '{city}'...")
    
    # Fetch weather data
    weather = fetch_weather(city)
    
    if not weather:
        print(f"\n❌ Could not retrieve weather data for '{city}'.")
        print("   Please check the city name and try again.\n")
        sys.exit(1)
    
    # Display current weather
    print(format_weather_output(weather))
    
    # Fetch and display forecast
    forecast = fetch_forecast(city)
    
    if forecast:
        print(format_forecast_output(forecast))
    else:
        print("⚠️  Could not retrieve forecast data.\n")

if __name__ == "__main__":
    main()