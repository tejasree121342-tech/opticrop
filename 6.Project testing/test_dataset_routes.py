import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def test_datasets_list_samples(client):
    resp = client.get("/api/datasets/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list)


def test_datasets_predict_uses_fallback(client):
    payload = {"soil_ph": 6.5, "rainfall": 120, "temperature": 25}
    resp = client.post("/api/datasets/predict", json=payload)
    assert resp.status_code == 200
    body = resp.get_json()
    assert "prediction" in body
    assert float(body["prediction"]) >= 0
