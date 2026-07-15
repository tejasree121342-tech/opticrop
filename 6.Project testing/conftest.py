import importlib
import os
import sys

import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

DB_MODULE_NAME = "backend.database.db"
APP_MODULE_NAME = "backend.app"


@pytest.fixture(scope="session")
def temp_db_path(tmp_path_factory, monkeypatch):
    db_module = importlib.import_module(DB_MODULE_NAME)
    temp_dir = tmp_path_factory.mktemp("db")
    temp_db = os.path.join(temp_dir, "opticrop_test.db")
    monkeypatch.setattr(db_module, "DB_PATH", temp_db)
    return temp_db


@pytest.fixture
def app(temp_db_path, monkeypatch):
    if APP_MODULE_NAME in sys.modules:
        del sys.modules[APP_MODULE_NAME]
    if DB_MODULE_NAME in sys.modules:
        del sys.modules[DB_MODULE_NAME]

    db_module = importlib.import_module(DB_MODULE_NAME)
    monkeypatch.setattr(db_module, "DB_PATH", temp_db_path)
    importlib.reload(db_module)
    db_module.init_db()

    app_module = importlib.import_module(APP_MODULE_NAME)
    importlib.reload(app_module)
    app = app_module.create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_token(client):
    creds = {
        "name": "OptiCrop Tester",
        "email": "testuser@opticrop.local",
        "password": "TestPassword123",
    }
    client.post("/api/auth/register", json=creds)
    resp = client.post("/api/auth/login", json={"email": creds["email"], "password": creds["password"]})
    assert resp.status_code == 200
    return resp.get_json()["data"]["token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
