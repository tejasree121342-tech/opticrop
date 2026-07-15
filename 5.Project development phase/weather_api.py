"""
Thin client for the OpenWeatherMap API, usable outside the Flask app context
(e.g. from notebooks or cron jobs that refresh cached weather data).
"""
import os
import requests

API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_weather_by_city(city: str) -> dict:
    if not API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is not set in the environment.")
    resp = requests.get(f"{BASE_URL}/weather", params={"q": city, "appid": API_KEY, "units": "metric"}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_weather_by_coords(lat: float, lon: float) -> dict:
    if not API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is not set in the environment.")
    resp = requests.get(f"{BASE_URL}/weather", params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}, timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    import json
    print(json.dumps(get_weather_by_city("Hyderabad"), indent=2))
