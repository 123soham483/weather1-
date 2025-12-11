import requests

def check_aqi():
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "current": "us_aqi,pm2_5,pm10",
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {data}")
        
        current = data.get("current", {})
        us_aqi = current.get("us_aqi")
        print(f"US AQI value: {us_aqi} (Type: {type(us_aqi)})")
        
        if us_aqi is None:
            print("US AQI is None!")
        
        # Simulate the backend logic
        if us_aqi <= 50:
            print("Comparison worked")
            
    except Exception as e:
        print(f"Error: {e}")

check_aqi()
