import os
import sys
from io import BytesIO

from PIL import Image

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def test_disease_detect_no_image(client):
    resp = client.post("/api/disease/detect", data={})
    assert resp.status_code == 400
    assert resp.get_json()["success"] is False


def test_disease_detect_invalid_file_type(client):
    resp = client.post(
        "/api/disease/detect",
        data={"image": (BytesIO(b"not-an-image"), "leaf.txt")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 400
    assert resp.get_json()["success"] is False


def test_disease_detect_success_with_image(client):
    img = Image.new("RGB", (64, 64), color=(100, 150, 200))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    resp = client.post(
        "/api/disease/detect",
        data={"image": (buffer, "leaf.png")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["success"] is True
    assert "predicted_label" in body["data"]
    assert 0 <= body["data"]["confidence"] <= 1
