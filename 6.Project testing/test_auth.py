import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def test_register_creates_user(client):
    payload = {
        "name": "Test Farmer",
        "email": "test_register@opticrop.local",
        "password": "securePass123",
    }
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["user"]["email"] == payload["email"]
    assert "token" in body["data"]


def test_login_returns_token(client):
    payload = {"email": "test_login@opticrop.local", "password": "MySecret!"}
    client.post("/api/auth/register", json={"name": "Login Tester", **payload})
    resp = client.post("/api/auth/login", json=payload)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert "token" in body["data"]


def test_me_requires_authorization(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_me_returns_user(client, auth_headers):
    resp = client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert body["data"]["email"] == "testuser@opticrop.local"
