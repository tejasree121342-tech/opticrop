import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def test_weather_current_requires_query(client):
    resp = client.get("/api/weather/current")
    assert resp.status_code == 400
    assert resp.get_json()["success"] is False


def test_weather_current_by_city(client):
    resp = client.get("/api/weather/current", query_string={"city": "Delhi"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert "temperature_c" in body["data"]


def test_weather_forecast_by_city(client):
    resp = client.get("/api/weather/forecast", query_string={"city": "Delhi"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert isinstance(body["data"]["days"], list)


def test_market_prices_returns_list(client):
    resp = client.get("/api/market/prices")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert isinstance(body["data"], list)


def test_market_forecast_requires_crop(client):
    resp = client.get("/api/market/forecast")
    assert resp.status_code == 400
    assert resp.get_json()["success"] is False


def test_market_forecast_success(client):
    resp = client.get("/api/market/forecast", query_string={"crop": "rice", "days": 3})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["crop"] == "rice"
    assert len(body["data"]["forecast"]) == 3
