import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def test_recommend_crop_missing_fields(client):
    resp = client.post("/api/prediction/recommend-crop", json={"nitrogen": 90})
    assert resp.status_code == 400
    assert resp.get_json()["success"] is False


def test_recommend_crop_success(client):
    payload = {
        "nitrogen": 90,
        "phosphorus": 42,
        "potassium": 43,
        "temperature": 25,
        "humidity": 80,
        "ph": 6.5,
        "rainfall": 200,
    }
    resp = client.post("/api/prediction/recommend-crop", json=payload)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["recommended_crop"]
    assert 0 <= body["data"]["confidence"] <= 1
    assert len(body["data"]["top_3"]) == 3


def test_yield_prediction_missing_fields(client):
    resp = client.post("/api/prediction/yield", json={"crop": "rice"})
    assert resp.status_code == 400
    assert resp.get_json()["success"] is False


def test_yield_prediction_success(client):
    payload = {"crop": "rice", "area_hectares": 2, "rainfall_mm": 150, "fertilizer_kg": 100}
    resp = client.post("/api/prediction/yield", json=payload)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["crop"] == "rice"
    assert body["data"]["predicted_yield_tons"] >= 0


def test_history_requires_auth(client):
    resp = client.get("/api/prediction/history")
    assert resp.status_code == 401


def test_history_returns_user_history(client, auth_headers):
    resp = client.get("/api/prediction/history", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert isinstance(body["data"], dict)
    assert "recommendations" in body["data"]
    assert "yield_predictions" in body["data"]
